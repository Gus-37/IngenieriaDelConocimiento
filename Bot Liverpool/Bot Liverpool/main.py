from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
def buscar_con_click_paginado(termino, num_paginas=3):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
 
    try:
        # 1) Inicio de búsqueda
        driver.get("https://www.google.com")
        caja = driver.find_element(By.NAME, "q")
        caja.send_keys(termino + Keys.RETURN)
 
        # Pausa para CAPTCHA en la primera página
        input("Si aparece CAPTCHA, resuélvelo y pulsa Enter para continuar…")
 
        for pagina in range(1, num_paginas + 1):
            # 2) Espera resultados
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))
            )
 
            # 3) Extrae y filtra encabezados
            encabezados = driver.find_elements(By.CSS_SELECTOR, "h3")
            textos = [h.text.strip() for h in encabezados if h.text.strip()]
 
            print(f"\n— Página {pagina}: {len(textos)} resultados —")
            for i, titulo in enumerate(textos, 1):
                print(f"{i}. {titulo}")
 
            # 4) Si aún no hemos llegado al tope, hacemos clic en “Siguiente”
            if pagina < num_paginas:
                try:
                    # Opción A: clic en el botón “Siguiente” (flecha)
                    siguiente = driver.find_element(By.ID, "pnnext")
                    siguiente.click()
                except:
                    # Opción B: clic en número de página concreto
                    next_page_num = pagina + 1
                    boton = driver.find_element(
                        By.XPATH,
                        f"//a[@aria-label='Page {next_page_num}']"
                    )
                    boton.click()
 
                # Breve espera para que cambie la página
                WebDriverWait(driver, 20).until(
                    EC.staleness_of(encabezados[0])
                )
 
    finally:
        driver.quit()
 
if __name__ == "__main__":
    buscar_con_click_paginado("mexico", num_paginas=3)