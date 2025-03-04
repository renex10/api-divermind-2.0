#utilidades\utilidades.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

#### MODULOS REUTILIZABLES 
#### FUNCIONALIDAD QUE PERMITE ENVIAR CORREO
def sendMail(html, asunto, para):
    msg = MIMEMultipart('alternative')  # Corrige el error tipográfico aquí
    msg['Subject'] = asunto
    msg['From'] = os.getenv("SMTP_USER")
    msg['To'] = para
    
    msg.attach(MIMEText(html, 'html'))
    
    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_USER"), para, msg.as_string())
        server.quit()
    except smtplib.SMTPResponseException as e:
        print("Error al enviar el email:", e)