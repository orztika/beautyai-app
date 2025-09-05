from app import main
import streamlit.web.cli as stcli
import sys

def run_streamlit():
    """运行Streamlit应用"""
    sys.argv = ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    stcli.main()

if __name__ == "__main__":
    run_streamlit()