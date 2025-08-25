document.getElementById("loginBtn").addEventListener("click", function() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (email === "" || password === "") {
    alert("Por favor, completa todos los campos.");
    return;
  }

  
  const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  if (!emailRegex.test(email)) {
    alert("Por favor, ingresa un correo válido.");
    return;
  }

  
  window.location.href = "http://127.0.0.1:5500/template/Paginainicio.html";
});
