document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // evitar recarga

        const email = document.getElementById("email").value;

        if (!email) {
            alert("Por favor ingresa un correo");
            return;
        }

        try {
            const response = await fetch("/auth/send-otp", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email: email })
            });

            const data = await response.json();

            alert(data.message);

            //  guardar email para usarlo en auth.js
            localStorage.setItem("email", email);

            // redirigir a la página de verificación
            window.location.href = "/otp.html";

        } catch (error) {
            console.error(error);
            alert("Error al enviar el código");
        }
    });
});