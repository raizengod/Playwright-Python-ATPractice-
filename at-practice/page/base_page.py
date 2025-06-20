#Importamos todo lo necesario
import re
import time
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from datetime import datetime
import os

class Funciones_Globales:
    
    #1- Creamos una función incial 'Constructor'-----ES IMPORTANTE TENER ESTE INICIADOR-----
    def __init__(self, page):
        self.page= page
        
    #2- Función para generar el nombre de archivo con marca de tiempo
    def _generar_nombre_archivo_con_timestamp(self, prefijo):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3] # Quita los últimos 3 dígitos para milisegundos más precisos
        return f"{prefijo}_{timestamp}"
    
    #3- Función para tomar captura de pantalla
    def tomar_captura(self, nombre_base, directorio):
        if not os.path.exists(directorio):
            os.makedirs(directorio) # Crea el directorio si no existe
        nombre_archivo = self._generar_nombre_archivo_con_timestamp(nombre_base)
        ruta_completa = os.path.join(directorio, f"{nombre_archivo}.jpg")
        self.page.screenshot(path=ruta_completa)
        print(f"Captura guardada en: {ruta_completa}") # Para ver dónde se guardó
        self.Esperar()
        
    #4- unción basica para tiempo de espera que espera recibir el parametro tiempo
    #En caso de no pasar el tiempo por parametro, el mismo tendra un valor de medio segundo
    def Esperar(self, tiempo=0.5):
        time.sleep(tiempo)
        
    #5- unción para indicar el tiempo que se tardará en hacer el scroll
    def Scroll(self, horz, vert, tiempo=0.5): 
        #Usamos 'self' ya que lo tenemos inicializada en __Init__ y para que la palabra page de la función funcione es necesaria
        self.page.mouse.wheel(horz, vert)
        time.sleep(tiempo)
        
    #7- Función para rellenar campo de texto y hacer capture la imagen
    def rellenarCampodeTexto(self, selector, texto, nombre_base, directorio, tiempo=0.5):
        try:
            # 1. Asegurar que el elemento es visible y está habilitado.
            expect(selector).to_be_visible(timeout=10000) # Espera hasta 10 segundos
            expect(selector).to_be_enabled(timeout=5000)  # Espera hasta 5 segundos
            print(f"  --> El campo '{selector}' está visible y habilitado.")

            # Resaltar el campo en azul para depuración visual
            selector.highlight()
            self.tomar_captura("Antes_de_rellenar", nombre_base, directorio, directorio)

            # 3. Rellenar el campo de texto.
            # Playwright espera automáticamente a que el campo sea editable.
            selector.fill(texto, timeout=15000) # Espera hasta 15 segundos para la operación de llenado
            print(f"  --> Campo '{selector}' rellenado con éxito con el texto: '{texto}'.")

            self.tomar_captura("Después_de_rellenar", nombre_base, directorio)

        except TimeoutError as e:
            # Captura errores cuando una aserción o una acción excede su tiempo de espera.
            error_msg = (
                f"ERROR (Timeout): El tiempo de espera se agotó al interactuar con '{selector}'.\n"
                f"Posibles causas: El elemento no apareció, no fue visible/habilitado/editable a tiempo.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura("error_timeout", nombre_base, directorio)
            # Re-lanza la excepción para que el test principal falle y marque el paso como erróneo.
            raise PlaywrightException(error_msg) from e

        except PlaywrightException as e:
            # Captura otras excepciones generales de Playwright (ej., elemento desprendido, selector incorrecto).
            error_msg = (
                f"ERROR (Playwright): Ocurrió un problema de Playwright al interactuar con '{selector}'.\n"
                f"Verifica la validez del selector y el estado del elemento en el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura("error_playwright", nombre_base, directorio)
            raise # Re-lanza la excepción

        except Exception as e:
            # Captura cualquier otra excepción inesperada que no sea de Playwright.
            error_msg = (
                f"ERROR (Inesperado): Se produjo un error desconocido al interactuar con '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura("error_inesperado", nombre_base, directorio)
            raise

        finally:
            # Este bloque se ejecuta siempre, independientemente de si hubo un error o no.
            if tiempo > 0:
                print(f"  --> Realizando espera fija de {tiempo} segundos.")
                time.sleep(tiempo)