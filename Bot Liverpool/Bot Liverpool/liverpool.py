import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración
PRODUCTO_A_BUSCAR = "laptop gamer"
OUTPUT_JSON = "stock_liverpool.json"
OUTPUT_CSV = "stock_liverpool.csv"
MAX_PRODUCTOS = 2  # Límite de productos a buscar

class LiverpoolScraper:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.wait = WebDriverWait(self.driver, 15)
        self.resultados = []

    def __del__(self):
        self.driver.quit()

    def buscar_productos(self, producto):
        try:
            self.driver.get("https://www.liverpool.com.mx/tienda/home")

            # Cerrar popup inicial si existe
            try:
                close_btn = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[aria-label='Cerrar']")))
                close_btn.click()
                time.sleep(1)
            except:
                pass

            # Buscar producto
            search_box = self.wait.until(EC.presence_of_element_located(
                (By.ID, "mainSearchbar")))
            search_box.clear()
            search_box.send_keys(producto)
            search_box.send_keys(Keys.RETURN)

            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "figcaption.m-figureCard__figcaption")))
            time.sleep(2)

            productos = self.driver.find_elements(
                By.CSS_SELECTOR, "figcaption.m-figureCard__figcaption")

            links = []
            for producto in productos[:MAX_PRODUCTOS]:
                try:
                    padre = producto.find_element(By.XPATH, "./ancestor::a[1]")
                    href = padre.get_attribute("href")
                    if href and "liverpool.com.mx/tienda" in href:
                        links.append(href)
                except Exception as e:
                    print(f"Error al obtener enlace: {e}")

            return links

        except Exception as e:
            print(f"Error al buscar productos: {str(e)}")
            return []

    def obtener_disponibilidad(self, url_producto):
        try:
            self.driver.get(url_producto)
            time.sleep(3)

            disponibilidad = {
                "producto": "",
                "url": url_producto,
                "estados": []
            }

            # 1. Obtener nombre del producto
            try:
                nombre_producto = self.wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "h1.pdp-header__title"))).text
                disponibilidad["producto"] = nombre_producto
            except:
                disponibilidad["producto"] = "Nombre no disponible"

            # 2. Hacer clic en "Ver disponibilidad en tienda"
            try:
                self.driver.execute_script("window.scrollBy(0, 500);")
                btn_disponibilidad = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.btnGeoStore")))

                # Ocultar barra sticky que tapa el botón
                self.driver.execute_script("""
                    var sticky = document.querySelector('div.m-stickyBar__actions');
                    if (sticky) { sticky.style.display = 'none'; }
                """)
                time.sleep(1)

                # Clic con JavaScript para evitar problemas de elementos superpuestos
                self.driver.execute_script("arguments[0].click();", btn_disponibilidad)
                time.sleep(2)

                # 3. Esperar que cargue la lista de estados
                self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a.a-product__anchorSelectState")))
                time.sleep(1)

                # 4. Obtener todos los estados disponibles
                estados = self.driver.find_elements(
                    By.CSS_SELECTOR, "a.a-product__anchorSelectState")

                for estado in estados[:1]:  # Solo el primer estado para prueba
                    nombre_estado = estado.text.strip()
                    if not nombre_estado:
                        continue

                    print(f"\nProcesando estado: {nombre_estado}")

                    # 5. Hacer clic en el estado
                    self.driver.execute_script("arguments[0].click();", estado)
                    time.sleep(3)

                    # 6. Esperar el modal de disponibilidad
                    try:
                        self.wait.until(EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "div.modal-body")))

                        # 7. Verificar estado en modal
                        estado_modal = self.driver.find_element(
                            By.CSS_SELECTOR, "p.undefined").text
                        print(f"Estado en modal: {estado_modal}")

                        # 8. Extraer info de tiendas
                        tiendas_info = []
                        tiendas = self.driver.find_elements(
                            By.CSS_SELECTOR, "ul.m-0.p-0 > li.pt-2.pb-2.pl-2")

                        for tienda in tiendas:
                            try:
                                nombre = tienda.find_element(
                                    By.CSS_SELECTOR, "div.a-product__store > p.m-0:first-child").text
                                stock = tienda.find_element(
                                    By.CSS_SELECTOR, "div.a-product__store > p.m-0:last-child").text

                                tiendas_info.append({
                                    "tienda": nombre,
                                    "stock": stock
                                })
                                print(f"  - {nombre}: {stock}")
                            except:
                                continue

                        if tiendas_info:
                            disponibilidad["estados"].append({
                                "estado": nombre_estado,
                                "tiendas": tiendas_info
                            })

                        # 9. Cerrar modal
                        try:
                            self.driver.find_element(
                                By.CSS_SELECTOR, "button[aria-label='Cerrar']").click()
                            time.sleep(1)
                        except:
                            pass

                    except Exception as e:
                        print(f"Error procesando modal: {str(e)}")
                        continue

                return disponibilidad if disponibilidad["estados"] else None

            except Exception as e:
                print(f"Error en proceso de disponibilidad: {str(e)}")
                self.driver.save_screenshot("error_disponibilidad.png")
                return None

        except Exception as e:
            print(f"Error general: {str(e)}")
            return None

    def guardar_resultados(self):
        # Guardar JSON
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)

        # Guardar CSV
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Producto', 'URL', 'Estado', 'Tienda', 'Disponibilidad'])

            for item in self.resultados:
                for estado in item['estados']:
                    for tienda in estado['tiendas']:
                        writer.writerow([
                            item['producto'],
                            item['url'],
                            estado['estado'],
                            tienda['tienda'],
                            tienda['stock']
                        ])

    def ejecutar(self):
        try:
            print(f"Iniciando búsqueda de: {PRODUCTO_A_BUSCAR}")

            # Obtener los links de productos
            links = self.buscar_productos(PRODUCTO_A_BUSCAR)
            if not links:
                print("No se encontraron productos.")
                return

            print(f"\nEncontrados {len(links)} productos. Procesando disponibilidad...\n")

            # Procesar cada producto
            for i, link in enumerate(links, 1):
                print(f"\n[{i}/{len(links)}] Procesando producto: {link}")

                disponibilidad = self.obtener_disponibilidad(link)

                if disponibilidad:
                    self.resultados.append(disponibilidad)
                    print(f"  Estados procesados: {len(disponibilidad['estados'])}")
                else:
                    print("  No se pudo obtener disponibilidad")

                time.sleep(1)  # Espera corta entre productos

            # Guardar resultados
            if self.resultados:
                self.guardar_resultados()
                print(f"\n✅ Datos guardados en {OUTPUT_JSON} y {OUTPUT_CSV}")
                print(f"Total de registros: {sum(len(estado['tiendas']) for item in self.resultados for estado in item['estados'])}")
            else:
                print("\n❌ No se encontraron datos de disponibilidad")

        except Exception as e:
            print(f"\n❌ Error durante la ejecución: {str(e)}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = LiverpoolScraper()
    scraper.ejecutar()
