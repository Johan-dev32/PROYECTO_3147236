document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("registroForm");
  const mensajeExito = document.getElementById("mensajeExito");

  const nombres = document.getElementById("nombres");
  const apellidos = document.getElementById("apellidos");
  const correoPersonal = document.getElementById("correoPersonal");
  const correoInstitucional = document.getElementById("correoInstitucional");
  const contrasena = document.getElementById("contrasena");
  const numDoc = document.getElementById("numDoc");
  const telefono = document.getElementById("telefono");

  function mostrarError(id, mensaje) {
    const errorSpan = document.getElementById(id);
    if (errorSpan) {
      errorSpan.textContent = mensaje;
    }
  }

  function limpiarErrores() {
    document.querySelectorAll(".error").forEach(el => el.textContent = "");
  }

  const soloLetras = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
  const soloNumeros = /^[0-9]+$/;

  nombres.addEventListener("input", function () {
    if (!soloLetras.test(this.value) && this.value !== "") {
      mostrarError("errorNombres", "Solo se permiten letras");
    } else {
      mostrarError("errorNombres", "");
    }
    this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, "");
  });

  apellidos.addEventListener("input", function () {
    if (!soloLetras.test(this.value) && this.value !== "") {
      mostrarError("errorApellidos", "Solo se permiten letras");
    } else {
      mostrarError("errorApellidos", "");
    }
    this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, "");
  });

  numDoc.addEventListener("input", function () {
    if (!soloNumeros.test(this.value) && this.value !== "") {
      mostrarError("errorNumDoc", "Solo se permiten números");
    } else {
      mostrarError("errorNumDoc", "");
    }
    this.value = this.value.replace(/\D/g, "");
  });

  telefono.addEventListener("input", function () {
    if (!soloNumeros.test(this.value) && this.value !== "") {
      mostrarError("errorTelefono", "Solo se permiten números");
    } else {
      mostrarError("errorTelefono", "");
    }
    this.value = this.value.replace(/\D/g, "");
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault(); 
    let valido = true;
    limpiarErrores();

    const formatoCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (nombres.value.trim() === "") {
      mostrarError("errorNombres", "Este campo es obligatorio");
      valido = false;
    }

    if (apellidos.value.trim() === "") {
      mostrarError("errorApellidos", "Este campo es obligatorio");
      valido = false;
    }

    if (!formatoCorreo.test(correoPersonal.value.trim())) {
      mostrarError("errorCorreoPersonal", "Correo inválido");
      valido = false;
    }

    if (!formatoCorreo.test(correoInstitucional.value.trim())) {
      mostrarError("errorCorreoInstitucional", "Correo inválido");
      valido = false;
    }

    if (contrasena.value.trim().length < 8) {
      mostrarError("errorContrasena", "Mínimo 8 caracteres");
      valido = false;
    }

    const docSeleccionado = document.querySelector('input[name="doc"]:checked');
    if (!docSeleccionado) {
      mostrarError("errorDoc", "Seleccione un tipo de documento");
      valido = false;
    }

    if (numDoc.value.trim() === "") {
      mostrarError("errorNumDoc", "Este campo es obligatorio");
      valido = false;
    }

    if (telefono.value.trim() === "") {
      mostrarError("errorTelefono", "Este campo es obligatorio");
      valido = false;
    }

    const sexoSeleccionado = document.querySelector('input[name="sexo"]:checked');
    if (!sexoSeleccionado) {
      mostrarError("errorSexo", "Seleccione un sexo");
      valido = false;
    }

    const rolSeleccionado = document.querySelector('input[name="rol"]:checked');
    if (!rolSeleccionado) {
      mostrarError("errorRol", "Seleccione un rol");
      valido = false;
    }

    if (valido) {
      mensajeExito.style.display = "block";
      setTimeout(() => mensajeExito.style.display = "none", 5000);
      form.reset();
    }
  });
});
