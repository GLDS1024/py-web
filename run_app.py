import subprocess
import sys

if __name__ == "__main__":
    # 运行 Streamlit 应用
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
