from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def before_scenario(context, scenario):
    """
    Inicializa el WebDriver antes de cada escenario de prueba.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    context.driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=chrome_options)
    context.base_url = "http://127.0.0.1:8000"

def after_scenario(context, scenario):
    """
    Cierra el navegador después de cada escenario de prueba.
    """
    context.driver.quit()