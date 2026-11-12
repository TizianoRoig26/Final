#!/usr/bin/env python3
"""
verify_camino_b_rubric.py
Evaluador formal de efectividad de detección de vulnerabilidades contra el Ground Truth
para la réplica experimental «Camino B» (TASTSERV).
"""

import os
import sys
import csv
import json
import hashlib
import argparse

EXPECTED_REFERENCE_SHA256 = "e47970c3bda9a52120138a2858a96169fda8257aea3a9ac0c2d3ff0c7996ed5e"
DEFAULT_REF_PATH = os.path.abspath("datos/camino_b/preregistro/referencia_camino_b_v1.csv")

def verify_reference_integrity(ref_path):
    if not os.path.exists(ref_path):
        raise FileNotFoundError(f"Archivo de referencia no encontrado: {ref_path}")
    with open(ref_path, "rb") as f:
        actual_sha = hashlib.sha256(f.read()).hexdigest()
    if actual_sha != EXPECTED_REFERENCE_SHA256:
        raise ValueError(
            f"ERROR DE INTEGRIDAD: El hash de referencia {actual_sha} no coincide "
            f"con el preregistrado oficial {EXPECTED_REFERENCE_SHA256}."
        )
    return True

def load_reference(ref_path):
    verify_reference_integrity(ref_path)
    ref_items = []
    with open(ref_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            ref_items.append(row)
    return ref_items

def parse_openvas_csv(csv_path):
    findings = []
    if not os.path.exists(csv_path):
        return findings

    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = None
        for row in reader:
            if not row or not any(row):
                continue
            if header is None:
                header = [c.strip().lower() for c in row]
                continue
            
            row_dict = {}
            for i, col in enumerate(row):
                if i < len(header):
                    row_dict[header[i]] = col.strip()
            findings.append(row_dict)
    return findings

def match_item(ref, findings):
    """
    Evalúa si un ítem de referencia fue detectado en la lista de hallazgos.
    Retorna (puntaje: 0/1/2, hallazgo_coincidente, obs)
    """
    ref_host = ref["host"].strip()
    ref_port_raw = ref["puerto"].strip()
    # Extraer numero de puerto si viene ej '21/tcp' o 'general/icmp'
    ref_port = ref_port_raw.split("/")[0] if "/" in ref_port_raw else ref_port_raw
    ref_cve = ref["cve_esperado"].strip()
    rule = ref["regla_coincidencia"].strip()

    rule_type, rule_val = rule.split(":", 1) if ":" in rule else ("name_contains", rule)

    candidates = []
    for f in findings:
        f_ip = f.get("ip", "") or f.get("host", "")
        f_port = f.get("port", "")
        
        # Filtro de host
        if f_ip and f_ip != ref_host:
            continue
            
        # Filtro de puerto (para puertos específicos o hallazgos generales de servicio)
        if ref_port.isdigit():
            if f_port and not f_port.startswith(ref_port) and not f_port.startswith('general'):
                continue

        candidates.append(f)

    # Evaluar regla
    matched = None
    if rule_type == "cve":
        cve_target = rule_val.upper()
        for f in candidates:
            cves = f.get("cves", "") or f.get("cve", "")
            if cve_target in cves.upper():
                matched = f
                break
    elif rule_type == "name_contains":
        pattern = rule_val.lower()
        subpatterns = [p.strip() for p in pattern.split("|")]
        for f in candidates:
            nvt_name = (f.get("nvt name", "") or f.get("vulnerability_name", "") or f.get("name", "")).lower()
            if any(p in nvt_name for p in subpatterns):
                matched = f
                break

    if matched:
        sev = matched.get("severity", "") or matched.get("cvss", "")
        nvt = matched.get("nvt name", "") or matched.get("vulnerability_name", "") or matched.get("name", "")
        cve = matched.get("cves", "") or matched.get("cve", "")
        return (2, matched, f"Detectado correctamente: {nvt} (Sev: {sev}, CVE: {cve or 'N/A'})")
    else:
        return (0, None, f"No detectado en {ref_host} ({ref_port_raw}) con regla {rule}")

def evaluate_report(csv_path, ref_items):
    findings = parse_openvas_csv(csv_path)
    results = []
    for it in ref_items:
        score, match, obs = match_item(it, findings)
        results.append({
            "id": it["id"],
            "host": it["host"],
            "puerto": it["puerto"],
            "tipo_hallazgo": it["tipo_hallazgo"],
            "nombre_esperado": it["nombre_esperado"],
            "cve_esperado": it["cve_esperado"],
            "cvss_esperado": it["cvss_esperado"],
            "puntaje": score,
            "detectado": "Sí" if score == 2 else ("Parcial" if score == 1 else "No"),
            "observaciones": obs,
            "nombre_detectado": (match.get("nvt name") or match.get("vulnerability_name")) if match else "",
            "cve_detectado": (match.get("cves") or match.get("cve")) if match else "",
            "severidad_detectada": (match.get("severity") or match.get("cvss")) if match else ""
        })
    return results, len(findings)

def main():
    parser = argparse.ArgumentParser(description="Evaluar reporte de vulnerabilidades con rúbrica formal")
    parser.add_argument("--reporte-csv", required=True, help="Ruta al archivo CSV de hallazgos del reporte")
    parser.add_argument("--referencia", default=DEFAULT_REF_PATH, help="Ruta al archivo de referencia CSV congelado")
    parser.add_argument("--salida-json", help="Ruta opcional para exportar resultados en JSON")
    parser.add_argument("--salida-csv", help="Ruta opcional para exportar resultados en CSV")
    args = parser.parse_args()

    ref_items = load_reference(args.referencia)
    results, total_findings = evaluate_report(args.reporte_csv, ref_items)

    core_results = [r for r in results if r["id"] <= 28]
    ext_results = [r for r in results if r["id"] > 28]

    core_detected = sum(1 for r in core_results if r["puntaje"] == 2)
    ext_detected = sum(1 for r in ext_results if r["puntaje"] == 2)

    print("=" * 70)
    print("      EVALUACIÓN DE EFECTIVIDAD — CAMINO B (TASTSERV)")
    print("=" * 70)
    print(f"Reporte evaluado: {args.reporte_csv}")
    print(f"Total hallazgos brutos en el reporte: {total_findings}")
    print("-" * 70)
    print(f"CONJUNTO CORE (28 ítems vigentes de tesis):")
    print(f"  Detectados: {core_detected} / {len(core_results)} ({core_detected/len(core_results)*100:.1f}%)")
    print(f"CONJUNTO AMPLIADO C7 (10 ítems adicionales):")
    print(f"  Detectados: {ext_detected} / {len(ext_results)} ({ext_detected/len(ext_results)*100:.1f}%)")
    print(f"TOTAL GLOBAL:")
    print(f"  Detectados: {core_detected + ext_detected} / {len(results)} ({(core_detected + ext_detected)/len(results)*100:.1f}%)")
    print("=" * 70)

    if args.salida_json:
        with open(args.salida_json, "w", encoding="utf-8") as f:
            json.dump({
                "reporte": args.reporte_csv,
                "total_hallazgos_reporte": total_findings,
                "core_detectados": core_detected,
                "core_total": len(core_results),
                "ampliado_detectados": ext_detected,
                "ampliado_total": len(ext_results),
                "detalles": results
            }, f, indent=2)
        print(f"Resultados guardados en JSON: {args.salida_json}")

    if args.salida_csv:
        with open(args.salida_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
            writer.writeheader()
            writer.writerows(results)
        print(f"Resultados guardados en CSV: {args.salida_csv}")

if __name__ == "__main__":
    main()

