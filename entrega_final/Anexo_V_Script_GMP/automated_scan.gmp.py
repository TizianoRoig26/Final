import sys
import time

# ===========================================================================
# IMPORTANTE: gvm-script 25.x usa exec() para ejecutar este archivo.
# NO llama main() automaticamente. Por eso se invoca al final del modulo.
#
# Variables disponibles en el namespace del exec():
#   gmp     -> objeto GMP autenticado (gvm.protocols.gmp.Gmp)
#   args    -> Namespace con:
#                args.argv       = [script_path, hosts, ports]
#                args.scriptargs = [hosts, ports]
#                args.username, args.password
#
# Output:
#   stderr -> mensajes de debug (no capturados por n8n como "resultado")
#   stdout -> XML del reporte (capturado en $json.stdout por n8n)
# ===========================================================================


def main(gmp, args):
    # -----------------------------------------------------------------------
    # 1. Extraer argumentos
    # args.argv[0] = ruta del script (ignorar)
    # args.argv[1] = hosts string   ej: "192.168.100.10,192.168.100.209"
    # args.argv[2] = ports string   ej: "22,80,443,5678"
    # -----------------------------------------------------------------------
    argv = args.argv  # [script_path, hosts, ports]

    sys.stderr.write(f"[GMP] argv={argv}\n")
    sys.stderr.flush()

    if len(argv) < 3:
        sys.stderr.write(
            f"[GMP] ERROR: Faltan argumentos. Se esperan 2 (hosts, ports).\n"
            f"[GMP] argv recibido: {argv}\n"
        )
        sys.stderr.flush()
        sys.exit(1)

    hosts_str = argv[1]
    ports_str = argv[2]
    timestamp  = str(int(time.time()))

    sys.stderr.write(f"[GMP] hosts={hosts_str}  ports={ports_str}\n")
    sys.stderr.flush()

    # -----------------------------------------------------------------------
    # 2. Port List dinamica (reduce el scan de horas a minutos)
    # -----------------------------------------------------------------------
    sys.stderr.write(f"[GMP] 1. Creando Port List dinamica: T:{ports_str}\n")
    sys.stderr.flush()
    res = gmp.create_port_list(
        name=f"Auto-Ports-{timestamp}",
        port_range=f"T:{ports_str}"
    )
    port_list_id = res.get('id')
    if not port_list_id:
        sys.stderr.write(f"[GMP] ERROR: create_port_list fallo. Respuesta: {res}\n")
        sys.stderr.flush()
        sys.exit(1)
    sys.stderr.write(f"[GMP] port_list_id={port_list_id}\n")
    sys.stderr.flush()

    # -----------------------------------------------------------------------
    # 3. Target
    # -----------------------------------------------------------------------
    hosts_list = [h.strip() for h in hosts_str.split(',') if h.strip()]
    if not hosts_list:
        sys.stderr.write("[GMP] ERROR: La lista de hosts esta vacia.\n")
        sys.stderr.flush()
        sys.exit(1)

    sys.stderr.write(f"[GMP] 2. Creando Target para {len(hosts_list)} host(s): {', '.join(hosts_list)}\n")
    sys.stderr.flush()
    res = gmp.create_target(
        name=f"Auto-Target-{timestamp}",
        hosts=hosts_list,
        port_list_id=port_list_id,
        alive_test="Consider Alive"
    )
    target_id = res.get('id')
    if not target_id:
        sys.stderr.write(f"[GMP] ERROR: create_target fallo. Respuesta: {res}\n")
        sys.stderr.flush()
        sys.exit(1)
    sys.stderr.write(f"[GMP] target_id={target_id}\n")
    sys.stderr.flush()

    # -----------------------------------------------------------------------
    # 4. Scan Config y Scanner
    # -----------------------------------------------------------------------
    sys.stderr.write("[GMP] 3. Buscando configuracion 'Full and fast'...\n")
    sys.stderr.flush()
    res = gmp.get_scan_configs(filter_string="Full and fast")
    config_ids = res.xpath('//config/@id')
    if not config_ids:
        sys.stderr.write("[GMP] ERROR: Configuracion 'Full and fast' no encontrada.\n")
        sys.stderr.flush()
        sys.exit(1)
    config_id = config_ids[0]

    res = gmp.get_scanners(filter_string="OpenVAS Default")
    scanner_ids = res.xpath('//scanner/@id')
    if not scanner_ids:
        sys.stderr.write("[GMP] ERROR: Scanner 'OpenVAS Default' no encontrado.\n")
        sys.stderr.flush()
        sys.exit(1)
    scanner_id = scanner_ids[0]
    sys.stderr.write(f"[GMP] config_id={config_id}  scanner_id={scanner_id}\n")
    sys.stderr.flush()

    # -----------------------------------------------------------------------
    # 5. Crear y lanzar Task
    # -----------------------------------------------------------------------
    sys.stderr.write("[GMP] 4. Creando y lanzando Task...\n")
    sys.stderr.flush()
    res = gmp.create_task(
        name=f"Auto-Scan-{timestamp}",
        config_id=config_id,
        target_id=target_id,
        scanner_id=scanner_id
    )
    task_id = res.get('id')
    if not task_id:
        sys.stderr.write(f"[GMP] ERROR: create_task fallo. Respuesta: {res}\n")
        sys.stderr.flush()
        sys.exit(1)

    res = gmp.start_task(task_id)
    report_nodes = res.xpath('//report_id')
    if not report_nodes:
        sys.stderr.write("[GMP] ERROR: start_task no retorno report_id.\n")
        sys.stderr.flush()
        sys.exit(1)
    report_id = report_nodes[0].text
    sys.stderr.write(f"[GMP] task_id={task_id}  report_id={report_id}\n")
    sys.stderr.flush()

    # -----------------------------------------------------------------------
    # 6. Polling hasta que el escaneo termine (max 30 min)
    # -----------------------------------------------------------------------
    sys.stderr.write("[GMP] 5. Polling hasta que el escaneo termine...\n")
    sys.stderr.flush()
    MAX_WAIT      = 1800
    POLL_INTERVAL = 15
    elapsed       = 0

    while elapsed < MAX_WAIT:
        res            = gmp.get_task(task_id)
        status_nodes   = res.xpath('//status')
        progress_nodes = res.xpath('//progress')
        status   = status_nodes[0].text   if status_nodes   else 'Unknown'
        progress = progress_nodes[0].text if progress_nodes else '?'
        sys.stderr.write(
            f"[GMP] status={status}  progress={progress}%  elapsed={elapsed}s\n"
        )
        sys.stderr.flush()

        if status in ('Done', 'Stopped', 'Interrupted'):
            sys.stderr.write(f"[GMP] Escaneo finalizado: {status}\n")
            sys.stderr.flush()
            break

        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL

    if elapsed >= MAX_WAIT:
        sys.stderr.write(f"[GMP] ADVERTENCIA: timeout de {MAX_WAIT}s alcanzado.\n")
        sys.stderr.flush()

    # -----------------------------------------------------------------------
    # 7. Extraer reporte XML y enviarlo a stdout (lo captura n8n)
    #    report_format_id a994b278... = formato XML nativo de OpenVAS
    # -----------------------------------------------------------------------
    sys.stderr.write("[GMP] 6. Extrayendo XML del reporte...\n")
    sys.stderr.flush()
    report = gmp.get_report(
        report_id,
        report_format_id="a994b278-1f62-11e1-96ac-406186ea4fc5",
        ignore_pagination=True,
        details=True
    )

    try:
        import lxml.etree as etree
        xml_str = etree.tostring(report, encoding='unicode')
    except (TypeError, Exception) as e:
        sys.stderr.write(f"[GMP] etree.tostring fallo ({e}), usando str(report)\n")
        sys.stderr.flush()
        xml_str = str(report)

    # Solo el XML va a stdout — n8n lo captura en $json.stdout
    print(xml_str, flush=True)
    sys.stderr.write("[GMP] XML enviado a stdout. Fin.\n")
    sys.stderr.flush()


# ===========================================================================
# gvm-script usa exec() y NO llama main() automaticamente.
# Esta linea es obligatoria para que el scan se ejecute.
# gmp y args son inyectados en el namespace del exec() por gvm-script.
# ===========================================================================
main(gmp, args)