import os
import streamlit.web.cli as stcli
import sys

def main():
    os.chdir(os.path.dirname(__file__))
    sys.argv = ["streamlit", "run", "app.py", "--global.developmentMode=false"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()