import time

from .. import config
from ..registry import tool


@tool("screen_screenshot", "Prend une capture d'écran du PC et l'enregistre sur le disque.", level=0)
def screen_screenshot() -> str:
    import mss
    import mss.tools

    out_dir = config.DATA_DIR / "screenshots"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{time.strftime('%Y%m%d-%H%M%S')}.png"
    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[1])
        mss.tools.to_png(shot.rgb, shot.size, output=str(path))
    return f"Capture enregistrée : {path}"
