document.addEventListener("DOMContentLoaded", function () {
  const codeInput = document.getElementById("code");
  const form = document.getElementById("createProjectForm");

  // Auto-mayúsculas para el código
  if (codeInput) {
    codeInput.addEventListener("input", function () {
      this.value = this.value.toUpperCase();
    });

    // Auto-focus en el primer campo
    setTimeout(() => {
      codeInput.focus();
    }, 300);
  }

  // Mostrar estado de carga al enviar
  if (form) {
    form.addEventListener("submit", function () {
      const submitButton = form.querySelector(".btn-submit");
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML =
          '<i class="bi bi-hourglass-split"></i> Creando...';
      }
    });
  }
});
