#!/usr/bin/env python3
"""Cross-platform launcher; dependencies and weights must already be installed."""
import os,sys,subprocess,webbrowser,time,threading
from pathlib import Path
root=Path(__file__).resolve().parents[1];os.chdir(root);sys.path.insert(0,str(root))
if '--no-browser' not in sys.argv:
    def open_ui():
        import urllib.request
        for _ in range(60):
            try:
                urllib.request.urlopen('http://127.0.0.1:8765/api/health',timeout=1)
                webbrowser.open('http://127.0.0.1:8765');return
            except Exception:time.sleep(.5)
    threading.Thread(target=open_ui,daemon=True).start()
import uvicorn
uvicorn.run('app:app',host='127.0.0.1',port=8765)
