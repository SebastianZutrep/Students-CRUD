# controllers/otp_controller.py
# controllers/otp_controller.py
import secrets
import os
import requests
import redis
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# Config Resend
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "onboarding@resend.dev")

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
    Envía correo usando Resend API
    """

    # Modo desarrollo (sin API key)
    if not RESEND_API_KEY:
        print(f"\n[MODO DEV] OTP para {email}: {code}\n")
        return

    url = "https://api.resend.com/emails"

    html = f"""
    <div style="font-family:Arial; padding:20px">
        <h2>Código de verificación</h2>
        <p>Tu código es:</p>
        <h1 style="letter-spacing:5px">{code}</h1>
        <p>Expira en {OTP_EXPIRY_MINUTES} minutos.</p>
    </div>
    """

    payload = {
        "from": FROM_EMAIL,
        "to": [email],
        "subject": "Código de verificación",
        "html": html
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code >= 400:
            print("Error Resend:", response.text)
            raise HTTPException(
                status_code=500,
                detail="Error enviando correo con Resend"
            )

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