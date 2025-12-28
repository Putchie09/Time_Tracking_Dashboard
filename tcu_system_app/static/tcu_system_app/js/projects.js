document.addEventListener("DOMContentLoaded", function () {
  // Búsqueda de proyectos
  const searchInput = document.getElementById("search-projects");
  if (searchInput) {
    searchInput.addEventListener("input", function (e) {
      const searchTerm = e.target.value.toLowerCase();
      const rows = document.querySelectorAll("#projects-table tbody tr");

      rows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? "" : "none";
      });
    });
  }

  // Manejo de eliminación de proyectos
  const deleteButtons = document.querySelectorAll(
    ".btn-delete[data-project-id]"
  );
  const deleteModal = document.getElementById("deleteModal");
  const modalClose = deleteModal.querySelector(".modal-close");
  const cancelButton = deleteModal.querySelector(".btn-cancel");
  const confirmDeleteButton = deleteModal.querySelector(".btn-confirm-delete");

  let projectIdToDelete = null;

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      projectIdToDelete = this.getAttribute("data-project-id");
      const projectName =
        this.closest("tr").querySelector(".project-name").textContent;

      // Actualizar mensaje del modal
      const modalBody = deleteModal.querySelector(".modal-body p:first-child");
      modalBody.textContent = `¿Estás seguro de que quieres eliminar el proyecto "${projectName}"?`;

      deleteModal.style.display = "flex";
    });
  });

  // Cerrar modal
  modalClose.addEventListener("click", () => {
    deleteModal.style.display = "none";
    projectIdToDelete = null;
  });

  cancelButton.addEventListener("click", () => {
    deleteModal.style.display = "none";
    projectIdToDelete = null;
  });

  // Confirmar eliminación
  confirmDeleteButton.addEventListener("click", () => {
    if (projectIdToDelete) {
      // Deshabilitar botón mientras se procesa
      confirmDeleteButton.disabled = true;
      confirmDeleteButton.textContent = "Eliminando...";

      // Realizar llamada AJAX para eliminar
      fetch(`/projects/delete/${projectIdToDelete}/`, {
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
            // Mostrar notificación de éxito
            showNotification(data.message, "success");

            // Eliminar la fila de la tabla
            const row = document
              .querySelector(`[data-project-id="${projectIdToDelete}"]`)
              .closest("tr");
            if (row) {
              row.remove();

              // Verificar si quedan filas
              const tableBody = document.querySelector("#projects-table tbody");
              if (tableBody && tableBody.children.length === 0) {
                // Si no hay más proyectos, recargar la página para mostrar el estado vacío
                setTimeout(() => {
                  location.reload();
                }, 1500);
              }
            }
          } else {
            // Mostrar error
            showNotification(
              data.error || "Error al eliminar el proyecto",
              "error"
            );
          }

          // Cerrar modal
          deleteModal.style.display = "none";
          projectIdToDelete = null;

          // Restablecer botón
          confirmDeleteButton.disabled = false;
          confirmDeleteButton.textContent = "Eliminar Proyecto";
        })
        .catch((error) => {
          console.error("Error:", error);
          showNotification(
            "Error de conexión al eliminar el proyecto",
            "error"
          );

          // Restablecer botón
          confirmDeleteButton.disabled = false;
          confirmDeleteButton.textContent = "Eliminar Proyecto";
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
      projectIdToDelete = null;
    }
  });
});
