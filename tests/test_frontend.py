import pytest
import subprocess
import requests

from time import sleep
from playwright.sync_api import sync_playwright

def test_app_responde():
    process = subprocess.Popen(["streamlit", "run", "src/frontend/app.py"])
    sleep(3)

    response = requests.get("http://localhost:8501")
    assert response.status_code == 200
    assert "<title>Streamlit</title>" in response.text

    process.kill()

def test_frontend_title():
    process = subprocess.Popen(["streamlit", "run", "src/frontend/app.py"])
    sleep(3)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8501")

        # Espera até que o título real apareça na página
        page.wait_for_selector("text=Validador de Schemas Excel", timeout=10000)

        assert "Validador de Schemas Excel" in page.content()

    process.kill()