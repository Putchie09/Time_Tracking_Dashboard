document.addEventListener("DOMContentLoaded", function () {
  const codeInput = document.getElementById("code");
  const form = document.getElementById("editProjectForm");

  if (codeInput) {
    codeInput.addEventListener("input", function () {
      this.value = this.value.toUpperCase();
    });

    setTimeout(() => {
      codeInput.focus();
    }, 300);
  }

  if (form) {
    form.addEventListener("submit", function () {
      const submitButton = form.querySelector(".btn-submit");
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML =
          '<i class="bi bi-hourglass-split"></i> Actualizando...';
      }
    });
  }
});
