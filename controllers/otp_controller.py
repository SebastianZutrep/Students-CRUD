# controllers/otp_controller.py — CORREGIDO

import secrets
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# Configuración 
SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER     = os.getenv("SMTP_USER", "")
SMTP_PASS     = os.getenv("SMTP_PASS", "")
FROM_NAME     = os.getenv("FROM_NAME", "Sistema de Estudiantes")

OTP_EXPIRY_MINUTES = 10


otp_storage: dict = {}


# ── Helpers ─────────────────────────────────────────────────────────

def generate_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)


def send_otp_email(email: str, code: str):
    # si no hay credenciales SMTP, imprime en consola
    if not SMTP_USER or not SMTP_PASS:
        print(f"\n{'='*40}")
        print(f"  [MODO DEV] OTP para {email}: {code}")
        print(f"  Expira en {OTP_EXPIRY_MINUTES} minutos")
        print(f"{'='*40}\n")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Tu código de verificación"
    msg["From"]    = f"{FROM_NAME} <{SMTP_USER}>"
    msg["To"]      = email

    html = f"""
    <html>
      <body style="font-family:'Segoe UI',sans-serif; background:#f4f7f6; padding:30px;">
        <div style="max-width:420px; margin:auto; background:#fff; border-radius:16px;
                    box-shadow:0 10px 30px rgba(0,0,0,.1); padding:40px; text-align:center;">

          <h2 style="color:#2d3436; margin-bottom:8px;">Código de verificación</h2>
          <p style="color:#636e72; font-size:14px; margin-bottom:28px;">
            Válido por <strong>{OTP_EXPIRY_MINUTES} minutos</strong>.
          </p>
          <div style="background:#f0fdf4; border:2px solid #45a049; border-radius:12px;
                      padding:20px; letter-spacing:12px; font-size:36px; font-weight:700;
                      color:#2d6a2f;">
            {code}
          </div>
          <p style="color:#b2bec3; font-size:12px; margin-top:24px;">
            Si no solicitaste este código, ignora este mensaje.
          </p>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        # SMTP con STARTTLS
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, email, msg.as_string())
    except Exception as e:
        print(f"Error enviando email: {e}")
        # Lanza HTTPException para que FastAPI devuelva un error legible al frontend
        raise HTTPException(
            status_code=500,
            detail="No se pudo enviar el correo. Verifica la configuración SMTP."
        )


# Controlador 

class AuthController:

    @staticmethod
    def send_otp(email: str) -> dict:
        code    = generate_otp()
        expires = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

        # Guarda código + tiempo de expiración 
        otp_storage[email] = {"code": code, "expires": expires}

        send_otp_email(email, code)
        return {"message": "Código enviado al correo"}

    @staticmethod
    def verify_otp(email: str, otp: str) -> dict:
        entry = otp_storage.get(email)

        if not entry:
            raise HTTPException(
                status_code=400,
                detail="No hay un código pendiente para este correo."
            )

        # Verificación de expiración 
        if datetime.utcnow() > entry["expires"]:
            del otp_storage[email]
            raise HTTPException(
                status_code=400,
                detail="El código ha expirado. Solicita uno nuevo."
            )

        if entry["code"] != otp:
            raise HTTPException(
                status_code=400,
                detail="Código incorrecto."
            )

        # Elimina el código para que no pueda reutilizarse
        del otp_storage[email]
        return {"valid": True, "message": "Código correcto"}