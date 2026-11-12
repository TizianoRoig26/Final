#!/usr/bin/env python3
"""
export_openvas_report.gmp.py
Script GMP para exportar reportes duales (primario y defecto) en XML y CSV
directamente desde gvmd a través del protocolo GMP en gvm-tools.
"""
import sys
import os
import base64
import json
from lxml import etree

XML_FORMAT_ID = "a994b278-1f62-11e1-96ac-406186ea4fc5"
CSV_FORMAT_ID = "c1645568-627a-11e3-a660-406186ea4fc5"

FILTER_PRIMARIO = "levels=chmlg rows=-1 min_qod=0"
FILTER_DEFECTO = "min_qod=70 rows=-1"

def export_format(gmp, report_id, format_id, filter_string, is_csv=False):
    resp = gmp.get_report(
        report_id=report_id,
        report_format_id=format_id,
        filter_string=filter_string,
        ignore_pagination=True,
        details=True
    )
    if not is_csv:
        return etree.tostring(resp, pretty_print=True, encoding="utf-8").decode("utf-8")
    
    # Formato CSV viene en base64 dentro de la etiqueta <report>
    rep_elem = resp.find(".//report")
    if rep_elem is not None and rep_elem.text:
        return base64.b64decode(rep_elem.text.strip()).decode("utf-8", errors="replace")
    return ""

def main(gmp, args):
    argv = args.argv
    if len(argv) < 3:
        sys.stderr.write("Uso: export_openvas_report.gmp.py <report_id|latest> <output_dir> [primario|defecto|ambos]\n")
        sys.exit(1)
        
    target_rid = argv[1].strip()
    out_dir = argv[2].strip()
    perfil = argv[3].strip() if len(argv) > 3 else "ambos"
    
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Resolver report_id
    if target_rid == "latest" or not target_rid:
        reports_resp = gmp.get_reports(filter_string="rows=1")
        r_elem = reports_resp.find(".//report")
        if r_elem is None:
            sys.stderr.write("ERROR: No se encontró ningún reporte en gvmd.\n")
            sys.exit(2)
        report_id = r_elem.get("id")
    else:
        report_id = target_rid

    # 2. Obtener metadatos básicos del reporte
    rep_meta = gmp.get_report(report_id=report_id, report_format_id=XML_FORMAT_ID, filter_string="rows=1", details=False)
    rep_node = rep_meta.find(".//report")
    
    task_node = rep_node.find("task") if rep_node is not None else None
    task_id = task_node.get("id") if task_node is not None else "unknown"
    task_name = task_node.findtext("name") if task_node is not None else "unknown"
    scan_end = rep_node.findtext("scan_end") if rep_node is not None else ""
    scan_start = rep_node.findtext("scan_start") if rep_node is not None else ""
    
    sys.stderr.write(f"[export_openvas] Procesando Reporte ID: {report_id} (Tarea: {task_name}, Fin: {scan_end})\n")
    
    metadata = {
        "report_id": report_id,
        "task_id": task_id,
        "task_name": task_name,
        "scan_start_utc": scan_start,
        "scan_end_utc": scan_end,
        "archivos_generados": {}
    }
    
    # 3. Exportar Perfil Primario (levels=chmlg rows=-1 min_qod=0)
    if perfil in ("primario", "ambos"):
        sys.stderr.write(f"[export_openvas] Exportando perfil PRIMARIO ({FILTER_PRIMARIO})...\n")
        xml_prim = export_format(gmp, report_id, XML_FORMAT_ID, FILTER_PRIMARIO, is_csv=False)
        xml_prim_path = os.path.join(out_dir, "reporte_openvas_primario.xml")
        with open(xml_prim_path, "w", encoding="utf-8") as f:
            f.write(xml_prim)
        metadata["archivos_generados"]["reporte_openvas_primario.xml"] = len(xml_prim)
        
        csv_prim = export_format(gmp, report_id, CSV_FORMAT_ID, FILTER_PRIMARIO, is_csv=True)
        csv_prim_path = os.path.join(out_dir, "reporte_openvas_primario.csv")
        with open(csv_prim_path, "w", encoding="utf-8") as f:
            f.write(csv_prim)
        metadata["archivos_generados"]["reporte_openvas_primario.csv"] = len(csv_prim)
        metadata["total_hallazgos_primario"] = max(0, len(csv_prim.splitlines()) - 1) if csv_prim else 0
        sys.stderr.write(f"[export_openvas] Perfil primario exportado: {metadata['total_hallazgos_primario']} hallazgos.\n")

    # 4. Exportar Perfil Defecto (min_qod=70 rows=-1)
    if perfil in ("defecto", "ambos"):
        sys.stderr.write(f"[export_openvas] Exportando perfil DEFECTO ({FILTER_DEFECTO})...\n")
        xml_def = export_format(gmp, report_id, XML_FORMAT_ID, FILTER_DEFECTO, is_csv=False)
        xml_def_path = os.path.join(out_dir, "reporte_openvas_defecto.xml")
        with open(xml_def_path, "w", encoding="utf-8") as f:
            f.write(xml_def)
        metadata["archivos_generados"]["reporte_openvas_defecto.xml"] = len(xml_def)
        
        csv_def = export_format(gmp, report_id, CSV_FORMAT_ID, FILTER_DEFECTO, is_csv=True)
        csv_def_path = os.path.join(out_dir, "reporte_openvas_defecto.csv")
        with open(csv_def_path, "w", encoding="utf-8") as f:
            f.write(csv_def)
        metadata["archivos_generados"]["reporte_openvas_defecto.csv"] = len(csv_def)
        metadata["total_hallazgos_defecto"] = max(0, len(csv_def.splitlines()) - 1) if csv_def else 0
        sys.stderr.write(f"[export_openvas] Perfil defecto exportado: {metadata['total_hallazgos_defecto']} hallazgos.\n")
        
    meta_path = os.path.join(out_dir, "metadatos_reporte.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    print(json.dumps(metadata))

# Ejecución obligatoria en el espacio de nombres de gvm-script
main(gmp, args)
