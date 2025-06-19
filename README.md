# Proyecto de Automatización de Pruebas UI con Playwright y Python

## 🚀 Descripción General

Este proyecto demuestra mis habilidades en **automatización de pruebas de interfaz de usuario (UI)** utilizando **Playwright** con **Python** y el framework **Pytest**. El objetivo es validar las funcionalidades clave de la página web de práctica: https://testautomationpractice.blogspot.com/.

Este repositorio forma parte de mi portafolio personal, mostrando mi capacidad para diseñar, desarrollar y ejecutar pruebas automatizadas robustas.

## ✨ Características Principales

* **Tecnología Moderna:** Implementado con Playwright, un framework de automatización rápido y confiable.
* **Lenguaje de Programación:** Desarrollado en **Python 3.13.5**.
* **Gestión de Pruebas:** Organización de casos de prueba con **Pytest**.
* **Generación de Informes:** Utilización de **Allure Reports** para visualización clara y detallada de los resultados de las pruebas.
* **Cobertura Funcional:** Validación de formularios, tablas web, alertas, carga de archivos, interacciones de arrastrar y soltar, y navegación entre ventanas/pestañas.

## 🛠️ Tecnologías Utilizadas

* **Playwright**: Framework de automatización de navegadores para pruebas end-to-end.
* **Python**: Lenguaje de programación utilizado para escribir los scripts de prueba.
* **Pytest**: Framework de pruebas para Python, utilizado para organizar y ejecutar los tests.
* **GitHub Actions**: Para la integración continua (CI) y la ejecución automatizada de pruebas.
* **Java Development Kit (JDK):** Requisito para Allure Reports.

## 🚀 Ejecución de las Pruebas
Sigue estos pasos para configurar y ejecutar las pruebas en tu entorno local:

**Prerrequisitos**
1. **Instalar Python 3.13.5** (si no lo tienes instalado).
2. **Instalar Java Development Kit (JDK 8 o superior):**
* Descárgalo e instálalo desde el sitio oficial de Oracle o una distribución OpenJDK (ej. AdoptOpenJDK/Eclipse Temurin).
* Asegúrate de que la variable de entorno JAVA_HOME esté configurada y que java esté en tu PATH.
3. **Instalar la Herramienta de Línea de Comandos de Allure:**
* **En macOS/Linux (usando Homebrew):**
    ```bash
    brew install allure

* **En Windows (usando Scoop):**
    ```bash
    scoop install allure

* **Descarga manual:** Descarga la última versión desde **[Allure GitHub Releases](https://github.com/allure-framework/allure2/releases)** y añade el directorio ```bin``` a tu ```PATH```.

**Configuración del Proyecto**

Para ejecutar las pruebas localmente, sigue los siguientes pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/raizengod/Playwright-Python-ATPractice-.git
    cd AT-PRACTICE
    ```

2.  **Crear y activar un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    playwright install  # Instala los navegadores necesarios (Chromium, Firefox, WebKit)
    ```
**Ejecución de Pruebas**

1.  **Ejecuta las pruebas y genera los resultados de Allure:**
    ```bash
    pytest --alluredir=allure-results
    ```

2.  **Ejecutar todas las pruebas con Pytest:**
    ```bash
    pytest -s -v
    ```

3.  **Ejecutar pruebas específicas (ejemplo):**
    ```bash
    pytest 
    ```

4.  **Ejecutar todas las pruebas con reporte detallado y genera los resultados de Allure:**:**
    ```bash
    pytest -s -v --template=html1/index.html --report=reporte_de_ejecución.html --alluredir=allure-results
    ```

5.  **Genera el informe HTML de Allure:**
    ```bash
    allure generate allure-results --clean
    ```

6.  **Abre el informe en tu navegador:**
    ```bash
    allure open allure-report
    ```

## 📂 Estructura del Proyecto (Ejemplo)

```
AT-PRACTICE/
├── .github/
│   └── workflows/
│       └── playwright.yml         # Configuración de GitHub Actions para CI
├── mv_ATP/
├── at-preactice/                 # Contenedor principal del código fuente
│   ├── pages/                 # Implementación del Page Object Model (POM)
│   │   ├── __init__.py
│   │   ├── base_page.py       # Clase base con funciones globales
│   │   ├── login_page.py      # Ejemplo de Page Object para Login (si existe)
│   │   ├── home_page.py       # Ejemplo de Page Object para Home (si existe)
│   │   └── cart_page.py       # Ejemplo de Page Object para Carrito (si existe)
│   ├── selectores/            # Centralización de selectores de elementos web
│   │   ├── __init__.py
│   │   ├── selectorCarrito.py
│   │   ├── selectorHome.py
│   │   ├── selectorLogin.py
│   │   ├── selectorMenu.py
│   │   └── selectorProducto.py
│   ├── tests/
│   │   ├── test_web_elements.py  # Archivos con los casos de prueba
│   │   ├── reporte/
│   │   │   ├── allure-results/          # Directorio donde se guardan los resultados de Allure (generado al ejecutar tests)
│   │   │   └── allure-report/           # Directorio donde se genera el informe HTML (generado por Allure CLI)
│   │   ├── evidencia/
│   │   │   ├── video/
│   │   │   └── imagen/ 
│   │   ├── traceView/   
│   │   └── util/
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo
```