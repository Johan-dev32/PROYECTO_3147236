// registroTutorias.js

// Guardar los datos del formulario en localStorage
function guardarTutoria() {
  const tutoria = {
    nombre: document.getElementById("nombre").value,
    rol: document.getElementById("rol").value,
    tema: document.getElementById("Tema").value,
    fecha: document.getElementById("fecha").value,
    curso: document.querySelector("select.form-select").value,
    estudiante: document.getElementById("nombre_estudiante").value,
    correo: document.getElementById("correo").value,
    motivo: document.getElementById("motivo").value,
    observaciones: document.getElementById("observaciones").value 
  };

  let tutorias = JSON.parse(localStorage.getItem("tutorias")) || [];
  tutorias.push(tutoria);
  localStorage.setItem("tutorias", JSON.stringify(tutorias));

  // Redirigir a la tabla
  window.location.href = "/registrotutorias"; // ajusta según tu ruta Flask
}

// Mostrar los datos guardados en la tabla
function mostrarTutorias() {
  const tabla = document.querySelector(".tabla-tutorias");
  if (!tabla) return; // si no existe la tabla, salir

  let tutorias = JSON.parse(localStorage.getItem("tutorias")) || [];

  tutorias.forEach(t => {
    let fila = `
      <tr>
        <td>${t.nombre}</td>
        <td>${t.rol}</td>
        <td>${t.tema}</td>
        <td>${t.fecha}</td>
        <td>${t.curso}</td>
        <td>${t.estudiante}</td>
        <td>${t.correo}</td>
        <td>${t.motivo}</td>
        <td>${t.observaciones}</td>
      </tr>
    `;
    tabla.innerHTML += fila;
  });
}

// Llamar a mostrarTutorias cuando cargue registrotutorias.html
document.addEventListener("DOMContentLoaded", mostrarTutorias);
