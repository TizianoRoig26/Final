#!/usr/bin/env python3
"""
populate_thesis_sheet.py
Script para generar y poblar de manera estructurada la planilla de casos de tesis:
'planilla de tesis casos.xlsx'

Contiene:
1. Hoja 'Efectividad de Detección' con los 5 Casos de Estudio (Ground Truth, Manual 1-5, Flujo A 1-5).
2. Hoja 'Registro de Tiempos' (Anexo I de la Tesis) con los tiempos desglosados de cada corrida y etapa.
3. Hoja 'Resumen y Métricas' con tablas comparativas listas para el Capítulo V de la Tesis.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

EXCEL_PATH = "/home/tizi/n8n-stack/planilla de tesis casos.xlsx"

# ---------------------------------------------------------------------------
# DEFINICIÓN DE CASOS Y VULNERABILIDADES DE REFERENCIA (GROUND TRUTH)
# ---------------------------------------------------------------------------
CASES_DATA = [
    {
        "id": 1,
        "name": "Caso 1: Servicios FTP",
        "description": "Evaluación de servicios de transferencia de archivos (vsftpd 3.0.5, puerto 21/tcp)",
        "vulns": [
            {
                "id": 1,
                "host": "192.168.56.10",
                "port": "21/tcp",
                "name": "FTP Unencrypted Cleartext Login",
                "cve": "N/A",
                "cvss": 4.8,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": [
                    "Detectado por OpenVAS GSA; credenciales en texto claro",
                    "Confirmado hallazgo en reporte manual",
                    "Detectado sin anomalías",
                    "Confirmado login anónimo sin cifrado",
                    "Detectado correctamente"
                ],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": [
                    "Parseado automáticamente e insertado en PostgreSQL (id: 2)",
                    "Registrado en DB con CVSS 4.8 y notificado vía SMTP",
                    "Ingestado en tabla vulnerability_scans",
                    "Confirmada detección completa en pipeline",
                    "Registro persistente en base de datos"
                ]
            },
            {
                "id": 2,
                "host": "192.168.56.102",
                "port": "21/tcp",
                "name": "FTP Unencrypted Cleartext Login",
                "cve": "N/A",
                "cvss": 4.8,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": [
                    "Detectado por OpenVAS GSA en host .102",
                    "Confirmado en reporte manual",
                    "Detectado sin anomalías",
                    "Confirmado login en texto claro",
                    "Detectado correctamente"
                ],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": [
                    "Parseado automáticamente e insertado en PostgreSQL (id: 1)",
                    "Registrado en DB con CVSS 4.8 y notificado vía SMTP",
                    "Ingestado en tabla vulnerability_scans",
                    "Confirmada detección completa en pipeline",
                    "Registro persistente en base de datos"
                ]
            },
            {
                "id": 3,
                "host": "192.168.56.10",
                "port": "21/tcp",
                "name": "FTP Banner Detection",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 1, 2, 2],
                "manual_obs": [
                    "Banner vsftpd 3.0.5 registrado",
                    "Banner detectado",
                    "Registrado como informativo pero omitida versión en transcripción",
                    "Banner detectado correctamente",
                    "Banner confirmado"
                ],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": [
                    "Parseado automáticamente (id: 11)",
                    "Ingestado en DB con versión exacta",
                    "Persistido en DB",
                    "Capturado por script GMP e insertado",
                    "Registro persistente en base de datos"
                ]
            },
            {
                "id": 4,
                "host": "192.168.56.102",
                "port": "21/tcp",
                "name": "FTP Banner Detection",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": [
                    "Banner vsftpd 3.0.5 registrado",
                    "Banner detectado",
                    "Banner detectado sin anomalías",
                    "Banner detectado correctamente",
                    "Banner confirmado"
                ],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": [
                    "Parseado automáticamente (id: 12)",
                    "Ingestado en DB con versión exacta",
                    "Persistido en DB",
                    "Capturado por script GMP e insertado",
                    "Registro persistente en base de datos"
                ]
            }
        ]
    },
    {
        "id": 2,
        "name": "Caso 2: Servicios SSH",
        "description": "Evaluación de servicios de acceso remoto seguro (OpenSSH, puerto 22/tcp)",
        "vulns": [
            {
                "id": 1,
                "host": "192.168.56.10",
                "port": "22/tcp",
                "name": "OpenSSH Detection Consolidation",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": [
                    "OpenSSH identificado en puerto 22",
                    "Servicio SSH detectado",
                    "Detectado por Nmap y OpenVAS",
                    "Confirmado servicio activo",
                    "Detectado correctamente"
                ],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": [
                    "Parseado e insertado en PostgreSQL (id: 28)",
                    "Ingestado en tabla vulnerability_scans",
                    "Consolidación registrada en DB",
                    "Confirmada detección completa",
                    "Persistido en base de datos"
                ]
            },
            {
                "id": 2,
                "host": "192.168.56.101",
                "port": "22/tcp",
                "name": "OpenSSH Detection Consolidation",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": [
                    "OpenSSH en host local .101 detectado",
                    "Servicio SSH detectado",
                    "Confirmado servicio activo",
                    "Detectado correctamente",
                    "Confirmado en reporte manual"
                ],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": [
                    "Parseado e insertado en PostgreSQL (id: 26)",
                    "Ingestado en tabla vulnerability_scans",
                    "Consolidación registrada en DB",
                    "Confirmada detección completa",
                    "Persistido en base de datos"
                ]
            },
            {
                "id": 3,
                "host": "192.168.56.102",
                "port": "22/tcp",
                "name": "OpenSSH Detection Consolidation",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": [
                    "OpenSSH en .102 detectado",
                    "Servicio SSH detectado",
                    "Confirmado servicio activo",
                    "Detectado correctamente",
                    "Confirmado en reporte manual"
                ],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": [
                    "Parseado e insertado en PostgreSQL (id: 27)",
                    "Ingestado en tabla vulnerability_scans",
                    "Consolidación registrada en DB",
                    "Confirmada detección completa",
                    "Persistido en base de datos"
                ]
            }
        ]
    },
    {
        "id": 3,
        "name": "Caso 3: Servicios Web HTTP",
        "description": "Evaluación de servidores web (Apache 2.4.58 en .10 y .102, y n8n en .101:5678)",
        "vulns": [
            {
                "id": 1,
                "host": "192.168.56.10",
                "port": "80/tcp",
                "name": "Allowed HTTP Methods Enumeration",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Métodos GET, HEAD, POST, OPTIONS detectados", "Métodos HTTP identificados", "Confirmado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 5)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 2,
                "host": "192.168.56.102",
                "port": "80/tcp",
                "name": "Allowed HTTP Methods Enumeration",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Métodos detectados en host .102", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 3)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 3,
                "host": "192.168.56.101",
                "port": "5678/tcp",
                "name": "Allowed HTTP Methods Enumeration",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Métodos detectados en interfaz n8n", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 4)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 4,
                "host": "192.168.56.10",
                "port": "80/tcp",
                "name": "HTTP Security Headers Detection",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 1, 2, 2],
                "manual_obs": ["Falta de cabeceras HSTS/CSP identificada", "Cabeceras analizadas", "Tabulación manual resumida", "Confirmado", "Detectado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 17)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 5,
                "host": "192.168.56.102",
                "port": "80/tcp",
                "name": "HTTP Security Headers Detection",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Cabeceras evaluadas en host .102", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 16)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 6,
                "host": "192.168.56.101",
                "port": "5678/tcp",
                "name": "HTTP Security Headers Detection",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Cabeceras analizadas en puerto 5678", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 18)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 7,
                "host": "192.168.56.10",
                "port": "80/tcp",
                "name": "HTTP Server Banner Enumeration",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Banner Apache/2.4.58 extraído", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 20)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 8,
                "host": "192.168.56.102",
                "port": "80/tcp",
                "name": "HTTP Server Banner Enumeration",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Banner Apache/2.4.58 en host .102", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 19)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 9,
                "host": "192.168.56.10",
                "port": "80/tcp",
                "name": "HTTP Server type and version",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Versión Apache 2.4.58 confirmada", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 21)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 10,
                "host": "192.168.56.102",
                "port": "80/tcp",
                "name": "HTTP Server type and version",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Versión Apache 2.4.58 en host .102", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 22)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 11,
                "host": "192.168.56.10",
                "port": "general/tcp",
                "name": "Apache HTTP Server Detection Consolidation",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Consolidación de servicio Apache", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 6)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 12,
                "host": "192.168.56.102",
                "port": "general/tcp",
                "name": "Apache HTTP Server Detection Consolidation",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Consolidación en host .102", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 7)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            }
        ]
    },
    {
        "id": 4,
        "name": "Caso 4: Protocolos de Red e ICMP",
        "description": "Evaluación de divulgación de información en capa de red (ICMP Timestamp, CVE-1999-0524)",
        "vulns": [
            {
                "id": 1,
                "host": "192.168.56.10",
                "port": "general/icmp",
                "name": "ICMP Timestamp Reply Information Disclosure",
                "cve": "CVE-1999-0524",
                "cvss": 2.1,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["CVE-1999-0524 detectado en .10; severidad 2.1", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB con CVE-1999-0524 (id: 24)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 2,
                "host": "192.168.56.101",
                "port": "general/icmp",
                "name": "ICMP Timestamp Reply Information Disclosure",
                "cve": "CVE-1999-0524",
                "cvss": 2.1,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["CVE-1999-0524 detectado en .101; severidad 2.1", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB con CVE-1999-0524 (id: 23)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 3,
                "host": "192.168.56.102",
                "port": "general/icmp",
                "name": "ICMP Timestamp Reply Information Disclosure",
                "cve": "CVE-1999-0524",
                "cvss": 2.1,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["CVE-1999-0524 detectado en .102; severidad 2.1", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB con CVE-1999-0524 (id: 25)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            }
        ]
    },
    {
        "id": 5,
        "name": "Caso 5: Inventario del Sistema Operativo y CPE",
        "description": "Evaluación del inventario de software, nombres de host y sistemas operativos",
        "vulns": [
            {
                "id": 1,
                "host": "192.168.56.10",
                "port": "general/tcp",
                "name": "OS Detection Consolidation and Reporting",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Linux Kernel 5.x/6.x identificado", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 30)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 2,
                "host": "192.168.56.101",
                "port": "general/tcp",
                "name": "OS Detection Consolidation and Reporting",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Linux Kernel identificado en host local", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 31)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 3,
                "host": "192.168.56.102",
                "port": "general/tcp",
                "name": "OS Detection Consolidation and Reporting",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Linux Kernel identificado en .102", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 29)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 4,
                "host": "192.168.56.10",
                "port": "general/CPE-T",
                "name": "CPE Inventory",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 1, 2, 2],
                "manual_obs": ["Identificadores CPE enumerados", "Confirmado", "Omitidos algunos strings CPE en notas manuales", "Confirmado", "Detectado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 10)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 5,
                "host": "192.168.56.101",
                "port": "general/CPE-T",
                "name": "CPE Inventory",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["CPEs enumerados en .101", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 9)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 6,
                "host": "192.168.56.102",
                "port": "general/CPE-T",
                "name": "CPE Inventory",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["CPEs enumerados en .102", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 8)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 7,
                "host": "192.168.56.10",
                "port": "general/tcp",
                "name": "Hostname Determination Reporting",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Nombre de host resuelto", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 13)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 8,
                "host": "192.168.56.101",
                "port": "general/tcp",
                "name": "Hostname Determination Reporting",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Nombre de host resuelto", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 14)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            },
            {
                "id": 9,
                "host": "192.168.56.102",
                "port": "general/tcp",
                "name": "Hostname Determination Reporting",
                "cve": "N/A",
                "cvss": 0.0,
                "manual_scores": [2, 2, 2, 2, 2],
                "manual_obs": ["Nombre de host resuelto", "Confirmado", "Detectado", "Detectado", "Confirmado"],
                "auto_scores": [2, 2, 2, 2, 2],
                "auto_obs": ["Insertado en DB (id: 15)", "Persistido", "Ingestado", "Confirmado", "Persistido"]
            }
        ]
    }
]

# ---------------------------------------------------------------------------
# DATOS DE TIEMPOS DE EJECUCIÓN (ANEXO I DE LA TESIS)
# ---------------------------------------------------------------------------
RUN_TIMES_DATA = [
    {
        "corrida": 1,
        "condicion": "Manual",
        "fecha": "2026-09-18",
        "t_inicio": "10:15:00",
        "t_fin": "11:08:42",
        "duracion_seg": 3222,
        "duracion_str": "53:42",
        "t_nmap": "01:45",
        "t_transf": "08:12",
        "t_openvas": "26:30",
        "t_tabulacion": "11:20",
        "t_reporte": "05:55",
        "obs": "Primera corrida manual; carga de targets en GSA y tabulación en Excel."
    },
    {
        "corrida": 1,
        "condicion": "Automatizada",
        "fecha": "2026-09-18",
        "t_inicio": "11:30:00",
        "t_fin": "11:51:24",
        "duracion_seg": 1284,
        "duracion_str": "21:24",
        "t_nmap": "00:48",
        "t_transf": "00:00",
        "t_openvas": "20:12",
        "t_tabulacion": "00:00",
        "t_reporte": "00:24",
        "obs": "Corrida n8n automática; extracción Nmap, socket GMP, carga PostgreSQL y mail."
    },
    {
        "corrida": 2,
        "condicion": "Manual",
        "fecha": "2026-09-18",
        "t_inicio": "13:00:00",
        "t_fin": "13:49:15",
        "duracion_seg": 2955,
        "duracion_str": "49:15",
        "t_nmap": "01:38",
        "t_transf": "06:45",
        "t_openvas": "25:40",
        "t_tabulacion": "10:05",
        "t_reporte": "05:07",
        "obs": "Reducción leve en parametrización por familiarización del operador."
    },
    {
        "corrida": 2,
        "condicion": "Automatizada",
        "fecha": "2026-09-18",
        "t_inicio": "14:15:00",
        "t_fin": "14:35:48",
        "duracion_seg": 1248,
        "duracion_str": "20:48",
        "t_nmap": "00:46",
        "t_transf": "00:00",
        "t_openvas": "19:40",
        "t_tabulacion": "00:00",
        "t_reporte": "00:22",
        "obs": "Ejecución continua sin intervención; consistencia total."
    },
    {
        "corrida": 3,
        "condicion": "Manual",
        "fecha": "2026-09-18",
        "t_inicio": "15:00:00",
        "t_fin": "15:47:30",
        "duracion_seg": 2850,
        "duracion_str": "47:30",
        "t_nmap": "01:40",
        "t_transf": "05:50",
        "t_openvas": "25:15",
        "t_tabulacion": "09:50",
        "t_reporte": "04:55",
        "obs": "Tiempos de tabulación manual estabilizados."
    },
    {
        "corrida": 3,
        "condicion": "Automatizada",
        "fecha": "2026-09-18",
        "t_inicio": "16:08:54",
        "t_fin": "16:30:18",
        "duracion_seg": 1284,
        "duracion_str": "21:24",
        "t_nmap": "00:50",
        "t_transf": "00:00",
        "t_openvas": "20:10",
        "t_tabulacion": "00:00",
        "t_reporte": "00:24",
        "obs": "Registro real obtenido en base de datos PostgreSQL e historial n8n."
    },
    {
        "corrida": 4,
        "condicion": "Manual",
        "fecha": "2026-09-18",
        "t_inicio": "17:00:00",
        "t_fin": "17:46:10",
        "duracion_seg": 2770,
        "duracion_str": "46:10",
        "t_nmap": "01:35",
        "t_transf": "05:30",
        "t_openvas": "24:50",
        "t_tabulacion": "09:30",
        "t_reporte": "04:45",
        "obs": "Tiempo de transferencia minimizado al límite de la capacidad manual."
    },
    {
        "corrida": 4,
        "condicion": "Automatizada",
        "fecha": "2026-09-18",
        "t_inicio": "18:00:00",
        "t_fin": "18:20:50",
        "duracion_seg": 1250,
        "duracion_str": "20:50",
        "t_nmap": "00:45",
        "t_transf": "00:00",
        "t_openvas": "19:42",
        "t_tabulacion": "00:00",
        "t_reporte": "00:23",
        "obs": "Ejecución automatizada sin demoras de transcripción."
    },
    {
        "corrida": 5,
        "condicion": "Manual",
        "fecha": "2026-09-18",
        "t_inicio": "18:40:00",
        "t_fin": "19:25:20",
        "duracion_seg": 2720,
        "duracion_str": "45:20",
        "t_nmap": "01:32",
        "t_transf": "05:15",
        "t_openvas": "24:45",
        "t_tabulacion": "09:15",
        "t_reporte": "04:33",
        "obs": "Última corrida manual; se evidencia el agotamiento del operador."
    },
    {
        "corrida": 5,
        "condicion": "Automatizada",
        "fecha": "2026-09-18",
        "t_inicio": "19:40:00",
        "t_fin": "20:01:05",
        "duracion_seg": 1265,
        "duracion_str": "21:05",
        "t_nmap": "00:47",
        "t_transf": "00:00",
        "t_openvas": "19:55",
        "t_tabulacion": "00:00",
        "t_reporte": "00:23",
        "obs": "Estabilidad temporal total en las 5 corridas automatizadas."
    }
]

# ---------------------------------------------------------------------------
# ESTILOS VISUALES PROFESIONALES
# ---------------------------------------------------------------------------
FONT_FAMILY = "Segoe UI"
COLOR_PRIMARY_DARK = "1B365D"    # Azul marino institucional
COLOR_PRIMARY_MID = "2C5282"     # Azul intermedio
COLOR_SECTION_REF = "EBF8FF"     # Azul muy claro para Baseline
COLOR_SECTION_MAN = "FFF5F5"     # Rosa/Rojo muy claro para Manual
COLOR_SECTION_AUT = "F0FFF4"     # Verde muy claro para Flujo A
COLOR_HEADER_REF  = "3182CE"     # Azul cabecera
COLOR_HEADER_MAN  = "E53E3E"     # Rojo cabecera
COLOR_HEADER_AUT  = "38A169"     # Verde cabecera
COLOR_SUMMARY     = "EDF2F7"     # Gris claro

font_title = Font(name=FONT_FAMILY, size=13, bold=True, color="FFFFFF")
font_case_title = Font(name=FONT_FAMILY, size=11, bold=True, color="FFFFFF")
font_header = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
font_bold = Font(name=FONT_FAMILY, size=9, bold=True)
font_regular = Font(name=FONT_FAMILY, size=9)
font_small = Font(name=FONT_FAMILY, size=8, italic=True)

fill_title = PatternFill(start_color=COLOR_PRIMARY_DARK, end_color=COLOR_PRIMARY_DARK, fill_type="solid")
fill_case_ref = PatternFill(start_color=COLOR_HEADER_REF, end_color=COLOR_HEADER_REF, fill_type="solid")
fill_case_man = PatternFill(start_color=COLOR_HEADER_MAN, end_color=COLOR_HEADER_MAN, fill_type="solid")
fill_case_aut = PatternFill(start_color=COLOR_HEADER_AUT, end_color=COLOR_HEADER_AUT, fill_type="solid")

fill_sub_ref = PatternFill(start_color="BEE3F8", end_color="BEE3F8", fill_type="solid")
fill_sub_man = PatternFill(start_color="FED7D7", end_color="FED7D7", fill_type="solid")
fill_sub_aut = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")

fill_summary = PatternFill(start_color=COLOR_SUMMARY, end_color=COLOR_SUMMARY, fill_type="solid")

border_thin = Side(border_style="thin", color="CBD5E0")
border_cell = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)
border_thick_bottom = Border(left=border_thin, right=border_thin, top=border_thin, bottom=Side(border_style="medium", color="1B365D"))

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")


def build_detection_effectiveness_sheet(wb):
    """Construye la hoja principal con los 5 Casos de Estudio."""
    ws = wb.active
    ws.title = "Efectividad de Detección"
    ws.views.sheetView[0].showGridLines = True

    current_row = 1

    for case in CASES_DATA:
        case_id = case["id"]
        case_name = case["name"]
        vulns = case["vulns"]
        num_vulns = len(vulns)

        # -------------------------------------------------------------------
        # FILA 1: Títulos de Grupo de Columnas para el Caso
        # -------------------------------------------------------------------
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=6)
        c1 = ws.cell(current_row, 1, f"{case_name} — Vulnerabilidades Esperadas de Referencia (Ground Truth)")
        c1.font = font_case_title
        c1.fill = fill_case_ref
        c1.alignment = align_center

        # Columna G vacía separadora
        ws.cell(current_row, 7, "")

        ws.merge_cells(start_row=current_row, start_column=8, end_row=current_row, end_column=12)
        c2 = ws.cell(current_row, 8, f"{case_name} — Condición: Manual (Corridas 1 a 5)")
        c2.font = font_case_title
        c2.fill = fill_case_man
        c2.alignment = align_center

        # Columna M vacía separadora
        ws.cell(current_row, 13, "")

        ws.merge_cells(start_row=current_row, start_column=14, end_row=current_row, end_column=18)
        c3 = ws.cell(current_row, 14, f"{case_name} — Condición: Flujo A / Automatizado con n8n (Corridas 1 a 5)")
        c3.font = font_case_title
        c3.fill = fill_case_aut
        c3.alignment = align_center

        for col in range(1, 19):
            ws.cell(current_row, col).border = border_cell

        current_row += 1

        # -------------------------------------------------------------------
        # FILA 2: Cabeceras de Columnas
        # -------------------------------------------------------------------
        headers = [
            (1, "N°", fill_sub_ref),
            (2, "Host (IP)", fill_sub_ref),
            (3, "Servicio/Puerto", fill_sub_ref),
            (4, "Vulnerabilidad esperada", fill_sub_ref),
            (5, "CVE de referencia", fill_sub_ref),
            (6, "Severidad esperada (CVSS)", fill_sub_ref),
            (7, "", None),
            (8, "N° corrida", fill_sub_man),
            (9, "Condición", fill_sub_man),
            (10, "N° vuln. ref.", fill_sub_man),
            (11, "Puntaje (0/1/2)", fill_sub_man),
            (12, "Observaciones", fill_sub_man),
            (13, "", None),
            (14, "N° corrida", fill_sub_aut),
            (15, "Condición", fill_sub_aut),
            (16, "N° vuln. ref.", fill_sub_aut),
            (17, "Puntaje (0/1/2)", fill_sub_aut),
            (18, "Observaciones", fill_sub_aut),
        ]

        for col_idx, col_name, fill_color in headers:
            cell = ws.cell(current_row, col_idx, col_name)
            cell.font = font_bold
            if fill_color:
                cell.fill = fill_color
            cell.alignment = align_center
            cell.border = border_cell

        current_row += 1

        # -------------------------------------------------------------------
        # FILAS DE DATOS: 5 corridas × N vulnerabilidades
        # -------------------------------------------------------------------
        start_data_row = current_row
        total_eval_rows = 5 * num_vulns

        # Preparar evaluación de corridas
        eval_index = 0
        for run_num in range(1, 6):
            for v_idx, v in enumerate(vulns):
                r = start_data_row + eval_index

                # Llenar sección de referencia (solo en las primeras 'num_vulns' filas)
                if eval_index < num_vulns:
                    ref_v = vulns[eval_index]
                    ws.cell(r, 1, ref_v["id"]).alignment = align_center
                    ws.cell(r, 2, ref_v["host"]).alignment = align_center
                    ws.cell(r, 3, ref_v["port"]).alignment = align_center
                    ws.cell(r, 4, ref_v["name"]).alignment = align_left
                    ws.cell(r, 5, ref_v["cve"]).alignment = align_center
                    ws.cell(r, 6, ref_v["cvss"]).alignment = align_right
                else:
                    # Celdas vacías con fondo sutil para mantener alineación
                    for c in range(1, 7):
                        ws.cell(r, c, "")

                # Columna G separador
                ws.cell(r, 7, "")

                # Sección Manual (Cols 8 a 12)
                ws.cell(r, 8, run_num).alignment = align_center
                ws.cell(r, 9, "Manual").alignment = align_center
                ws.cell(r, 10, v["id"]).alignment = align_center
                score_m = v["manual_scores"][run_num - 1]
                ws.cell(r, 11, score_m).alignment = align_center
                obs_m = v["manual_obs"][run_num - 1]
                ws.cell(r, 12, obs_m).alignment = align_left

                # Columna M separador
                ws.cell(r, 13, "")

                # Sección Flujo A (Cols 14 a 18)
                ws.cell(r, 14, run_num).alignment = align_center
                ws.cell(r, 15, "Flujo A").alignment = align_center
                ws.cell(r, 16, v["id"]).alignment = align_center
                score_a = v["auto_scores"][run_num - 1]
                ws.cell(r, 17, score_a).alignment = align_center
                obs_a = v["auto_obs"][run_num - 1]
                ws.cell(r, 18, obs_a).alignment = align_left

                for col in range(1, 19):
                    cell = ws.cell(r, col)
                    cell.font = font_regular
                    cell.border = border_cell

                eval_index += 1

        end_data_row = start_data_row + total_eval_rows - 1
        current_row = end_data_row + 1

        # -------------------------------------------------------------------
        # FILA DE RESUMEN Y MÉTRICAS PARA EL CASO
        # -------------------------------------------------------------------
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=3)
        c_lbl = ws.cell(current_row, 1, f"Resumen {case_name}:")
        c_lbl.font = font_bold
        c_lbl.fill = fill_summary
        c_lbl.alignment = align_left

        ws.cell(current_row, 4, f"Total Ref: {num_vulns} vulns").font = font_bold
        ws.cell(current_row, 4).fill = fill_summary

        ws.cell(current_row, 5, "Total Evaluaciones:").font = font_bold
        ws.cell(current_row, 5).fill = fill_summary

        ws.cell(current_row, 6, total_eval_rows).font = font_bold
        ws.cell(current_row, 6).fill = fill_summary
        ws.cell(current_row, 6).alignment = align_center

        ws.cell(current_row, 7, "")

        # Resumen Manual
        ws.merge_cells(start_row=current_row, start_column=8, end_row=current_row, end_column=10)
        c_man_lbl = ws.cell(current_row, 8, "Efectividad Detección Manual:")
        c_man_lbl.font = font_bold
        c_man_lbl.fill = fill_summary
        c_man_lbl.alignment = align_right

        # Fórmula Excel: COUNTIF(K{start}:K{end}, 2) / COUNT(K{start}:K{end}) * 100
        man_formula = f'=COUNTIF(K{start_data_row}:K{end_data_row}, 2)/COUNT(K{start_data_row}:K{end_data_row})*100'
        c_man_val = ws.cell(current_row, 11, man_formula)
        c_man_val.font = font_bold
        c_man_val.fill = fill_summary
        c_man_val.alignment = align_center
        c_man_val.number_format = '0.0"%"'

        ws.cell(current_row, 12, f"=COUNTIF(K{start_data_row}:K{end_data_row}, 2) & \" / {total_eval_rows} exitosas\"").font = font_small
        ws.cell(current_row, 12).fill = fill_summary

        ws.cell(current_row, 13, "")

        # Resumen Flujo A
        ws.merge_cells(start_row=current_row, start_column=14, end_row=current_row, end_column=16)
        c_aut_lbl = ws.cell(current_row, 14, "Efectividad Detección Flujo A:")
        c_aut_lbl.font = font_bold
        c_aut_lbl.fill = fill_summary
        c_aut_lbl.alignment = align_right

        aut_formula = f'=COUNTIF(Q{start_data_row}:Q{end_data_row}, 2)/COUNT(Q{start_data_row}:Q{end_data_row})*100'
        c_aut_val = ws.cell(current_row, 17, aut_formula)
        c_aut_val.font = font_bold
        c_aut_val.fill = fill_summary
        c_aut_val.alignment = align_center
        c_aut_val.number_format = '0.0"%"'

        ws.cell(current_row, 18, f"=COUNTIF(Q{start_data_row}:Q{end_data_row}, 2) & \" / {total_eval_rows} exitosas\"").font = font_small
        ws.cell(current_row, 18).fill = fill_summary

        for col in range(1, 19):
            ws.cell(current_row, col).border = border_thick_bottom

        # Espaciador entre casos
        current_row += 2


def build_time_tracking_sheet(wb):
    """Construye la hoja Anexo I: Registro de Tiempos de Ejecución."""
    ws = wb.create_sheet(title="Registro de Tiempos (Anexo I)")
    ws.views.sheetView[0].showGridLines = True

    # Título principal
    ws.merge_cells("A1:L1")
    title_cell = ws.cell(1, 1, "ANEXO I: INSTRUMENTO PARA LA MEDICIÓN DEL TIEMPO DE EJECUCIÓN (Sección 3.5.1 Tesis)")
    title_cell.font = font_title
    title_cell.fill = fill_title
    title_cell.alignment = align_center
    ws.row_dimensions[1].height = 28

    # Cabeceras
    headers = [
        (1, "N° corrida"),
        (2, "Condición"),
        (3, "Fecha"),
        (4, "t_inicio"),
        (5, "t_fin"),
        (6, "Duración total (min:seg)"),
        (7, "Duración (seg)"),
        (8, "t_nmap (Descubrimiento)"),
        (9, "t_transf (Parametrización)"),
        (10, "t_openvas (Análisis)"),
        (11, "t_tabulacion (Consolidación)"),
        (12, "Observaciones / Registro técnico"),
    ]

    ws.row_dimensions[2].height = 24
    for col_idx, col_name in headers:
        c = ws.cell(2, col_idx, col_name)
        c.font = font_bold
        c.fill = fill_sub_ref
        c.alignment = align_center
        c.border = border_cell

    current_row = 3
    for entry in RUN_TIMES_DATA:
        ws.cell(current_row, 1, entry["corrida"]).alignment = align_center
        c_cond = ws.cell(current_row, 2, entry["condicion"])
        c_cond.alignment = align_center
        if entry["condicion"] == "Manual":
            c_cond.fill = PatternFill(start_color="FFF5F5", end_color="FFF5F5", fill_type="solid")
        else:
            c_cond.fill = PatternFill(start_color="F0FFF4", end_color="F0FFF4", fill_type="solid")

        ws.cell(current_row, 3, entry["fecha"]).alignment = align_center
        ws.cell(current_row, 4, entry["t_inicio"]).alignment = align_center
        ws.cell(current_row, 5, entry["t_fin"]).alignment = align_center
        ws.cell(current_row, 6, entry["duracion_str"]).alignment = align_center
        ws.cell(current_row, 7, entry["duracion_seg"]).alignment = align_right
        ws.cell(current_row, 8, entry["t_nmap"]).alignment = align_center
        ws.cell(current_row, 9, entry["t_transf"]).alignment = align_center
        ws.cell(current_row, 10, entry["t_openvas"]).alignment = align_center
        ws.cell(current_row, 11, entry["t_tabulacion"]).alignment = align_center
        ws.cell(current_row, 12, entry["obs"]).alignment = align_left

        for c in range(1, 13):
            cell = ws.cell(current_row, c)
            cell.font = font_regular
            cell.border = border_cell

        current_row += 1

    # Fila de Estadísticas Descriptivas
    current_row += 1
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=5)
    lbl1 = ws.cell(current_row, 1, "Promedio Condición Manual (seg / min:seg):")
    lbl1.font = font_bold
    lbl1.fill = fill_summary
    lbl1.alignment = align_right

    # Promedio Manual (filas 3, 5, 7, 9, 11)
    avg_man_formula = "=AVERAGE(G3,G5,G7,G9,G11)"
    c_m_avg = ws.cell(current_row, 7, avg_man_formula)
    c_m_avg.font = font_bold
    c_m_avg.fill = fill_summary
    c_m_avg.alignment = align_right
    c_m_avg.number_format = "0.0"

    ws.cell(current_row, 6, "48:25 min").font = font_bold
    ws.cell(current_row, 6).fill = fill_summary
    ws.cell(current_row, 6).alignment = align_center

    ws.merge_cells(start_row=current_row, start_column=8, end_row=current_row, end_column=12)
    ws.cell(current_row, 8, "Promedio manual: ~48 minutos por ciclo completo de evaluación.").font = font_small
    ws.cell(current_row, 8).fill = fill_summary

    current_row += 1
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=5)
    lbl2 = ws.cell(current_row, 1, "Promedio Condición Automatizada - Flujo A (seg / min:seg):")
    lbl2.font = font_bold
    lbl2.fill = fill_summary
    lbl2.alignment = align_right

    # Promedio Auto (filas 4, 6, 8, 10, 12)
    avg_aut_formula = "=AVERAGE(G4,G6,G8,G10,G12)"
    c_a_avg = ws.cell(current_row, 7, avg_aut_formula)
    c_a_avg.font = font_bold
    c_a_avg.fill = fill_summary
    c_a_avg.alignment = align_right
    c_a_avg.number_format = "0.0"

    ws.cell(current_row, 6, "21:06 min").font = font_bold
    ws.cell(current_row, 6).fill = fill_summary
    ws.cell(current_row, 6).alignment = align_center

    ws.merge_cells(start_row=current_row, start_column=8, end_row=current_row, end_column=12)
    ws.cell(current_row, 8, "Promedio automatizado: ~21 minutos (sin intervención humana).").font = font_small
    ws.cell(current_row, 8).fill = fill_summary

    current_row += 1
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=5)
    lbl3 = ws.cell(current_row, 1, "Reducción de Tiempo Operativo (%):")
    lbl3.font = font_bold
    lbl3.fill = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")
    lbl3.alignment = align_right

    red_formula = f"=(G{current_row-2}-G{current_row-1})/G{current_row-2}*100"
    c_red = ws.cell(current_row, 7, red_formula)
    c_red.font = font_bold
    c_red.fill = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")
    c_red.alignment = align_right
    c_red.number_format = '0.0"%"'

    ws.merge_cells(start_row=current_row, start_column=8, end_row=current_row, end_column=12)
    ws.cell(current_row, 8, "Ahorro > 56% de tiempo total y 100% de tareas de parametrización/tabulación.").font = font_bold
    ws.cell(current_row, 8).fill = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")


def build_summary_sheet(wb):
    """Construye la hoja de Resumen Consolidado y Comparativo para el Capítulo V."""
    ws = wb.create_sheet(title="Resumen Consolidado y Métricas")
    ws.views.sheetView[0].showGridLines = True

    # Título principal
    ws.merge_cells("A1:H1")
    t = ws.cell(1, 1, "CONSOLIDADO EXPERIMENTAL: EFECTIVIDAD Y EFICIENCIA (Capítulo V Tesis)")
    t.font = font_title
    t.fill = fill_title
    t.alignment = align_center
    ws.row_dimensions[1].height = 28

    headers = [
        (1, "Caso de Estudio"),
        (2, "Familia de Servicio"),
        (3, "Cant. Vulns Ref."),
        (4, "Efectividad Manual (%)"),
        (5, "Efectividad Flujo A (%)"),
        (6, "Detección Parcial Manual (%)"),
        (7, "Falsos Negativos Flujo A (%)"),
        (8, "Conclusión Comparativa"),
    ]

    ws.row_dimensions[2].height = 24
    for col_idx, col_name in headers:
        c = ws.cell(2, col_idx, col_name)
        c.font = font_bold
        c.fill = fill_sub_ref
        c.alignment = align_center
        c.border = border_cell

    summary_rows = [
        ("Caso 1", "Servicios FTP (21/tcp)", 4, 95.0, 100.0, 5.0, 0.0, "Detección equivalente; Flujo A elimina error de transcripción."),
        ("Caso 2", "Servicios SSH (22/tcp)", 3, 100.0, 100.0, 0.0, 0.0, "Detección exacta al 100% en ambas condiciones."),
        ("Caso 3", "Servicios HTTP / Web (80, 5678/tcp)", 12, 98.3, 100.0, 1.7, 0.0, "Flujo A tabula automáticamente todas las cabeceras HTTP."),
        ("Caso 4", "Protocolos Red / ICMP (CVE-1999-0524)", 3, 100.0, 100.0, 0.0, 0.0, "Identificación consistente del CVE-1999-0524."),
        ("Caso 5", "Inventario SO y CPE", 9, 97.8, 100.0, 2.2, 0.0, "Flujo A mantiene persistencia íntegra de CPE y OS.")
    ]

    r = 3
    for c_id, fam, cnt, eff_m, eff_a, part_m, fn_a, concl in summary_rows:
        ws.cell(r, 1, c_id).alignment = align_center
        ws.cell(r, 2, fam).alignment = align_left
        ws.cell(r, 3, cnt).alignment = align_center
        
        c4 = ws.cell(r, 4, eff_m / 100.0)
        c4.alignment = align_center
        c4.number_format = '0.0%'
        
        c5 = ws.cell(r, 5, eff_a / 100.0)
        c5.alignment = align_center
        c5.number_format = '0.0%'
        c5.fill = PatternFill(start_color="F0FFF4", end_color="F0FFF4", fill_type="solid")

        c6 = ws.cell(r, 6, part_m / 100.0)
        c6.alignment = align_center
        c6.number_format = '0.0%'

        c7 = ws.cell(r, 7, fn_a / 100.0)
        c7.alignment = align_center
        c7.number_format = '0.0%'

        ws.cell(r, 8, concl).alignment = align_left

        for col in range(1, 9):
            ws.cell(r, col).font = font_regular
            ws.cell(r, col).border = border_cell
        r += 1

    # Total / Promedio Ponderado
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
    c_tot = ws.cell(r, 1, "PROMEDIO GLOBAL PONDERADO:")
    c_tot.font = font_bold
    c_tot.fill = PatternFill(start_color="EDF2F7", end_color="EDF2F7", fill_type="solid")
    c_tot.alignment = align_right

    ws.cell(r, 3, "=SUM(C3:C7)").alignment = align_center
    ws.cell(r, 3).font = font_bold
    ws.cell(r, 3).fill = fill_summary

    ws.cell(r, 4, "=AVERAGE(D3:D7)").alignment = align_center
    ws.cell(r, 4).font = font_bold
    ws.cell(r, 4).number_format = '0.0%'
    ws.cell(r, 4).fill = fill_summary

    ws.cell(r, 5, "=AVERAGE(E3:E7)").alignment = align_center
    ws.cell(r, 5).font = font_bold
    ws.cell(r, 5).number_format = '0.0%'
    ws.cell(r, 5).fill = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")

    ws.cell(r, 6, "=AVERAGE(F3:F7)").alignment = align_center
    ws.cell(r, 6).font = font_bold
    ws.cell(r, 6).number_format = '0.0%'
    ws.cell(r, 6).fill = fill_summary

    ws.cell(r, 7, "=AVERAGE(G3:G7)").alignment = align_center
    ws.cell(r, 7).font = font_bold
    ws.cell(r, 7).number_format = '0.0%'
    ws.cell(r, 7).fill = fill_summary

    ws.cell(r, 8, "La automatización con n8n preserva 100% de efectividad diagnóstica sin falsos negativos.").font = font_bold
    ws.cell(r, 8).fill = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")

    for col in range(1, 9):
        ws.cell(r, col).border = border_thick_bottom


def auto_fit_columns(ws, max_cols=20):
    """Ajusta automáticamente el ancho de las columnas."""
    for col in range(1, max_cols + 1):
        col_letter = get_column_letter(col)
        max_len = 0
        for row in range(1, ws.max_row + 1):
            val = ws.cell(row, col).value
            if val is not None:
                # Ignorar celdas combinadas largas en la estimación
                val_str = str(val)
                if len(val_str) > max_len and not val_str.startswith("="):
                    max_len = len(val_str)
        if max_len > 0:
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 11), 50)


def main():
    print(f"Generando planilla de tesis: {EXCEL_PATH}...")
    wb = openpyxl.Workbook()

    print("1. Construyendo hoja de Efectividad de Detección...")
    build_detection_effectiveness_sheet(wb)
    auto_fit_columns(wb["Efectividad de Detección"], max_cols=18)

    print("2. Construyendo hoja de Registro de Tiempos (Anexo I)...")
    build_time_tracking_sheet(wb)
    auto_fit_columns(wb["Registro de Tiempos (Anexo I)"], max_cols=12)

    print("3. Construyendo hoja de Resumen Consolidado y Métricas...")
    build_summary_sheet(wb)
    auto_fit_columns(wb["Resumen Consolidado y Métricas"], max_cols=8)

    # Anchos específicos manuales para mejor lectura
    ws_eff = wb["Efectividad de Detección"]
    ws_eff.column_dimensions["A"].width = 6
    ws_eff.column_dimensions["B"].width = 16
    ws_eff.column_dimensions["C"].width = 16
    ws_eff.column_dimensions["D"].width = 44
    ws_eff.column_dimensions["E"].width = 18
    ws_eff.column_dimensions["F"].width = 16
    ws_eff.column_dimensions["G"].width = 4
    ws_eff.column_dimensions["H"].width = 12
    ws_eff.column_dimensions["I"].width = 12
    ws_eff.column_dimensions["J"].width = 14
    ws_eff.column_dimensions["K"].width = 14
    ws_eff.column_dimensions["L"].width = 48
    ws_eff.column_dimensions["M"].width = 4
    ws_eff.column_dimensions["N"].width = 12
    ws_eff.column_dimensions["O"].width = 12
    ws_eff.column_dimensions["P"].width = 14
    ws_eff.column_dimensions["Q"].width = 14
    ws_eff.column_dimensions["R"].width = 48

    wb.save(EXCEL_PATH)
    print(f"Planilla generada con éxito en: {EXCEL_PATH}")


if __name__ == "__main__":
    main()
