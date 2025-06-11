document.addEventListener("DOMContentLoaded", function () {
    const socket = io();

    // El ID del paciente debería ser insertado desde el backend (ver más abajo)
    const pacienteId = document.querySelector('meta[name="paciente-id"]').content;
    console.log(`Uniéndose como paciente con ID: ${pacienteId}`) 
    // Enviar evento para unirse a la sala correspondiente
    socket.emit("unirse", {
        tipo: "paciente",
        id: pacienteId
    });

    // Recibir confirmación
    socket.on("joined", function (data) {
        console.log(data.mensaje);
    });

    // Escuchar nuevas notificaciones
    socket.on("nueva_notificacion", function (data) {
        console.log("Notificación recibida:", data.mensaje);
        mostrarNotificacion(data);
    });

    // Función para mostrar notificación en pantalla
    function mostrarNotificacion(data) {
        const contenedor = document.getElementById("zona-dinamica-notificaciones");
        
        const div = document.createElement("div");
        div.className = "notificacion";

        // Mostrar mensaje
        div.innerText = data.mensaje;

        // Agregar botón de apertura
        const boton = document.createElement("button");
        boton.innerText = "Abrir";
        boton.className = "btn-abrir";
        boton.onclick = () => marcarComoLeida(data.id, div);

        div.appendChild(document.createElement("br"));
        div.appendChild(boton);

        contenedor.prepend(div);

        // Limitar a 3
        const notificaciones = contenedor.querySelectorAll(".notificacion");
        if (notificaciones.length > 3) {
            notificaciones[3].remove();
        }
    }

    // Función para marcar como leída
    function marcarComoLeida(id, elementoDiv) {
        fetch(`/notificaciones/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ estado: "leida" })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Notificación marcada como leída:", data);
            elementoDiv.style.opacity = 0.5;
        })
        .catch(error => {
            console.error("Error al actualizar estado:", error);
        });
    }
});
