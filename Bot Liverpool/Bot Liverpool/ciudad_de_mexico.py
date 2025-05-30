import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verificar_disponibilidad_liverpool(url_producto):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 30)

    resultados = []

    try:
        # Paso 1: Ir al URL del producto
        driver.get(url_producto)

        # Paso 2: Click en "Ver disponibilidad en tienda"
        ver_disp_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btnGeoStore")))
        ver_disp_btn.click()

        # Paso 3: Esperar que aparezca el modal y hacer click en "AGUASCALIENTES"
        estado_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class, 'a-product__anchorSelectState') and contains(text(),'CDMX/ZONA METROPOLITANA')]")
        ))
        estado_btn.click()

        # Paso 4: Esperar a que cargue la disponibilidad en tiendas
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.a-product__store")))

        # Paso 5: Extraer disponibilidad por tienda
        tiendas = driver.find_elements(By.CSS_SELECTOR, "div.a-product__store")
        for tienda in tiendas:
            try:
                nombre_tienda = tienda.find_elements(By.TAG_NAME, "p")[0].text.strip()
                stock = tienda.find_elements(By.TAG_NAME, "p")[1].text.strip()
                resultados.append({
                    "Estado": "CDMX",
                    "Tienda": nombre_tienda,
                    "Stock": stock
                })
            except Exception as e:
                print(f" Error leyendo tienda: {e}")

        # Paso 6: Guardar en CSV
        with open("disponibilidad_cdmx.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=["Estado", "Tienda", "Stock"])
            writer.writeheader()
            writer.writerows(resultados)

        print(" Datos guardados en 'disponibilidad_CDMX.csv'")

    finally:
        driver.quit()

if __name__ == "__main__":
    # Reemplaza esta URL por cualquier producto de tu CSV original
    url = "https://www.liverpool.com.mx/tienda/pdp/gorra-con-visera-curva-entrenamiento-puma/1169156278?skuid=1169156278"
    verificar_disponibilidad_liverpool(url)
