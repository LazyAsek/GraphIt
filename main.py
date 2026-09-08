import subprocess
import sys
import time
import webview
import streamlit as st

def start_app():

    process = subprocess.Popen(
[
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.port=8501",
            "--server.headless=true",
            "--theme.base=dark",          
            "--theme.backgroundColor=#121212",
            "--theme.secondaryBackgroundColor=#1e1e1e"
        ]
    )

    time.sleep(2)


    window = webview.create_window(
        title="GraphIt",
        url="http://localhost:8501",
        width=1200,
        height=800,
        resizable=True,
        background_color='#121212',
    )

    webview.start(
        icon='graphit.ico',
        gui="edgechromium",
        debug=False,
        )

    process.kill()


if __name__ == "__main__":
    start_app()