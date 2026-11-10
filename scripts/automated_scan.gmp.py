import os
import sys
import time

# ===========================================================================
# IMPORTANTE: gvm-script 25.x usa exec() para ejecutar este archivo.
# NO llama main() automaticamente. Por eso se invoca al final del modulo.
#
# Variables disponibles en el namespace del exec():
#   gmp     -> objeto GMP autenticado (gvm.protocols.gmp.Gmp)
#   args    -> Namespace con:
#                args.argv       = [script_path, hosts, ports, scan_id]
#                args.scriptargs = [hosts, ports, scan_id]
#                args.username, args.password
#
# Output:
#   stderr -> mensajes de diagnóstico y progreso (no capturados como resultado)
#   stdout -> ÚNICAMENTE el XML del reporte (capturado en $json.stdout por n8n)
# ===========================================================================

def main(gmp, args):
    argv = args.argv  # [script_path, hosts, ports, (optional) scan_id]

    if len(argv) < 3:
        sys.stderr.write(
            f"[GMP] ERROR: Faltan argumentos. Se esperan al menos 2 (hosts, ports).\n"
            f"[GMP] argv recibido: {argv}\n"
        )
        sys.stderr.flush()
        sys.exit(1)

    hosts_str = argv[1].strip()
    ports_str = argv[2].strip()
    scan_id = argv[3].strip() if len(argv) > 3 and argv[3].strip() else f"scan_{int(time.time())}"

    sys.stderr.write(f"[GMP] Iniciando escaneo n8n: scan_id={scan_id} hosts={hosts_str} ports={ports_str}\n")
    sys.stderr.flush()

    port_list_id = None
    target_id = None
    task_id = None
    keep_objects = os.environ.get("KEEP_GVM_OBJECTS", "0") == "1"

    try:
        # -----------------------------------------------------------------------
        # 1. Port List dinámica con prefijo n8n_
        # -----------------------------------------------------------------------
        port_list_name = f"n8n_{scan_id}_ports"
        sys.stderr.write(f"[GMP] 1. Creando Port List: {port_list_name} (T:{ports_str})\n")
        sys.stderr.flush()

        res_pl = gmp.create_port_list(
            name=port_list_name,
            port_range=f"T:{ports_str}",
            comment=f"Port list dinamica generada por n8n para {scan_id}"
        )
        port_list_id = res_pl.get('id')
        if not port_list_id:
            sys.stderr.write(f"[GMP] ERROR: create_port_list fallo. Respuesta: {res_pl}\n")
            sys.stderr.flush()
            sys.exit(1)
        sys.stderr.write(f"[GMP] Port List creada: {port_list_id}\n")
        sys.stderr.flush()

        # -----------------------------------------------------------------------
        # 2. Target con prefijo n8n_
        # -----------------------------------------------------------------------
        hosts_list = [h.strip() for h in hosts_str.split(',') if h.strip()]
        if not hosts_list:
            sys.stderr.write("[GMP] ERROR: La lista de hosts esta vacia.\n")
            sys.stderr.flush()
            sys.exit(1)

        target_name = f"n8n_{scan_id}_target"
        sys.stderr.write(f"[GMP] 2. Creando Target: {target_name} ({len(hosts_list)} hosts)\n")
        sys.stderr.flush()

        res_target = gmp.create_target(
            name=target_name,
            hosts=hosts_list,
            port_list_id=port_list_id,
            alive_test="Consider Alive",
            comment=f"Target dinamico generado por n8n para {scan_id}"
        )
        target_id = res_target.get('id')
        if not target_id:
            sys.stderr.write(f"[GMP] ERROR: create_target fallo. Respuesta: {res_target}\n")
            sys.stderr.flush()
            sys.exit(1)
        sys.stderr.write(f"[GMP] Target creado: {target_id}\n")
        sys.stderr.flush()

        # -----------------------------------------------------------------------
        # 3. Scan Config y Scanner
        # -----------------------------------------------------------------------
        scan_config_id = "daba56c8-73ec-11df-a475-002264764cea"  # Full and fast
        scanner_id = None
        try:
            sc_res = gmp.get_scanners()
            for sc in sc_res.xpath('//scanner'):
                n_el = sc.xpath('name')
                if n_el and n_el[0].text == 'OpenVAS Default':
                    scanner_id = sc.get('id')
                    break
        except Exception:
            pass
        if not scanner_id:
            scanner_id = "08b69003-5fc2-4037-a479-93b440211c73"


        # -----------------------------------------------------------------------
        # 4. Crear y lanzar Task con prefijo n8n_
        # -----------------------------------------------------------------------
        task_name = f"n8n_{scan_id}_task"
        sys.stderr.write(f"[GMP] 3. Creando Task: {task_name}\n")
        sys.stderr.flush()

        res_task = gmp.create_task(
            name=task_name,
            config_id=scan_config_id,
            target_id=target_id,
            scanner_id=scanner_id,
            comment=f"Task automatizada de n8n para {scan_id}"
        )
        task_id = res_task.get('id')
        if not task_id:
            sys.stderr.write(f"[GMP] ERROR: create_task fallo. Respuesta: {res_task}\n")
            sys.stderr.flush()
            sys.exit(1)

        sys.stderr.write(f"[GMP] 4. Iniciando Task {task_id}...\n")
        sys.stderr.flush()
        res_start = gmp.start_task(task_id)
        report_nodes = res_start.xpath('//report_id')
        if not report_nodes:
            sys.stderr.write(f"[GMP] ERROR: start_task no retorno report_id. Respuesta: {res_start}\n")
            sys.stderr.flush()
            sys.exit(1)
        report_id = report_nodes[0].text
        sys.stderr.write(f"[GMP] Task iniciada exitosamente: report_id={report_id}\n")
        sys.stderr.flush()

        # -----------------------------------------------------------------------
        # 5. Polling hasta finalizacion (timeout configurable, default 5400s / 90m)
        # -----------------------------------------------------------------------
        MAX_WAIT = int(os.environ.get("MAX_WAIT_SECONDS", "5400"))
        POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "15"))
        elapsed = 0
        final_status = None

        sys.stderr.write(f"[GMP] 5. Monitoreando progreso (timeout: {MAX_WAIT}s, intervalo: {POLL_INTERVAL}s)...\n")
        sys.stderr.flush()

        while elapsed < MAX_WAIT:
            res_t = gmp.get_task(task_id)
            status_nodes = res_t.xpath('//status')
            progress_nodes = res_t.xpath('//progress')
            status = status_nodes[0].text if status_nodes else 'Unknown'
            progress = progress_nodes[0].text if progress_nodes else '?'

            sys.stderr.write(f"[GMP] Status={status} Progreso={progress}% Tiempo={elapsed}s\n")
            sys.stderr.flush()

            if status in ('Done', 'Stopped', 'Interrupted'):
                final_status = status
                break

            time.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL

        if final_status != 'Done':
            if elapsed >= MAX_WAIT:
                sys.stderr.write(f"[GMP] ERROR: Se alcanzo el timeout maximo de {MAX_WAIT}s.\n")
                try:
                    gmp.stop_task(task_id)
                except Exception as e:
                    sys.stderr.write(f"[GMP] No se pudo detener la tarea tras timeout: {e}\n")
            else:
                sys.stderr.write(f"[GMP] ERROR: La tarea finalizo con estado no exitoso: {final_status}\n")
            sys.stderr.flush()
            sys.exit(3)

        # -----------------------------------------------------------------------
        # 6. Extraer reporte XML completo
        # -----------------------------------------------------------------------
        sys.stderr.write("[GMP] 6. Extrayendo reporte XML completo...\n")
        sys.stderr.flush()

        report = gmp.get_report(
            report_id=report_id,
            report_format_id="a994b278-1f62-11e1-96ac-406186ea4fc5",
            filter_string="levels=chmlg rows=-1 min_qod=0",
            ignore_pagination=True,
            details=True
        )

        try:
            import lxml.etree as etree
            xml_str = etree.tostring(report, encoding='unicode')
        except Exception:
            xml_str = str(report)

        # Enviar ÚNICAMENTE el XML a STDOUT
        print(xml_str, flush=True)
        sys.stderr.write("[GMP] Reporte XML enviado con exito a STDOUT. Proceso completado.\n")
        sys.stderr.flush()

    except Exception as exc:
        sys.stderr.write(f"[GMP] EXCEPCION CRITICA: {exc}\n")
        sys.stderr.flush()
        sys.exit(1)
    finally:
        # -----------------------------------------------------------------------
        # Limpieza garantizada de objetos creados por n8n (prefijo n8n_)
        # Se ejecuta ante exito, sys.exit (timeout / Stopped / Interrupted) o excepcion
        # -----------------------------------------------------------------------
        if not keep_objects:
            sys.stderr.write("[GMP] Limpiando objetos temporales de GVM (n8n_*)...\n")
            sys.stderr.flush()
            if task_id:
                try:
                    res_t = gmp.get_task(task_id)
                    st = res_t.xpath('//status')
                    if st and st[0].text not in ('Done', 'Stopped', 'Interrupted'):
                        gmp.stop_task(task_id)
                        time.sleep(1)
                except Exception:
                    pass
                try:
                    gmp.delete_task(task_id)
                    sys.stderr.write(f"[GMP] Task {task_id} eliminada.\n")
                except Exception as e:
                    sys.stderr.write(f"[GMP] Advertencia: delete_task fallo ({e})\n")
            if target_id:
                try:
                    gmp.delete_target(target_id)
                    sys.stderr.write(f"[GMP] Target {target_id} eliminado.\n")
                except Exception as e:
                    sys.stderr.write(f"[GMP] Advertencia: delete_target fallo ({e})\n")
            if port_list_id:
                try:
                    gmp.delete_port_list(port_list_id)
                    sys.stderr.write(f"[GMP] Port List {port_list_id} eliminada.\n")
                except Exception as e:
                    sys.stderr.write(f"[GMP] Advertencia: delete_port_list fallo ({e})\n")
            sys.stderr.flush()

# Invocación obligatoria
main(gmp, args)
