import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException

# Parámetros de la cuenta de correo
SMTP_SERVER = "mail.softdesarrolladores.com"
SMTP_PORT = 465
SENDER_EMAIL = "henry@softdesarrolladores.com"
SENDER_PASSWORD = "96WmmXAj$DW_"  # Asegúrate de proteger esta información.

def send_email(subject: str, body: str, to_email: str):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    # Cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conexión segura con SMTP_SSL
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {e}")
