import subprocess
import sys
import os

# 确保路径正确
base_dir = os.path.dirname(__file__)
app_path = os.path.join(base_dir, "app.py")

subprocess.run([
    sys.executable, "-m", "streamlit", "run", app_path,
    "--server.port", "8501"
])