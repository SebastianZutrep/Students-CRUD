# 🎓 Sistema de Gestión de Estudiantes

Aplicación web full-stack con autenticación segura por OTP (One-Time Password) vía correo electrónico, construida con **FastAPI** en el backend y **HTML/CSS/JS vanilla** en el frontend, desplegada en **Render**.

🔗 **Demo en vivo:** [https://estudiantes-api-h4rx.onrender.com](https://estudiantes-api-h4rx.onrender.com)

---

## ✨ Características

- 🔐 Autenticación sin contraseña mediante código OTP de 6 dígitos
- 📧 Envío de correos transaccionales con [Resend](https://resend.com)
- ⏱️ Códigos con expiración automática de 10 minutos
- 🗄️ Persistencia de OTPs en Redis (Upstash) — sobrevive reinicios del servidor
- 🔁 Botón de reenvío con cooldown de 60 segundos
- 📋 Soporte para pegar el código completo desde el portapapeles
- 📱 Diseño responsive para móvil, tablet y escritorio
- 🚀 Desplegado en Render con variables de entorno seguras

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python · FastAPI |
| Frontend | HTML · CSS · JavaScript (Vanilla) |
| Autenticación | OTP por correo (Resend API) |
| Almacenamiento OTP | Redis (Upstash) |
| Despliegue | Render |

---

## 📁 Estructura del Proyecto

```
├── main.py                  # Entrada de la aplicación FastAPI
├── controllers/
│   └── otp_controller.py    # Lógica de generación y verificación OTP
├── routes/
│   └── auth.py              # Endpoints /auth/send-otp y /auth/verify-otp
├── static/
│   ├── index.html           # Página de login (ingreso de correo)
│   ├── otp.html             # Página de verificación OTP
│   ├── students.html        # Página principal (protegida)
│   ├── css/
│   │   └── students.css     # Estilos responsive
│   └── js/
│       ├── otp.js           # Lógica del formulario OTP
│       └── students.js      # Lógica CRUD de estudiantes
├── .env                     # Variables de entorno (no subir a Git)
├── requirements.txt         # Dependencias Python
└── README.md
```

---

## 🔄 Flujo de Autenticación

```
Usuario ingresa correo
        │
        ▼
POST /auth/send-otp
  · Genera código de 6 dígitos (criptográficamente seguro)
  · Lo guarda en Redis con TTL de 10 minutos
  · Envía correo vía Resend API
        │
        ▼
Usuario recibe el código en su correo
        │
        ▼
POST /auth/verify-otp
  · Busca el código en Redis por clave otp:{email}
  · Compara con lo ingresado
  · Si es válido → elimina de Redis y redirige a /students.html
  · Si es inválido o expiró → devuelve error 400
```

---

## ⚙️ Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
RESEND_API_KEY=tu_api_key
FROM_EMAIL=onboarding@resend.dev
REDIS_URL="rediss://default:..."
```

| Variable | Descripción |
|----------|-------------|
| `RESEND_API_KEY` | API Key de [resend.com](https://resend.com) para enviar correos |
| `FROM_EMAIL` | Dirección de origen de los correos (por defecto `onboarding@resend.dev`) |
| `REDIS_URL` | URL completa de conexión a Redis (Upstash recomendado) |

---

## 🚀 Instalación y Ejecución Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tus credenciales reales
```

### 4. Correr el servidor

```bash
uvicorn main:app --reload
```

La app estará disponible en `http://localhost:8000`

---

## 📦 Dependencias Principales

```txt
fastapi
uvicorn
python-dotenv
requests
redis==6.1.1
```

---

## 🔒 Seguridad

- Los códigos OTP se generan con `secrets.randbelow()` (criptográficamente seguro)
- Los códigos expiran en 10 minutos automáticamente vía TTL de Redis
- Cada código es de un solo uso — se elimina de Redis tras verificarse
- El correo se normaliza a minúsculas en todos los endpoints para evitar inconsistencias
- El email se guarda en `localStorage` solo durante el flujo de autenticación y se elimina al completarlo
- Las variables sensibles se manejan con `.env` y nunca se suben al repositorio

---

## 📮 Endpoints de la API

### `POST /auth/send-otp`

Genera y envía un código OTP al correo indicado.

**Body:**
```json
{ "email": "usuario@ejemplo.com" }
```

**Respuesta:**
```json
{ "message": "Código enviado al correo" }
```

---

### `POST /auth/verify-otp`

Verifica el código ingresado por el usuario.

**Body:**
```json
{ "email": "usuario@ejemplo.com", "otp": "482910" }
```

**Respuesta exitosa:**
```json
{ "valid": true, "message": "Código correcto" }
```

**Respuesta fallida (HTTP 400):**
```json
{ "detail": "Código incorrecto" }
```

---

### CRUD Estudiantes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/students/` | Lista todos los estudiantes |
| `POST` | `/students/` | Crea un estudiante |
| `PUT` | `/students/{id}` | Actualiza un estudiante |
| `DELETE` | `/students/{id}` | Elimina un estudiante |

---

## ☁️ Despliegue en Render

1. Conecta tu repositorio de GitHub en [render.com](https://render.com)
2. Crea un nuevo **Web Service**
3. Configura las variables de entorno en el panel **Environment**
4. El comando de inicio es:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

---

## 📱 Responsive Design

| Breakpoint | Comportamiento |
|-----------|---------------|
| Escritorio (> 768px) | Layout completo con tabla y formulario |
| Tablet (≤ 768px) | Padding reducido, fuentes ajustadas |
| Móvil (≤ 480px) | Botones apilados, columna ID oculta, tabla adaptada |

---

## 👨‍💻 Autor

Desarrollado como proyecto universitario.
