document.addEventListener("DOMContentLoaded", function () {
  const roleSelect = document.getElementById("roleId");
  const projectGroup = document.getElementById("project-group");
  const projectSelect = document.getElementById("projectId");
  const form = document.getElementById("editUserForm");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");

  // Función para mostrar/ocultar campo de proyecto
  function toggleProjectField() {
    if (roleSelect && roleSelect.value) {
      const selectedOption = roleSelect.options[roleSelect.selectedIndex];
      const roleName = selectedOption.text.toLowerCase();

      if (roleName.includes("estudiante")) {
        if (projectGroup) {
          projectGroup.style.display = "block";
        }
        if (projectSelect) {
          projectSelect.required = false;
        }
      } else {
        if (projectGroup) {
          projectGroup.style.display = "none";
        }
        if (projectSelect) {
          projectSelect.value = "";
          projectSelect.required = false;
        }
      }
    }
  }

  // Inicializar estado basado en el rol actual
  if (roleSelect) {
    toggleProjectField();

    // Escuchar cambios en el rol
    roleSelect.addEventListener("change", toggleProjectField);
  }

  // Validación de contraseñas (solo si se ingresó una nueva)
  if (form && password && confirmPassword) {
    form.addEventListener("submit", function (e) {
      let isValid = true;

      // Solo validar si se ingresó una contraseña
      if (password.value.trim() !== "") {
        if (password.value !== confirmPassword.value) {
          e.preventDefault();
          showNotification("Las contraseñas no coinciden", "error");
          confirmPassword.focus();
          isValid = false;
        }

        if (password.value.length < 6) {
          e.preventDefault();
          showNotification(
            "La contraseña debe tener al menos 6 caracteres",
            "error"
          );
          password.focus();
          isValid = false;
        }
      }

      // Si es válido, mostrar estado de carga
      if (isValid) {
        const submitButton = form.querySelector(".btn-submit");
        if (submitButton) {
          submitButton.disabled = true;
          submitButton.innerHTML =
            '<i class="bi bi-hourglass-split"></i> Actualizando...';
        }
      }
    });
  }

  // Función para mostrar notificaciones
  function showNotification(message, type) {
    // Crear elemento de notificación
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
            <i class="bi ${
              type === "success" ? "bi-check-circle" : "bi-exclamation-circle"
            }"></i>
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        `;

    // Estilos para la notificación
    notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === "success" ? "#10b981" : "#ef4444"};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            min-width: 300px;
            max-width: 400px;
        `;

    // Animación
    const style = document.createElement("style");
    style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
    document.head.appendChild(style);

    // Botón para cerrar
    const closeBtn = notification.querySelector(".notification-close");
    closeBtn.addEventListener("click", function () {
      notification.style.animation = "slideOut 0.3s ease";
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    });

    // Auto-eliminar después de 5 segundos
    setTimeout(() => {
      if (notification.parentNode) {
        notification.style.animation = "slideOut 0.3s ease";
        setTimeout(() => {
          if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
          }
        }, 300);
      }
    }, 5000);

    document.body.appendChild(notification);
  }
});
