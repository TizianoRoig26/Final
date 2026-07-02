import sys
import time
from lxml import etree
from gvm.protocols.gmp import Gmp


def main(gmp: Gmp, args):
    if len(args.script) < 2:
        print("ERROR: falta el rango de red como argumento")
        sys.exit(1)

    target_hosts = args.script[1]
    port_list_id = "33d0cd82-57c6-11e1-8ed1-406186ea4fc5"

    target_name = f"Auto-Target-{int(time.time())}"
    res = gmp.create_target(
        name=target_name,
        hosts=[target_hosts],
        port_list_id=port_list_id
    )
    target_id = res.get("id")
    print(f"DEBUG: target_id={target_id}", file=sys.stderr)

    scan_config_id = "daba56c8-73ec-11df-a475-002264764cea"
    scanner_id = "08b69003-5fc2-4037-a479-93b440211c73"

    task_name = f"Automated-Scan-{int(time.time())}"
    res = gmp.create_task(
        name=task_name,
        config_id=scan_config_id,
        target_id=target_id,
        scanner_id=scanner_id,
    )
    task_id = res.get("id")
    print(f"DEBUG: task_id={task_id}", file=sys.stderr)

    res = gmp.start_task(task_id)
    report_id = res.xpath("//report_id/text()")[0]
    print(f"DEBUG: report_id={report_id}", file=sys.stderr)

    max_wait_seconds = 1800
    poll_interval = 15
    elapsed = 0

    while elapsed < max_wait_seconds:
        status_res = gmp.get_task(task_id)
        status = status_res.xpath("task/status/text()")[0]
        print(f"DEBUG: status={status} elapsed={elapsed}s", file=sys.stderr)
        if status in ("Done", "Stopped", "Interrupted"):
            break
        time.sleep(poll_interval)
        elapsed += poll_interval
    else:
        print("ADVERTENCIA: timeout alcanzado", file=sys.stderr)

    report_xml = gmp.get_report(report_id, details=True)
    print(etree.tostring(report_xml, pretty_print=False).decode())