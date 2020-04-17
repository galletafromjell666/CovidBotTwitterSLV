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


##cerrar ventanas anteriores en caso de error
os.system('killall chrome')
os.system('killall chromedriver')

# bot telegram
TOKEN = '1236365617:AAHl0G1pivRLTIfRqNgdc7VVCgHdspu_mRo'
tb = telebot.TeleBot(TOKEN)
AGCHATID = -395961858
ahora = datetime.now()
notificacion = (f"Inicio del programa a las {ahora} ")
tb.send_message(AGCHATID, notificacion)
# ajustes de chromedriver
options = Options()
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
options.page_load_strategy = 'eager'


# TIEMPO DE ACTUALIZACION

tiempoactualizar = 4*60

# inicializar contadores cada vez que se empiece a ejecutar
#print("LA PRIMERA VEZ DEBE INTRODUCIR LOS DATOS ACTUALES PARA PODER EMPEZAR LA EJECUCION DEL PROGRAMA")

#BACKmuertes = int(input("INSERTE CASOS TOTALES ACTUALES "))
#BACKRECUPERADOS = int(input("INSERTE CASOS RECUPERADOS TOTALES ACTUALES "))
#BACKdeath = int(input("INSERTE MUERTES ACTUALES "))

# BUCLE QUE REVISA SI HAY CAMBIOS PARA TWITEAR
while True:
    tiempoactualizar = 2*60
    notificacion = ("Corriendo 🥰")
    tb.send_message(AGCHATID, notificacion)
    
    if limpiadorpantalla == 20:
        os.system('clear')
        limpiadorpantalla = 0

    ahora = datetime.now()
    print("")
    print("-------------------------------------------------------------------")
    print(f"Ciclo iniciado a las {ahora}")

    driver = Chrome(executable_path='/home/gio/Downloads/chromedriver', options=chrome_options)
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
            ahora = datetime.now()
            print("------ES LA PRIMERA EJECUCION NO HAY DATOS PARA SALTAR EL ERROR DEBE EJECUTARLO NUEVAMENTE-----")
            print("DETENIENDO")
            notificacion = (
                f"ERROR AL EXTRAER - PROGRAMA DETENIDO A LAS  {ahora} VOLVER A EJECUTARLO")
            tb.send_message(AGCHATID, notificacion)
            exit()
        else:
            ahora = datetime.now()
            fintotales = BACKmuertes
            finrecuperados = BACKRECUPERADOS
            finmuerte = BACKdeath
            print("ERROR EXTRAYENDO DATOS: SE USARON DATOS DE LA ANTERIOR EJECUCION")
            tiempoactualizar = 10
            notificacion = (f"ERROR AL EXTRAER  😕 - {ahora} ")
            tb.send_message(AGCHATID, notificacion)
    else:
        
        try:
            fintotales = int(str(fintotales.text))
            finrecuperados = int(str(finrecuperados.text))
            finmuerte = int(str(finmuerte.text))
            
        except:
            ahora = datetime.now()
            fintotales = BACKmuertes
            finrecuperados = BACKRECUPERADOS
            finmuerte = BACKdeath
            tiempoactualizar = 20
            print("ERROR EXTRAYENDO DATOS +ERROR DATO VACIO: SE USARON DATOS DE LA ANTERIOR EJECUCION")
            notificacion = (
                f"ERROR AL EXTRAER + ERROR DATO VACIO 🥴 {ahora} ")
            tb.send_message(AGCHATID, notificacion)

##########################
    # TEST METER DATOS MANUALMENTE PARA PROBAR
    driver.close()
    driver.quit()
    os.system('killall chrome')
    os.system('killall chromedriver')

    if False:
        fintotales = int(input("INSERTE CASOS TOTALES PRUEBA "))
        finrecuperados = int(input("INSERTE CASOS RECUPERADOS TOTALES PRUEBA "))
        finmuerte = int(input("INSERTE MUERTES PRUEBA "))
#############################

## cambiando tiempo de espera primera ejecucion
    if ejecucion == 0:
        tiempoactualizar = 10
       

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
            tweet = f'''⚠️ Covid19 Bot 🤖 El Salvador 🇸🇻
🚨 Nueva actualización 🚨

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
                print('Autentificacion exitosa de twitter')

            except:
                print('Error autenticando twitter')
                sys.exit(1)

            tweet = create_tweet()
            api.update_status(tweet)
            print('tweet publicado')
            ahora = datetime.now()
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
    else:
        
        limpiadorpantalla = limpiadorpantalla+1
        print("")
        print(f"NUEVA CANTIDAD ALMACENADA DE CASOS TOTALES {BACKmuertes}")
        print(
            f"NUEVA CANTIDAD ALMACENADA DE CASOS RECUPERADOS {BACKRECUPERADOS }")
        print(f"NUEVA CANTIDAD ALMACENADA DE MUERTES {BACKdeath}")
        ejecucion = 2
        ahora = datetime.now()
        #print("HORA =          ", ahora)
        print(f"No hubieron cambios, no se twitea nada {ahora}")

    time.sleep(tiempoactualizar)
