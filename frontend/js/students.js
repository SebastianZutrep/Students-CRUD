const API_URL = "https://estudiantes-api-h4rx.onrender.com/students/";

document.addEventListener('DOMContentLoaded', () => {
    loadStudents();
    document.getElementById("student-form").addEventListener("submit", (e) => {
        e.preventDefault();
        saveStudents();
    });
});

function saveStudents() {
    const id       = document.getElementById("student-id").value;
    const name     = document.getElementById("name").value;
    const age      = parseInt(document.getElementById("age").value);
    const gradeRaw = document.getElementById("grade").value;
    const grade    = parseFloat(gradeRaw);

    if (!name || !age || gradeRaw === "" || isNaN(grade)) {
        alert("Por favor completa todos los campos");
        return;
    }

    const studentData = { name, age, grade };
    const method = id ? "PUT" : "POST";
    const url = id ? `${API_URL}${id}` : API_URL;

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(studentData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.detail || 'Error en la operación');
            });
        }
        return response.json();
    })
    .then(() => {
        alert("Estudiante guardado correctamente");
        document.getElementById("student-form").reset();
        document.getElementById("student-id").value = "";

        document.getElementById("submit-btn").textContent = "Guardar";
        loadStudents();
    })
    .catch(error => {
        alert("Error: " + error.message);
        console.error("Error al guardar:", error);
    });
}

function loadStudents() {
    fetch(API_URL)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            const tbody = document.getElementById("students-list");
            tbody.innerHTML = "";

            if (data.length === 0) {
                tbody.innerHTML = "<tr><td colspan='5' style='text-align:center;'>No hay estudiantes registrados</td></tr>";
                return;
            }

            data.forEach(student => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.age}</td>
                    <td>${student.grade}</td>
                    <td>
                        <div style="display:flex; flex-direction:column; gap:5px; align-items:flex-start;">
                            <button onclick="editStudent(${student.id})">Editar</button>
                            <button class="danger" onclick="deleteStudent(${student.id})">Eliminar</button>
                        </div>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error cargando estudiantes:", error);
            document.getElementById("students-list").innerHTML =
                "<tr><td colspan='5' style='text-align:center; color:red;'>Error al cargar estudiantes</td></tr>";
        });
}

function editStudent(id) {
    fetch(`${API_URL}${id}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(student => {
            document.getElementById("student-id").value  = student.id;
            document.getElementById("name").value        = student.name;
            document.getElementById("age").value         = student.age;
            document.getElementById("grade").value       = student.grade;
            document.getElementById("submit-btn").textContent = "Actualizar";
            window.scrollTo(0, 0);
        })
        .catch(error => {
            alert("Error cargando estudiante: " + error.message);
            console.error(error);
        });
}

function cancelEdit() {
    document.getElementById("student-form").reset();
    document.getElementById("student-id").value = "";
    document.getElementById("submit-btn").textContent = "Guardar";
}

function deleteStudent(id) {
    if (confirm("¿Estás seguro de que deseas eliminar este estudiante?")) {
        fetch(`${API_URL}${id}`, { method: "DELETE" })
            .then(response => {
                if (response.ok) {
                    alert("Estudiante eliminado correctamente");
                    loadStudents();
                } else {
                    return response.json().then(err => {
                        throw new Error(err.detail || "Error desconocido");
                    });
                }
            })
            .catch(error => {
                alert("Error al eliminar: " + error.message);
                console.error("Error eliminando:", error);
            });
    }
}

function cerrarSesion() {
    sessionStorage.removeItem("authenticated");
    localStorage.removeItem("user-email");
    window.location.href = "index.html";
}