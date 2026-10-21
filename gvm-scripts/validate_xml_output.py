#!/usr/bin/env python3
"""
validate_xml_output.py
Valida que el XML generado por automated_scan.gmp.py sea parseable
y extrae un resumen de vulnerabilidades.
Uso: python3 validate_xml_output.py < scan_output.xml
      cat scan.xml | python3 validate_xml_output.py
"""
import sys
import re

xml_data = sys.stdin.read()

print(f"[VALIDACION] Bytes recibidos: {len(xml_data)}")

if not xml_data.strip():
    print("[ERROR] stdin vacio. No hay XML.")
    sys.exit(1)

if not xml_data.strip().startswith('<'):
    print("[ERROR] El contenido no empieza con '<'. No es XML.")
    print(f"  Primeros 200 chars: {xml_data[:200]!r}")
    sys.exit(1)

# Intentar parsear con lxml
try:
    import lxml.etree as etree
    root = etree.fromstring(xml_data.encode('utf-8'))
    print(f"[OK] lxml parseo exitoso. Root tag: {root.tag}")
except Exception as e:
    print(f"[WARN] lxml fallo: {e}. Intentando con regex...")

# Extraer resultados con regex (como lo hace n8n)
result_blocks = re.findall(r'<result[^>]*>[\s\S]*?</result>', xml_data)
print(f"[INFO] Bloques <result> encontrados: {len(result_blocks)}")

vulns = []
for block in result_blocks:
    name_m    = re.search(r'<name>([^<]*)</name>', block)
    sev_m     = re.search(r'<severity>([^<]*)</severity>', block)
    host_m    = re.search(r'<host[^>]*>([\s\S]*?)</host>', block)
    port_m    = re.search(r'<port>([^<]*)</port>', block)
    cve_ref_m = re.search(r'<ref[^>]+type=["\']cve["\'][^>]+id=["\']([^"\']+)["\']', block)
    cve_leg_m = re.search(r'<cve>([^<]+)</cve>', block)
    threat_m  = re.search(r'<threat>([^<]*)</threat>', block)

    sev = float(sev_m.group(1)) if sev_m else 0
    if sev > 0:
        host_raw = host_m.group(1).strip() if host_m else 'Unknown'
        host_raw = re.sub(r'<[^>]+>', '', host_raw).strip()
        cve = cve_ref_m.group(1) if cve_ref_m else (cve_leg_m.group(1) if cve_leg_m else 'N/A')
        vulns.append({
            'name':    name_m.group(1).strip() if name_m else 'Unknown',
            'sev':     sev,
            'host':    host_raw,
            'port':    port_m.group(1).strip() if port_m else '',
            'cve':     cve.strip(),
            'threat':  threat_m.group(1).strip() if threat_m else 'Log'
        })

print(f"\n[RESUMEN] Vulnerabilidades (severidad > 0): {len(vulns)}")

by_threat = {}
for v in vulns:
    by_threat.setdefault(v['threat'], []).append(v)

for threat in ['Critical', 'High', 'Medium', 'Low', 'Log']:
    grp = by_threat.get(threat, [])
    if grp:
        print(f"  {threat}: {len(grp)}")

print("\n[TOP 5 por severidad]")
for v in sorted(vulns, key=lambda x: x['sev'], reverse=True)[:5]:
    print(f"  [{v['sev']:5.1f}] {v['threat']:8s} {v['host']:20s}:{v['port']:10s} CVE:{v['cve']} - {v['name'][:60]}")

print("\n[OK] Validacion completa.")
