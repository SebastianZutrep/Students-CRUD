# controllers/otp_controller.py
import secrets
import os
import smtplib
import redis
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# Config Brevo SMTP
SMTP_HOST     = os.getenv("SMTP_HOST", "smtp-relay.brevo.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER     = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL    = os.getenv("FROM_EMAIL", "aa9736001@smtp-brevo.com")

OTP_EXPIRY_MINUTES = 10

# Config Redis
REDIS_HOST     = os.getenv("REDIS_HOST")
REDIS_PORT     = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

try:
    if REDIS_HOST and REDIS_PASSWORD:
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=False
        )
        print(f"[REDIS] Conectado OK: {REDIS_HOST}")
    else:
        print("[REDIS] Variables no configuradas, Redis desactivado.")
        r = None
except Exception as e:
    print(f"[REDIS] Error al conectar: {e}")
    r = None


# ── Helpers ─────────────────────────────────────────────

def generate_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)


def send_otp_email(email: str, code: str):
    """
    Envía correo usando Brevo SMTP
    """

    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"\n[MODO DEV] OTP para {email}: {code}\n")
        return

    html = f"""
    <div style="font-family:Arial; padding:20px">
        <h2>Código de verificación</h2>
        <p>Tu código es:</p>
        <h1 style="letter-spacing:5px">{code}</h1>
        <p>Expira en {OTP_EXPIRY_MINUTES} minutos.</p>
    </div>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Código de verificación"
        msg["From"]    = FROM_EMAIL
        msg["To"]      = email
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, email, msg.as_string())

        print(f"[BREVO] Correo enviado a {email}")

    except Exception as e:
        print("Error enviando email:", e)
        raise HTTPException(
            status_code=500,
            detail="No se pudo enviar el correo"
        )


# ── Controller ─────────────────────────────────────────

class AuthController:

    @staticmethod
    def send_otp(email: str) -> dict:
        email = email.strip().lower()
        code = generate_otp()

        if r:
            r.setex(f"otp:{email}", OTP_EXPIRY_MINUTES * 60, code)
        else:
            print(f"\n[MODO DEV - SIN REDIS] OTP para {email}: {code}\n")

        send_otp_email(email, code)

        print("SEND EMAIL:", repr(email))
        print("GENERATED OTP:", code)

        return {"message": "Código enviado al correo"}


    @staticmethod
    def verify_otp(email: str, otp: str) -> dict:
        email = email.strip().lower()

        if not r:
            raise HTTPException(
                status_code=500,
                detail="Redis no configurado"
            )

        stored = r.get(f"otp:{email}")

        if not stored:
            raise HTTPException(
                status_code=400,
                detail="No hay código pendiente o ya expiró"
            )

        if stored.decode() != otp:
            raise HTTPException(
                status_code=400,
                detail="Código incorrecto"
            )

        r.delete(f"otp:{email}")

        print("VERIFY EMAIL:", repr(email))
        print("RECEIVED OTP:", otp)

        return {"valid": True, "message": "Código correcto"}