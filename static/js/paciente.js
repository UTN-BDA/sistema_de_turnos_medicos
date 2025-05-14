document.addEventListener("DOMContentLoaded", function () {
    const socket = io();

    // El ID del paciente debería ser insertado desde el backend (ver más abajo)
    const pacienteId = window.pacienteId;

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
        mostrarNotificacion(data.mensaje);
    });

    // Función para mostrar notificación en pantalla
    function mostrarNotificacion(mensaje) {
        const contenedor = document.getElementById("contenedor-notificaciones");
        const div = document.createElement("div");
        div.className = "notificacion";
        div.innerText = mensaje;

        contenedor.prepend(div);

        // Opcional: desaparecer luego de unos segundos
        setTimeout(() => {
            div.remove();
        }, 10000);
    }
});
