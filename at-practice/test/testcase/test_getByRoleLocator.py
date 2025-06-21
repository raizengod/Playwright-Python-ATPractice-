import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from page.base_page import Funciones_Globales 
from locator.getByRole import RoleLocatorsPage
from locator.barraMenu import MenuLocatorsPage

def test_ir_a_opcion_playwright(set_up):
    page= set_up
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lr= RoleLocatorsPage(page)
    #IMPORTANTE: Creamos un objeto de tipo función 'barraMenu'
    ml= MenuLocatorsPage(page)

    fg.validar_url_actual("https://testautomationpractice.blogspot.com")
    fg.hacer_click_en_elemento(ml.irAPlaywright, "prueba", "SCREENSHOT_DIR", "PlaywrightPractice")
    #Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
    fg.esperar_fijo(1)
    fg.validar_url_actual(".*/p/playwrightpractice.html")
    #Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
    fg.esperar_fijo(1)
    
def test_verificar_titulo_seccion(set_up_playwright):
    page= set_up_playwright
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lr= RoleLocatorsPage(page)
    
    fg.validar_elemento_visible(lr.tituloUno, "prueba", "SCREENSHOT_DIR")
    fg.verificar_texto_contenido(lr.tituloUno, "1. getByRole() Locators", "prueba", "SCREENSHOT_DIR")
    
def test_verificar_descripcion_seccion(set_up_playwright):
    page= set_up_playwright
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lr= RoleLocatorsPage(page)
    
    fg.validar_elemento_visible(lr.labelDescripcion, "prueba", "SCREENSHOT_DIR")
    fg.verificar_texto_contenido(lr.labelDescripcion, "implicit ARIA roles.", "prueba", "SCREENSHOT_DIR")