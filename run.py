import subprocess,sys
raise SystemExit(subprocess.call([sys.executable,"-m","streamlit","run","app/main.py"]))
