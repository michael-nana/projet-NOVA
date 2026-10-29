import json

import psutil

from ..registry import tool


@tool("system_status", "Donne l'état du PC : CPU, mémoire, disque.", level=0)
def system_status() -> str:
    mem, disk = psutil.virtual_memory(), psutil.disk_usage("/")
    return json.dumps({
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram_used_gb": round(mem.used / 1e9, 1), "ram_total_gb": round(mem.total / 1e9, 1),
        "disk_used_gb": round(disk.used / 1e9, 1), "disk_total_gb": round(disk.total / 1e9, 1),
    }, ensure_ascii=False)
