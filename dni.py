__author__ = 'jose Quine'

# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from sys import argv


try:
    import Image
except ImportError:
    from PIL import Image


#Permite Marcar Autonomamente el teclado
def marcar_teclado(dni, driver):
    #Recorremos cada uno de los digitos del DNI
    for num in dni:
        #Buscamos el boton que tenga como nombre tecla_0
        boton_0 = driver.find_element_by_name("tecla_0")
        #Obtenemos el valor del boton con nombre tecla_0
        valor_0 = boton_0.get_attribute('value')
        #Buscamos el boton que tenga como nombre tecla_1
        boton_1 = driver.find_element_by_name("tecla_1")
        #Obtenemos el valor del boton con nombre tecla_1
        valor_1 = boton_1.get_attribute('value')
        #Buscamos el boton que tenga como nombre tecla_2
        boton_2 = driver.find_element_by_name("tecla_2")
        #Obtenemos el valor del boton con nombre tecla_2
        valor_2 = boton_2.get_attribute('value')
        #Buscamos el boton que tenga como nombre tecla_3
        boton_3 = driver.find_element_by_name("tecla_3")
        #Obtenemos el valor del boton con nombre tecla_3
        valor_3 = boton_3.get_attribute('value')
        #Buscamos el boton que tenga como nombre tecla_4
        boton_4 = driver.find_element_by_name("tecla_4")
        #Obtenemos el valor del boton con nombre tecla_4
        valor_4 = boton_4.get_attribute('value')
        #Buscamos el boton que tenga como nombre tecla_5
        boton_5 = driver.find_element_by_name("tecla_5")
        #Obtenemos el valor del boton con nombre tecla_5
        valor_5 = boton_5.get_attribute('value')
        #Buscamos el boton que tenga como nombre tecla_6
        boton_6 = driver.find_element_by_name("tecla_6")
        #Obtenemos el valor del boton con nombre tecla_6
        valor_6 = boton_6.get_attribute('value')
        #Buscamos el boton que tenga como nombre tecla_7
        boton_7 = driver.find_element_by_name("tecla_7")
        #Obtenemos el valor del boton con nombre tecla_7
        valor_7 = boton_7.get_attribute('value')
        #Buscamos el boton que tenga como nombre tecla_8
        boton_8 = driver.find_element_by_name("tecla_8")
        #Obtenemos el valor del boton con nombre tecla_8
        valor_8 = boton_8.get_attribute('value')
        #Buscamos el boton que tenga como nombre tecla_9
        boton_9 = driver.find_element_by_name("tecla_9")
        #Obtenemos el valor del boton con nombre tecla_9
        valor_9 = boton_9.get_attribute('value')

        if num==valor_0:
            boton_0 = driver.find_element_by_name("tecla_0")
            boton_0.click()
        elif num==valor_1:
            boton_1 = driver.find_element_by_name("tecla_1")
            boton_1.click()
        elif num==valor_2:
            boton_2 = driver.find_element_by_name("tecla_2")
            boton_2.click()
        elif num==valor_3:
            boton_3 = driver.find_element_by_name("tecla_3")
            boton_3.click()
        elif num==valor_4:
            boton_4 = driver.find_element_by_name("tecla_4")
            boton_4.click()
        elif num==valor_5:
            boton_5 = driver.find_element_by_name("tecla_5")
            boton_5.click()
        elif num==valor_6:
            boton_6 = driver.find_element_by_name("tecla_6")
            boton_6.click()
        elif num==valor_7:
            boton_7 = driver.find_element_by_name("tecla_7")
            boton_7.click()
        elif num==valor_8:
            boton_8 = driver.find_element_by_name("tecla_8")
            boton_8.click()
        elif num==valor_9:
            boton_9 = driver.find_element_by_name("tecla_9")
            boton_9.click()

def pausa(segundos):
    sleep(segundos)

def crear_archivo(texto):
    f=open("dni.txt","w")
    f.write(texto)
    f.write("\n")
    f.close()

def limpiar_reniec_web(dni, driver):
    #Obtenemos el boton de limpiar
    boton_limpiar=driver.find_element_by_name("bot_limpiar01")
    #Damos click al boton de limpiar
    boton_limpiar.click()

def romper_captcha(nombre_imagen):
    #Abro la imagen
    img = Image.open(nombre_imagen)
    #Obtengo un arreglo de pixeles de la imagen
    pixdata = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][2] < 146:
                pixdata[x, y] = (255, 255, 255)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][1] > 64:
                pixdata[x, y] = (255, 255, 255)
            else:
                pixdata[x, y] = (0,0,0)

    #Guardo la imagen modificada
    rgb_im = img.convert('RGB')
    rgb_im.save("modificado.jpg", quality=95)

    #Abro la imagen modificado
    image = Image.open("modificado.jpg")
    #Obtenemos el texto de la imagen
    frase = pytesseract.image_to_string(image)
    #Retornamos el texto eliminado los espacios en blanco entre las palabras y convirtiendolas en mayusculas
    return frase.replace(' ',"").upper()


def ir_reniec_web(dni):
    fp = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(fp)
    #Definimos nuestra pagina objetivo
    driver.get("https://cel.reniec.gob.pe/valreg/valreg.do")
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "imagcodigo")))
    except:
        print("Elemento no esta presente")

    #Marca el teclado automaticamente segun el numero del dni
    marcar_teclado(dni, driver)
    #pausa(1)
    driver.save_screenshot("screenshot.png")
    img=Image.open('screenshot.png')
    #Obtenemos el ancho y el largo de la imagen
    ancho = img.size[0]
    alto = img.size[1]

    imagen_capcha= driver.find_element_by_id("imagcodigo")
    #Coordenada X, Y
    coordenada = imagen_capcha.location
    #Ancho y Alto de la Imagen
    tamano = imagen_capcha.size

    posX1 = coordenada.get('x')
    posY1 = coordenada.get('y')
    posX2 = coordenada.get('x') + tamano.get('width')
    posY2 = coordenada.get('y') + tamano.get('height')

    #Recortamos la parte del captcha teniendo en cuenta el ancho y el largo de la imagen
    img_recortada = img.crop((posX1, posY1, posX2, posY2))
    #Guardamos el recorte
    img_recortada.save("recorte.png")
    #Se llama al metodo romper_captcha para obtener el texto correspondiente
    captcha = romper_captcha("recorte.png")

    try:
        #Obtenemos la caja de texto donde se escribe el texto del captcha
        codigo = driver.find_element_by_name("imagen")
        #Si el captcha esta vacio o no se ha logrado romper se cierra el navegador y se termina la aplicacion
        if captcha=='':
            crear_archivo("Error en conección a la web de la RENIEC..." + ":1")
            driver.close()
            return
        #Escribimos el texto
        codigo.send_keys(captcha)
    except:
        pass
    try:
        #Obtenemos el boton de consulta
        boton_consultar=driver.find_element_by_name("bot_consultar")
        #Damos click al boton de consulta
        boton_consultar.click()
    except:
        print ("Elemento no esta presente")
    #Obtengo el resultado que aparece en el elemento llamado style2
    resultado = driver.find_element_by_class_name("style2")
    #Partimos el resultado para obtener el nombre
    nombre = resultado.text.split('\n')

    if len(nombre) == 2:
        if nombre[1][0:8]==dni:
            crear_archivo(nombre[0]+ ":0")
        elif nombre[0][-8:]==dni:
            texto = nombre[0] + ' ' + nombre[1] + ":1"
            crear_archivo(texto)
    elif len(nombre)==1 :
        crear_archivo(nombre[0] + ":1")

    driver.close()
    return nombre[0]



def main():
    dni = argv[1]
    print("Soft.DNI V.1.0.0")
    print("procesando DNI", dni)
    nombre = ir_reniec_web(dni)
    f = open("dni.txt","r")
    texto = f.readline()
    f.close()
    lista = texto.split(":")
    print(lista[0])
main()


