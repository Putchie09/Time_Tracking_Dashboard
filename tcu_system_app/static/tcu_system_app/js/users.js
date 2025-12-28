document.addEventListener("DOMContentLoaded", function () {
  // Búsqueda de usuarios
  const searchInput = document.getElementById("search-users");
  if (searchInput) {
    searchInput.addEventListener("input", function (e) {
      const searchTerm = e.target.value.toLowerCase();
      const rows = document.querySelectorAll("#users-table tbody tr");

      rows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? "" : "none";
      });
    });
  }

  // Manejo de eliminación de usuarios
  const deleteButtons = document.querySelectorAll(".btn-delete[data-user-id]");
  const deleteModal = document.getElementById("deleteModal");
  const modalClose = deleteModal.querySelector(".modal-close");
  const cancelButton = deleteModal.querySelector(".btn-cancel");
  const confirmDeleteButton = deleteModal.querySelector(".btn-confirm-delete");

  let userIdToDelete = null;

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      userIdToDelete = this.getAttribute("data-user-id");
      deleteModal.style.display = "flex";
    });
  });

  // Cerrar modal
  modalClose.addEventListener("click", () => {
    deleteModal.style.display = "none";
    userIdToDelete = null;
  });

  cancelButton.addEventListener("click", () => {
    deleteModal.style.display = "none";
    userIdToDelete = null;
  });

  // Confirmar eliminación
  confirmDeleteButton.addEventListener("click", () => {
    if (userIdToDelete) {
      confirmDeleteButton.disabled = true;
      confirmDeleteButton.textContent = "Eliminando...";

      // Realizar llamada AJAX para eliminar
      fetch(`/users/delete/${userIdToDelete}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}), 
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            showNotification(data.message, "success");

            // Eliminar la fila de la tabla
            const row = document
              .querySelector(`[data-user-id="${userIdToDelete}"]`)
              .closest("tr");
            if (row) {
              row.remove();

              // Verificar si quedan filas
              const tableBody = document.querySelector("#users-table tbody");
              if (tableBody && tableBody.children.length === 0) {
                // Si no hay más usuarios, recargar la página para mostrar el estado vacío
                setTimeout(() => {
                  location.reload();
                }, 1500);
              }
            }
          } else {
            // Mostrar error
            showNotification(
              data.error || "Error al eliminar el usuario",
              "error"
            );
          }

          // Cerrar modal
          deleteModal.style.display = "none";
          userIdToDelete = null;

          // Restablecer botón
          confirmDeleteButton.disabled = false;
          confirmDeleteButton.textContent = "Eliminar Usuario";
        })
        .catch((error) => {
          console.error("Error:", error);
          showNotification("Error de conexión al eliminar el usuario", "error");

          // Restablecer botón
          confirmDeleteButton.disabled = false;
          confirmDeleteButton.textContent = "Eliminar Usuario";
        });
    }
  });

  // Función para obtener el token CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
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

  // Cerrar modal al hacer clic fuera
  deleteModal.addEventListener("click", function (e) {
    if (e.target === deleteModal) {
      deleteModal.style.display = "none";
      userIdToDelete = null;
    }
  });
});
