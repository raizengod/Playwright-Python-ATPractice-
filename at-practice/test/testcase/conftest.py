#nombra el archivo: Ve a la ubicación de tu archivo y colcoar el nombre a conftest.py
# La convención de conftest.py le indica a Pytest que este archivo contiene fixtures que deben estar disponibles 
# para los tests en ese directorio y sus subdirectorios.
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from datetime import datetime
import os # Importa el módulo os para manejar rutas de archivos y creación de directorios

# Tu URL base para las pruebas
url_Base = "https://testautomationpractice.blogspot.com" # Tu URL de inicio de sesión real

# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="function",
    params=[
        # Resoluciones de escritorio
        {"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        {"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        {"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        {"browser": "chromium", "device": "iPhone 12", "resolution": None},
        {"browser": "firefox", "device": "Pixel 5", "resolution": None},
        {"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up(playwright: Playwright, request) -> None:
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

        # Aseguramos de que el directorio de evidencia de video exista
        # Se usa os.path.join para construir la ruta, lo cual es más robusto.
        video_dir = os.path.join("test", "evidencia", "video")
        os.makedirs(video_dir, exist_ok=True) # Crea el directorio si no existe

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": video_dir,
            "record_video_size": {"width": 1920, "height": 1080} # Establece un tamaño de video consistente
        }

        if device_name:
            # Usa los descriptores de dispositivo de Playwright para la emulación móvil
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            # Establece el tamaño del viewport para resoluciones de escritorio
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            # Fallback si no hay resolución/dispositivo específico, usando solo las opciones de video
            context = browser_instance.new_context(**context_options) 

        page = context.new_page()

        # Inicializa Trace Viewer con un nombre dinámico
        # Formato: traceview_AAAAMMDD_HHMMSS_Navegador_ResolucionOdispositivo.zip
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "") # Limpiar el nombre del dispositivo
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        
        # Se usa os.path.join para construir la ruta completa del traceview
        # Aseguramos de que el directorio traceview exista antes de usarlo.
        trace_output_dir = os.path.join("test", "traceview")
        os.makedirs(trace_output_dir, exist_ok=True) 
        trace_path = os.path.join(trace_output_dir, trace_file_name)


        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(url_Base)
        page.set_default_timeout(5000)

        yield page

    finally:
        if context:
            # Detén el rastreo y guárdalo con la ruta dinámica
            context.tracing.stop(path=trace_path)
            context.close()
        if browser_instance:
            browser_instance.close()