#Importamos todo lo necesario
import re
import time
from playwright.sync_api import Page, expect, TimeoutError, PlaywrightException, Playwright, sync_playwright
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
        print(f"📸 Captura guardada en: {ruta_completa}") # Para ver dónde se guardó
        
    #4- unción basica para tiempo de espera que espera recibir el parametro tiempo
    #En caso de no pasar el tiempo por parametro, el mismo tendra un valor de medio segundo
    def esperar_fijo(self, tiempo=0.5):
        time.sleep(tiempo)
        
    #5- unción para indicar el tiempo que se tardará en hacer el scroll
    def scroll_pagina(self, horz, vert, tiempo=0.5): 
        #Usamos 'self' ya que lo tenemos inicializada en __Init__ y para que la palabra page de la función funcione es necesaria
        self.page.mouse.wheel(horz, vert)
        time.sleep(tiempo)
        
    #6- Función para validar que un elemento es visible
    def validar_elemento_visible(self, selector, nombre_base, directorio, timeout_ms: int = 10000, resaltar: bool = True) -> bool:
        print(f"Validando visibilidad del elemento con selector: '{selector}'")

        try:
            # Espera explícita para que el elemento sea visible.
            expect(selector).to_be_visible(timeout_ms)
            
            if resaltar:
                selector.highlight() # Resaltar el elemento visible
                
            self.tomar_captura(f"{nombre_base}_visible", directorio)
            print(f"  --> ÉXITO: El elemento '{selector}' es visible en la página.")
            return True

        except TimeoutError as e:
            error_msg = (
                f"FALLO (Timeout): El elemento con selector '{selector}' NO es visible "
                f"después de {timeout_ms / 1000} segundos.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            # Toma una captura de pantalla del estado actual de la página cuando el elemento no es visible
            self.tomar_captura(f"{nombre_base}_NO_visible_timeout", directorio)
            # En este caso, no relanzamos la excepción porque la función está diseñada para retornar False
            # Si el llamador necesita que la prueba falle, debe verificar el valor de retorno.
            return False

        except PlaywrightException as e:
            error_msg = (
                f"FALLO (Playwright): Error de Playwright al verificar la visibilidad de '{selector}'.\n"
                f"Posibles causas: Selector inválido, elemento desprendido del DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            # Aquí sí relanzamos, ya que es un error inesperado de Playwright, no solo que no sea visible.
            raise 

        except Exception as e:
            error_msg = (
                f"FALLO (Inesperado): Ocurrió un error inesperado al validar la visibilidad de '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise

        finally:
            # Eliminamos el time.sleep() o self.esperar_fijo() final, ya que no es necesario para una validación de visibilidad.
            # El timeout de expect() ya maneja la espera.
            pass
    
    #7- Función para validar que un elemento NO es visible
    def validar_elemento_no_visible(self, selector, nombre_base, directorio, timeout: int = 5000):
        print(f"Validando que el elemento con selector '{selector}' NO es visible.")
        try:
            # Usamos to_be_hidden() con un timeout explícito para mayor robustez.
            # Playwright espera automáticamente por el elemento sin necesidad de time.sleep()
            expect(selector).to_be_hidden(timeout=timeout)
            print(f"El elemento con selector '{selector}' NO es visible.")
            self.tomar_captura(f"{nombre_base}_fallo_no_visible", directorio)
            
        except AssertionError as e:
            print(f"Error: El elemento con selector '{selector}' aún es visible o no se ocultó a tiempo.")
            # Tomamos la captura solo si la aserción falla para depuración.
            self.tomar_captura(f"{nombre_base}_fallo_no_visible", directorio)
            raise e # Re-lanza la excepción para que el test falle.
        
        finally:
            # Puedes optar por tomar una captura de pantalla exitosa si lo deseas,
            # pero generalmente se toman en caso de fallo para depuración.
            # self.tomar_captura(nombre_base=f"{nombre_base}_exito_no_visible", directorio=directorio)
            pass
        
    #8- Función para verificar que un elemento (o elementos) localizado en una página web contiene un texto específico    
    def verificar_texto_contenido(self, selector, texto_esperado, nombre_base, directorio, timeout: float = 5.0):
        try:
            # Esperar visibilidad y capturar antes de la verificación del texto
            # Usamos expect().to_be_visible() con un timeout específico.
            # El timeout de expect es más robusto que time.sleep().
            expect(selector).to_be_visible(timeout=timeout)
            print(f"✅ Elemento con selector '{selector}' es visible.")

            # Opcional: Resaltar el elemento solo si es necesario para depuración.
            # En un entorno de CI/CD, no siempre es práctico o visible.
            selector.highlight()

            self.tomar_captura(f"{nombre_base}_antes_verificacion", directorio)

            # Verificar que el elemento contenga el texto esperado
            # Playwright ya espera implícitamente a que el texto aparezca.
            # Usamos to_contain_text() para la verificación, también con timeout.
            expect(selector).to_contain_text(texto_esperado, timeout=timeout)
            print(f"✅ Elemento con selector '{selector}' contiene el texto esperado: '{texto_esperado}'.")

            # 4. Capturar después de la verificación exitosa
            self.tomar_captura(nombre_base=f"{nombre_base}_despues_verificacion", directorio=directorio)

        except Exception as e:
            # Manejo de errores para capturar cualquier fallo durante la operación
            print(f"❌ Error al verificar el texto para el selector '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_error", directorio)
            raise  # Re-lanzar la excepción para que el test falle
        
    #9- Función para rellenar campo de texto y hacer capture la imagen
    def rellenar_campo_de_texto(self, selector, texto, nombre_base, directorio, tiempo=0.5):
        try:
            # Resaltar el campo en azul para depuración visual
            selector.highlight()
            self.tomar_captura("Antes_de_rellenar", directorio)

            # Rellenar el campo de texto.
            # Playwright espera automáticamente a que el campo sea editable.
            selector.fill(texto, timeout=15000) # Espera hasta 15 segundos para la operación de llenado
            print(f"  --> Campo '{selector}' rellenado con éxito con el texto: '{texto}'.")

            self.tomar_captura(nombre_base, directorio)

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
                
    #10- Función para rellenar campo numérico y hacer capture la imagen
    def rellenar_campo_numerico_positivo(self, selector, valor_numerico: int | float, nombre_base, directorio, tiempo= 0.5):
        print(f"Iniciando intento de rellenar campo con selector '{selector}' con el valor numérico POSITIVO: '{valor_numerico}'")

        # --- VALIDACIÓN DE NÚMERO POSITIVO ---
        if not isinstance(valor_numerico, (int, float)):
            error_msg = f"ERROR: El valor proporcionado '{valor_numerico}' no es un tipo numérico (int o float)."
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_valor_no_numerico", directorio)
            raise ValueError(error_msg)

        if valor_numerico < 0:
            error_msg = f"ERROR: El valor numérico '{valor_numerico}' no es positivo. Se esperaba un número mayor o igual a cero."
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_valor_negativo", directorio)
            raise ValueError(error_msg)

        # Convertir el valor numérico a cadena para el método fill()
        valor_a_rellenar_str = str(valor_numerico)
        # --- FIN DE VALIDACIÓN ---

        locator = self.page.locator(selector) # Instanciar el locator correctamente

        try:
            # Resaltar el campo en azul para depuración visual
            selector.highlight()
            # Se usa f-string para incluir nombre_base en el nombre de la captura
            self.tomar_captura(f"{nombre_base}_antes_de_rellenar", directorio) 

            # Rellenar el campo de texto.
            selector.fill(valor_a_rellenar_str)
            print(f"  --> Campo '{selector}' rellenado con éxito con el valor: '{valor_a_rellenar_str}'.")

            self.tomar_captura(f"{nombre_base}_despues_de_rellenar", directorio)

        except TimeoutError as e:
            error_msg = (
                f"ERROR (Timeout): El tiempo de espera se agotó al interactuar con '{selector}'.\n"
                f"Posibles causas: El elemento no apareció, no fue visible/habilitado/editable a tiempo.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_timeout", directorio)
            raise PlaywrightException(error_msg) from e

        except PlaywrightException as e:
            error_msg = (
                f"ERROR (Playwright): Ocurrió un problema de Playwright al interactuar con '{selector}'.\n"
                f"Verifica la validez del selector y el estado del elemento en el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise # Re-lanza la excepción

        except TypeError as e:
            error_msg = (
                f"ERROR (TypeError): El selector proporcionado no es un objeto Locator válido.\n"
                f"Asegúrate de pasar un objeto locator o una cadena para que sea convertido a locator.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_tipo_selector", directorio)
            raise

        except Exception as e:
            error_msg = (
                f"ERROR (Inesperado): Se produjo un error desconocido al interactuar con '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise

        finally:
            if tiempo > 0:
                print(f"  --> Realizando espera fija de {tiempo} segundos.")
                time.sleep(tiempo)
                
    #11- Función para validar titulo de una página
    def validar_titulo_de_web(self, titulo_esperado, nombre_base, directorio, timeout_ms: int = 5000):
        try:
            # Usa el 'expect' de Playwright con un timeout para una espera robusta
            expect(self.page).to_have_title(titulo_esperado, timeout=timeout_ms)
            print(f"✅ Título de la página '{titulo_esperado}' validado exitosamente.")
           
            self.tomar_captura(nombre_base, directorio)

        except Exception as e:
            print(f"❌ Error al validar el título o tomar la captura: {e}")
            # Opcionalmente, puedes relanzar la excepción si quieres que la prueba falle
            raise
    
    #12- Función para validar UR    
    def validar_url_actual(self, patron_url, timeout_ms: int = 10000):
        try:
            # Usa 'expect' de Playwright con un timeout para una espera robusta.
            # to_have_url ya espera automáticamente y reintenta.
            expect(self.page).to_have_url(re.compile(patron_url), timeout=timeout_ms)
            print(f"✅ URL '{self.page.url}' validada exitosamente con el patrón: '{patron_url}'.")
            
        except Exception as e:
            print(f"❌ Error al validar la URL. URL actual: '{self.page.url}', Patrón esperado: '{patron_url}'. Error: {e}")
            # Es buena práctica relanzar la excepción para que la prueba falle si la URL no coincide
            raise
        
    #13- Función para hacer click
    def hacer_click_en_elemento(self, selector, nombre_base, directorio, texto_esperado= None, timeout_ms: int = 10000):
        try:
            # Resaltar el elemento (útil para depuración visual)
            selector.highlight()

            # Validaciones robustas con Playwright's 'expect'
            # Playwright ya espera automáticamente a que el elemento sea visible y esté habilitado
            # hasta que se cumpla el timeout, lo que elimina la necesidad de time.sleep.
            expect(selector).to_be_visible(timeout=timeout_ms)
            expect(selector).to_be_enabled(timeout=timeout_ms)

            # Validar texto solo si se proporciona
            if texto_esperado:
                expect(selector).to_contain_text(texto_esperado, timeout=timeout_ms)
                print(f"✅ El elemento con selector '{selector}' contiene el texto esperado: '{texto_esperado}'.")

            # Hacer click en el elemento
            selector.click(timeout=timeout_ms) # El click también puede tener un timeout
            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
            print(f"✅ Click realizado exitosamente en el elemento con selector '{selector}'.")

        except Exception as e:
            print(f"❌ Error al intentar hacer click en el elemento con selector '{selector}'. Error: {e}")
            # Es buena práctica relanzar la excepción para que la prueba falle
            raise

    #14- Función para hacer doble click
    def hacer_doble_click_en_elemento(self, selector, nombre_base, directorio, texto_esperado= None, timeout_ms: int = 10000):
        try:
            # Resaltar el elemento (útil para depuración visual)
            selector.highlight()

            # Validaciones robustas con Playwright's 'expect'
            # Playwright ya espera automáticamente a que el elemento sea visible y esté habilitado
            # hasta que se cumpla el timeout, lo que elimina la necesidad de time.sleep.
            expect(selector).to_be_visible(timeout=timeout_ms)
            expect(selector).to_be_enabled(timeout=timeout_ms)

            # Validar texto solo si se proporciona
            if texto_esperado:
                expect(selector).to_contain_text(texto_esperado, timeout=timeout_ms)
                print(f"✅ El elemento con selector '{selector}' contiene el texto esperado: '{texto_esperado}'.")

            # Realizar la acción de DOBLE CLICK
            selector.dblclick(timeout=timeout_ms)
            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
            print(f"✅ Doble click realizado exitosamente en el elemento con selector '{selector}'.")

        except Exception as e:
            print(f"❌ Error al intentar hacer click en el elemento con selector '{selector}'. Error: {e}")
            # Es buena práctica relanzar la excepción para que la prueba falle
            raise
    
    #14- Función para hacer hover over
    def hacer_hover_en_elemento(self, selector, nombre_base, directorio, texto_esperado= None, timeout_ms: int = 10000):
        try:
            # Resaltar el elemento (útil para depuración visual)
            selector.highlight()

            # Validaciones robustas con Playwright's 'expect'
            # Playwright ya auto-espera por estas condiciones antes del hover.
            expect(selector).to_be_visible(timeout=timeout_ms)
            expect(selector).to_be_enabled(timeout=timeout_ms)

            # Validar texto solo si se proporciona (útil para asegurar que se hace hover sobre el elemento correcto)
            if texto_esperado:
                expect(selector).to_contain_text(texto_esperado, timeout=timeout_ms)
                print(f"✅ El elemento con selector '{selector}' contiene el texto esperado: '{texto_esperado}'.")

            # Realizar la acción de HOVER OVER
            selector.hover(timeout=timeout_ms) # El hover también puede tener un timeout
            print(f"✅ Hover realizado exitosamente en el elemento con selector '{selector}'.")

            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura

        except Exception as e:
            print(f"❌ Error al intentar hacer hover en el elemento con selector '{selector}'. Error: {e}")
            # Es buena práctica relanzar la excepción para que la prueba falle
            raise
        
    #15- Función para verificar si un elemento está habilitado o deshabilitado
    def verificar_elemento_habilitado(self, selector, nombre_base, directorio, timeout_ms: int = 10000) -> bool:
        try:
            # Resaltar el elemento (útil para depuración visual)
            selector.highlight()

            # Validar si el elemento está habilitado usando expect de Playwright
            # Playwright espera automáticamente hasta que el elemento cumpla la condición
            expect(selector).to_be_enabled(timeout=timeout_ms)
            print(f"✅ El elemento con selector '{selector}' está habilitado.")
            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
            return True
        
        except Exception as e:
            print(f"❌ Error: El elemento con selector '{selector}' NO está habilitado o no se encontró dentro del tiempo esperado. Error: {e}")
            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
            return False
        