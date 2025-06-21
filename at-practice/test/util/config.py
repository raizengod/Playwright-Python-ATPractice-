import os

# --- Configuración de URLs ---
BASE_URL = "https://testautomationpractice.blogspot.com"

# --- Rutas de Almacenamiento de Evidencias ---

# Directorio base donde se guardarán todas las evidencias.
# Puedes ajustar esto según la estructura de tu proyecto.
# Por ejemplo, si este archivo está en la raíz y tus tests están en una carpeta 'tests',
# podrías querer 'os.path.join(os.getcwd(), "evidencias")' o similar.
# Para este ejemplo, asumo que las rutas son relativas a la ejecución de pytest.
EVIDENCE_BASE_DIR = "test"

# Ruta para videos.
# Se creará 'test/evidencia/video'
VIDEO_DIR = os.path.join(EVIDENCE_BASE_DIR, "evidencia", "video")

# Ruta para traceview.
# Se creará 'test/traceview'
TRACEVIEW_DIR = os.path.join(EVIDENCE_BASE_DIR, "traceview")

# Ruta para capturas de pantalla (si planeas guardar capturas de pantalla fuera del traceview o videos).
# Puedes añadir una lógica similar a la del video si necesitas capturas separadas.
# Por ahora, las capturas de pantalla se incluyen en el traceview.
SCREENSHOT_DIR = os.path.join(EVIDENCE_BASE_DIR, "evidencia", "imagen")

# Función para asegurar que los directorios existan
def ensure_directories_exist():
    """
    Crea los directorios necesarios si no existen.
    """
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(TRACEVIEW_DIR, exist_ok=True)
    # Si descomentas SCREENSHOT_DIR, también agrégalo aquí:
    # os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Llama a la función para asegurar que los directorios se creen al importar este módulo
ensure_directories_exist()