# Autores: Juan Campos - Giovanni Aguirre

from os import path
import sys
from datetime import datetime
import os
import telebot
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import tweepy
import requests
from lxml import html

limpiadorpantalla = 0
ejecucion = 0

ubicacionchromedriver = path.relpath("chromedriverfiles/chromedriver")

# bot telegram
TOKEN = '1236365617:AAHl0G1pivRLTIfRqNgdc7VVCgHdspu_mRo'
tb = telebot.TeleBot(TOKEN)
AGCHATID = 715725112
ahora = datetime.now()
options = Options()
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
options.page_load_strategy = 'eager'
notificacion = (f"Inicio del programa a las {ahora} ")
tb.send_message(AGCHATID, notificacion)

# TIEMPO DE ACTUALIZACION

tiempoactualizar = 5*60

# inicializar contadores cada vez que se empiece a ejecutar
#print("LA PRIMERA VEZ DEBE INTRODUCIR LOS DATOS ACTUALES PARA PODER EMPEZAR LA EJECUCION DEL PROGRAMA")

#BACKmuertes = int(input("INSERTE CASOS TOTALES ACTUALES "))
#BACKRECUPERADOS = int(input("INSERTE CASOS RECUPERADOS TOTALES ACTUALES "))
#BACKdeath = int(input("INSERTE MUERTES ACTUALES "))

# BUCLE QUE REVISA SI HAY CAMBIOS PARA TWITEAR
while True:
    ahora = datetime.now()
    driver = Chrome(executable_path=ubicacionchromedriver, chrome_options=chrome_options)
    driver.get("https://e.infogram.com/_/fx5xud0FhM7Z9NS6qpxs?parent_url=https%3A%2F%2Fcovid19.gob.sv%2F&src=embed#async_embed")
    recuperados = driver.find_elements_by_tag_name('span')
    try:
        fintotales = recuperados[12]
        finrecuperados = recuperados[14]
        finmuerte = recuperados[16]
        cofirmados = recuperados[19]
    except:
        print("-----ERROR EXTRAYENDO DATOS-----")
        if ejecucion == 0:
            print("------ES LA PRIMERA EJECUCION NO HAY DATOS PARA SALTAR EL ERROR DEBE EJECUTARLO NUEVAMENTE-----")
            print("DETENIENDO")
            notificacion = (
                f"ERROR AL EXTRAER - PROGRAMA DETENIDO A LAS  {ahora} ")
            tb.send_message(AGCHATID, notificacion)
            driver.close()
            exit()
        else:
            fintotales = BACKmuertes
            finrecuperados = BACKRECUPERADOS
            finmuerte = BACKdeath
            tiempoactualizar = 60
            print(f"intdeath es {intdeath}")
            print("dentro else")
            notificacion = (f"ERROR AL EXTRAER - {ahora} ")
            tb.send_message(AGCHATID, notificacion)
            driver.close()
    else:
        tiempoactualizar = 5*60
        fintotales = int(str(fintotales.text))
        finrecuperados = int(str(finrecuperados.text))
        finmuerte = int(str(finmuerte.text))
        driver.close()
    # print(rec.text)

##########################
    # TEST METER DATOS MANUALMENTE PARA PROBAR
    if False:
        fintotales = int(input("INSERTE CASOS TOTALES PRUEBA "))
        finrecuperados = int(input("INSERTE CASOS RECUPERADOS TOTALES PRUEBA "))
        finmuerte = int(input("INSERTE MUERTES PRUEBA "))
#############################
    # contador de total casos
    intmuerte = fintotales
    if ejecucion == 0:
        BACKmuertes = intmuerte

    difmuertes = intmuerte-BACKmuertes

    print(f"casos totales {intmuerte}")
    print(f"diferencia de totales {intmuerte}-{BACKmuertes}  =  {difmuertes}")

    # contador muertes
    intdeath = finmuerte
    if ejecucion == 0:
        BACKdeath = intdeath

    difdeath = intdeath-BACKdeath
    print(f"muertes totales {intdeath}")
    print(f"diferencia de muertes {intdeath}-{BACKdeath}  =  {difdeath}")

    # contados recuperados
    intrecuperados = finrecuperados
    if ejecucion == 0:

        # cambiando el tiempo de actualizacion la primera vez para no esperar mucho
        tiempoactualizar = 10
        BACKRECUPERADOS = intrecuperados

    difrecuperados = intrecuperados-BACKRECUPERADOS
    print(f"recuperados totales {intrecuperados}")
    print(
        f"diferencia de recuperados {intrecuperados}-{BACKRECUPERADOS}  =  {difrecuperados}")

    print(f"limpiador {limpiadorpantalla}")

    # evaluar si se crea el tweet o no
    # difrecuperados != 0 or difmuertes != 0 or difdeath !=0
    if difrecuperados != 0 or difmuertes != 0 or difdeath != 0:
        # evaluar que publicar
        if difmuertes != 0:
            txtotal = "Casos nuevos: "+str(difmuertes)
        else:
            txtotal = ""

        if difdeath != 0:
            txtmuerte = "Muertes nuevas: "+str(difdeath)
        else:
            txtmuerte = ""

        if difrecuperados != 0:
            txtrecover = "Recuperados nuevos: "+str(difrecuperados)
        else:
            txtrecover = ""

            # crear tweet
        def create_tweet():

            tempo = datetime.now()
            dia = tempo.day
            mes = tempo.month
            hora = tempo.hour
            tweet = f'''⚠️ Coronavirus El Salvador 🇸🇻

📆{dia}/{mes} ⌚{hora}H

{txtotal}
Casos totales: {fintotales} 

{txtrecover} 
Total recuperados: {finrecuperados}

{txtmuerte}
Total muertes: {finmuerte} 
        
Fuente: 
https://covid19.gob.sv/
    
#QuédateEnCasa #AlertaCOVID19SV 
        '''
            return tweet

        if __name__ == '__main__':
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

            # Create API object
            api = tweepy.API(auth)

            try:
                api.verify_credentials()
                print('Authentication Successful')

            except:
                print('Error while authenticating API')
                sys.exit(1)

            tweet = create_tweet()
            api.update_status(tweet)
            print('Tweet successful')
            notificacion = (f"Nueva Publicacion! {ahora}  {tweet}")
            tb.send_message(AGCHATID, notificacion)
            BACKmuertes = intmuerte
            BACKRECUPERADOS = intrecuperados
            BACKdeath = intdeath
            print(tweet)
            print(f"NUEVA CANTIDAD ALMACENADA DE CASOS TOTALES {BACKmuertes}")
            print(
                f"NUEVA CANTIDAD ALMACENADA DE CASOS RECUPERADOS {BACKRECUPERADOS }")
            print(f"NUEVA CANTIDAD ALMACENADA DE MUERTES {BACKdeath}")
            limpiadorpantalla = limpiadorpantalla+1
            ejecucion = 2
            ahora = datetime.now()
            print("HORA =       ", ahora)
    else:
        print("No hubieron cambios, no se twitea nada")
        limpiadorpantalla = limpiadorpantalla+1
        print(f"NUEVA CANTIDAD ALMACENADA DE CASOS TOTALES {BACKmuertes}")
        print(
            f"NUEVA CANTIDAD ALMACENADA DE CASOS RECUPERADOS {BACKRECUPERADOS }")
        print(f"NUEVA CANTIDAD ALMACENADA DE MUERTES {BACKdeath}")
        ejecucion = 2
        ahora = datetime.now()
        print("HORA =          ", ahora)

# limpia la pantalla cuando se tiene X registros
    if limpiadorpantalla == 20:
        os.system('clear')
        print("pantalla limpia")
        limpiadorpantalla = 0

    time.sleep(tiempoactualizar)
