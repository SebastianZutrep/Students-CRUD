
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("auth-form");
    const inputs = document.querySelectorAll(".otp-inputs input");



    // Navegación entre cajas de autenticación
    inputs.forEach((input, i) => {
        // Al escribir un dígito, saltar al siguiente
        input.addEventListener("input", (e) => {
            const val = e.target.value.replace(/\D/g, "");
            e.target.value = val;
            if (val && i < inputs.length - 1) {
                inputs[i + 1].focus();
            }
        });

        // borrar y volver al anterior
        input.addEventListener("keydown", (e) => {
            if (e.key === "Backspace" && !input.value && i > 0) {
                inputs[i - 1].focus();
            }
        });

        // Pegar código completo 
        input.addEventListener("paste", (e) => {
            e.preventDefault();
            const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6);
            pasted.split("").forEach((char, idx) => {
                if (inputs[idx]) inputs[idx].value = char;
            });
            const lastIndex = Math.min(pasted.length, inputs.length - 1);
            inputs[lastIndex].focus();
        });
    });

    // Leer los 6 inputs y armar el código ─
    function getCode() {
        return Array.from(inputs).map(i => i.value).join("");
    }

    // Submit 
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const otp = getCode();
        const email = localStorage.getItem("email");

        if (!email) {
            alert("No se encontró el correo. Vuelve al login.");
            window.location.href = "/";
            return;
        }

        if (otp.length !== 6) {
            alert("Por favor ingresa los 6 dígitos del código.");
            return;
        }

        try {
            const response = await fetch("/auth/verify-otp", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, otp })
            });

            const data = await response.json();

            if (data.valid) {
                localStorage.removeItem("email");
                sessionStorage.setItem("authenticated", "true");
                window.location.href = "/students.html";
            } else {
                alert(data.message || "Código incorrecto.");
                inputs.forEach(i => { i.value = ""; });
                inputs[0].focus();
            }

        } catch (error) {
            console.error(error);
            alert("Error en la verificación.");
        }
    });

    // Reenviar código 
    const resendLink = document.querySelector(".resend-link");
    let cooldown = 0;

    resendLink.addEventListener("click", async (e) => {
        e.preventDefault();
        if (cooldown > 0) return;

        const email = localStorage.getItem("email");
        if (!email) return;

        try {
            const res = await fetch("/auth/send-otp", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email })
            });
            const data = await res.json();
            alert(data.message || "Código reenviado.");
            inputs.forEach(i => { i.value = ""; });
            inputs[0].focus();
            startCooldown(60);
        } catch {
            alert("Error al reenviar el código.");
        }
    });

    function startCooldown(seconds) {
        cooldown = seconds;
        resendLink.style.opacity = "0.4";
        resendLink.style.pointerEvents = "none";
        resendLink.textContent = `Reenviar código (${cooldown}s)`;

        const interval = setInterval(() => {
            cooldown--;
            resendLink.textContent = cooldown > 0
                ? `Reenviar código (${cooldown}s)`
                : "Reenviar código";

            if (cooldown <= 0) {
                clearInterval(interval);
                resendLink.style.opacity = "1";
                resendLink.style.pointerEvents = "auto";
            }
        }, 1000);
    }

    // Enfocar el primer input al cargar
    inputs[0].focus();
});