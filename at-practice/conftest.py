#nombra el archivo: Ve a la ubicación de tu archivo y colcoar el nombre a conftest.py
# La convención de conftest.py le indica a Pytest que este archivo contiene fixtures que deben estar disponibles 
# para los tests en ese directorio y sus subdirectorios.
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from datetime import datetime
import os
from typing import Generator
from test.util import config 


# Ahora que conftest.py está en 'at-practice/', importamos 'config'
# desde el paquete 'test.util'.
from test.util import config 

# Tu URL base para las pruebas
# Ya no es necesario definir url_Base aquí, se toma de config.BASE_URL
# url_Base = "https://testautomationpractice.blogspot.com" 

# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="function",
    params=[
        # Resoluciones de escritorio
        #{"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        {"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"El tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        page = context.new_page()

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        

        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
        if browser_instance:
            browser_instance.close()
            
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session",
    params=[
        # Resoluciones de escritorio
        #{"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        {"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_playwright(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        from page.base_page import Funciones_Globales 
        from locator.getByRole import RoleLocatorsPage
        from locator.barraMenu import MenuLocatorsPage
        #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
        fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
        #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
        lr= RoleLocatorsPage(page)
        #IMPORTANTE: Creamos un objeto de tipo función 'barraMenu'
        ml= MenuLocatorsPage(page)
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"El tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        page = context.new_page()
        
        #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
        fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
        #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
        lr= RoleLocatorsPage(page)
        #IMPORTANTE: Creamos un objeto de tipo función 'barraMenu'
        ml= MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "prueba", "SCREENSHOT_DIR", "PlaywrightPractice")
        #Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        

        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
        if browser_instance:
            browser_instance.close()