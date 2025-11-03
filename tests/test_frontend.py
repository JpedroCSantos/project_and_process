from selenium import webdriver
from time import sleep
import pytest
import subprocess
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    process = subprocess.Popen(["streamlit", "run", "src/frontend/app.py"])
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(5)
    yield driver

    driver.quit()
    process.kill()

def test_check_title_is(driver):
    driver.get("http://localhost:8501")
    sleep(5)
    page_title = driver.title

    expected_title = "Validador de Schemas Excel"
    assert page_title == expected_title