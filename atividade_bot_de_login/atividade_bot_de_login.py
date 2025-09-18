from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

# Configuração do log
logging.basicConfig(
    filename="./atividade_bot_de_login/login.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Usuário e senha de teste (válidos para esse site)
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"

# Configurações do webdriver
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Inicializa o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Abre a página de login
    driver.get("https://the-internet.herokuapp.com/login")
    wait = WebDriverWait(driver, 10)
    time.sleep(2)

    # Preenche usuário
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(USERNAME)

    # Preenche senha
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PASSWORD)

    # Submete o formulário
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    # Esperar pela mensagem de sucesso
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success")))
    message = driver.find_element(By.CSS_SELECTOR, ".flash.success").text.strip()

    # Verifica se login foi bem-sucedido
    if "You logged into a secure area!" in message:
        logging.info("Login bem-sucedido: %s", message)
        print("✅ Login realizado com sucesso!")
    else:
        logging.error("Falha no login: %s", message)
        print("❌ Erro no login:", message)

except Exception as e:
    logging.exception("Erro inesperado: %s", str(e))
    print("⚠️ Ocorreu um erro:", e)

finally:
    # Fecha o navegador
    driver.quit()
