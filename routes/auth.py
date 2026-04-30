from fastapi import APIRouter
from pydantic import BaseModel
from controllers.otp_controller import AuthController

router = APIRouter(prefix="/auth")

class EmailRequest(BaseModel):
    email: str

class OTPRequest(BaseModel):
    email: str
    otp: str

@router.post("/send-otp")
def send_otp(request: EmailRequest):
    return AuthController.send_otp(request.email)

@router.post("/verify-otp")
def verify_otp(request: OTPRequest):
    return AuthController.verify_otp(request.email, request.otp)