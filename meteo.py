#! /usr/bin/env python3
"""Envia uma notificação por SMS para com a meteorologia actual"""
import requests, bs4, datetime, time, math, threading, sys
from twilio.rest import Client

def interact():
    print("  #####################################")
    print(' #This is your wake up weather update#')
    print('#####################################')
    
    while True:
        global hora
        global sair
        console=input()
        #fazer validação se inserção de letras na hora tipo 'set alarm op:fg'
        if console[:9]=='set alarm' and console[12]==':' and int(console[10:12])>=0 and int(console[10:12])<=23 and int(console[13:15])>=0 and int(console[13:15])<=59:
            hora[0]=int(console[10:12])
            hora[1]=int(console[13:15])
        elif console[:5]=='set alarm' and console[12]==':':
            print("That's not a valid 24 hour time. Try again with 'set alarm hh:mm'")
        elif console=='alarm status':
            #estado alarme
            alarme=hora[1]/60+hora[0]
            actual=agora.minute/60+agora.hour
            if alarme>actual:
                falta=alarme-actual
                falta_hora=math.floor(falta)
                falta_minutos=round((falta-math.floor(falta))*60)
                print("not yet,",falta_hora,"hours and",falta_minutos," minutes still to go...")
            else:
                falta=24-abs(alarme-actual)
                falta_hora=math.floor(falta)
                falta_minutos=round((falta-math.floor(falta))*60)
                print("not yet, alarm set to ",hora[0],":",hora[1],"\n"+str(falta_hora),"hours and",falta_minutos," minutes still to go...")
        elif console=='exit':
            sair=True
            sys.exit()
        else:
            print("type 'set alarm hh:mm' to set the alarm\ntype 'alarm status' to check the alarm time")

#pré-definição de alarme
hora=[0,0]
#sair?
sair=False
#inicia thread da consola
consola=threading.Thread(target=interact)
consola.start()

#ciclo de verificação de hora
while True:
    if sair==True:
        sys.exit()
    agora=datetime.datetime.now()
    #na hora do alarme
    if agora.hour==hora[0] and agora.minute==hora[1]:
        #scraper
        site="http://meteofontes.cm-lagoa.pt"
        meteo=requests.get(site)
        try:
            meteo.raise_for_status() 
        except Exception as excep:
            print('There was a problemo: ', excep)
        texto=bs4.BeautifulSoup(meteo.text,features="html.parser")
        data1=texto.select(".row-a")
        data2=texto.select(".row-b")
        #obtenção mensagem
        sms=""
        for i in range(0,5):
            sms=sms+" ".join(data1[i].getText().split())
            sms=sms+"\n"
            sms=sms+" ".join(data2[i].getText().split())
            sms=sms+"\n"
        #envio da mensagem
        """
        accountSID="ACa2f8c346d9e569497ccc5aa332132aaa"
        authToken="b6ef51b7d2417aa17c4455f2c0f5441d"
        dest=Client(accountSID, authToken)
        myTwilioNumber='+12034635590'
        myCellPhone='+351910304364'
        message=dest.messages.create(body=sms,from_=myTwilioNumber,to=myCellPhone)
        """
        print(sms)
        #evitar que envie várias mensagens no minuto
        time.sleep(61)
    #verificação ciclica em pausa
    time.sleep(1)