document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("createRequestForm");
  const hoursInput = document.getElementById("hoursRequested");
  const dateInput = document.getElementById("date");
  const descriptionInput = document.getElementById("description");
  const fileInput = document.getElementById("files");
  const filePreview = document.getElementById("filePreview");
  const submitBtn = document.getElementById("submitBtn");

  // Elementos para mensajes de error
  const errorContainer = document.createElement("div");
  errorContainer.className = "validation-errors";
  form.insertBefore(errorContainer, form.firstChild);

  // Función para mostrar errores de forma destacada
  function showFieldError(field, message) {
    removeFieldError(field);

    const errorElement = document.createElement("div");
    errorElement.className = "field-error-message";
    errorElement.innerHTML = `<i class="bi bi-exclamation-circle"></i> ${message}`;

    field.parentNode.insertBefore(errorElement, field.nextSibling);
    field.classList.add("has-error");

    setTimeout(() => {
      field.focus();
      field.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 100);

    return errorElement;
  }

  function removeFieldError(field) {
    field.classList.remove("has-error");
    const existingError = field.parentNode.querySelector(
      ".field-error-message"
    );
    if (existingError) {
      existingError.remove();
    }
  }

  // Previsualización de archivos
  if (fileInput) {
    fileInput.addEventListener("change", function () {
      updateFilePreview();
    });
  }

  function updateFilePreview() {
    const files = Array.from(fileInput.files);

    if (files.length === 0) {
      filePreview.innerHTML = "<p>No hay archivos seleccionados</p>";
      return;
    }

    let html = '<ul class="file-list">';
    let totalSize = 0;
    let hasInvalidFiles = false;

    files.forEach((file) => {
      const fileSize = formatFileSize(file.size);
      totalSize += file.size;

      // Validar tipo de archivo
      const allowedExtensions = [
        ".pdf",
        ".doc",
        ".docx",
        ".jpg",
        ".jpeg",
        ".png",
        ".txt",
      ];
      const isValidType = allowedExtensions.some((ext) =>
        file.name.toLowerCase().endsWith(ext)
      );

      // Validar tamaño individual
      const isSizeValid = file.size <= 10 * 1024 * 1024; // 10MB

      html += `
                <li class="file-item ${
                  !isValidType || !isSizeValid ? "invalid-file" : ""
                }">
                    <div class="file-name">
                        <i class="bi bi-file-earmark ${
                          !isValidType || !isSizeValid ? "text-danger" : ""
                        }"></i>
                        <span>${file.name}</span>
                    </div>
                    <div class="file-info">
                        <span class="file-size">${fileSize}</span>
                        ${
                          !isValidType
                            ? '<span class="file-error">Tipo no permitido</span>'
                            : ""
                        }
                        ${
                          !isSizeValid
                            ? '<span class="file-error">>10MB</span>'
                            : ""
                        }
                    </div>
                </li>
            `;

      if (!isValidType || !isSizeValid) {
        hasInvalidFiles = true;
      }
    });

    html += "</ul>";

    // Validar tamaño total
    const maxTotalSize = 50 * 1024 * 1024;
    if (totalSize > maxTotalSize) {
      html += `<p class="file-error"><i class="bi bi-exclamation-triangle"></i> El tamaño total excede los 50MB</p>`;
      hasInvalidFiles = true;
    }

    filePreview.innerHTML = html;
    updateSubmitButton();
  }

  function formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }

  function validateForm(showIndividualErrors = false) {
    const errors = [];
    errorContainer.innerHTML = "";

    // Limpiar errores anteriores
    if (hoursInput) removeFieldError(hoursInput);
    if (dateInput) removeFieldError(dateInput);
    if (descriptionInput) removeFieldError(descriptionInput);

    // Validar horas
    if (hoursInput) {
      const hours = parseInt(hoursInput.value);
      if (isNaN(hours)) {
        errors.push("Las horas deben ser un número válido");
        if (showIndividualErrors) {
          showFieldError(hoursInput, "Las horas deben ser un número válido");
        }
      } else if (hours < 1) {
        errors.push("Las horas deben ser al menos 1");
        if (showIndividualErrors) {
          showFieldError(hoursInput, "Las horas deben ser al menos 1");
        }
      } else if (hours > 100) {
        errors.push("Las horas no pueden exceder 100");
        if (showIndividualErrors) {
          showFieldError(hoursInput, "Las horas no pueden exceder 100");
        }
      }
    }

    // Validar fecha
    if (dateInput) {
      if (!dateInput.value) {
        errors.push("La fecha es requerida");
        if (showIndividualErrors) {
          showFieldError(dateInput, "La fecha es requerida");
        }
      } else {
        const selectedDate = new Date(dateInput.value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (selectedDate > today) {
          errors.push("La fecha no puede ser futura");
          if (showIndividualErrors) {
            showFieldError(dateInput, "La fecha no puede ser futura");
          }
        }
      }
    }

    // Validar descripción
    if (descriptionInput) {
      const desc = descriptionInput.value.trim();
      if (desc.length === 0) {
        errors.push("La descripción es requerida");
        if (showIndividualErrors) {
          showFieldError(descriptionInput, "La descripción es requerida");
        }
      } else if (desc.length < 10) {
        errors.push("La descripción debe tener al menos 10 caracteres");
        if (showIndividualErrors) {
          showFieldError(
            descriptionInput,
            "La descripción debe tener al menos 10 caracteres"
          );
        }
      }
    }

    if (errors.length > 0 && showIndividualErrors) {
      errorContainer.innerHTML = `
                <div class="alert alert-error">
                    <i class="bi bi-exclamation-triangle"></i>
                    <div>
                        <strong>Por favor corrige los siguientes errores:</strong>
                        <ul>
                            ${errors
                              .map((error) => `<li>${error}</li>`)
                              .join("")}
                        </ul>
                    </div>
                </div>
            `;

      // Hacer scroll al inicio del formulario
      setTimeout(() => {
        errorContainer.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);

      return false;
    }

    return errors.length === 0;
  }

  // Actualizar estado del botón
  function updateSubmitButton() {
    const isValid = validateForm(false);
    if (submitBtn) {
      submitBtn.disabled = !isValid;
      submitBtn.classList.toggle("disabled", !isValid);
    }
  }

  // Escuchar cambios en los campos para validación en tiempo real
  if (hoursInput)
    hoursInput.addEventListener("input", function () {
      updateSubmitButton();
    });

  if (dateInput)
    dateInput.addEventListener("change", function () {
      updateSubmitButton();
    });

  if (descriptionInput)
    descriptionInput.addEventListener("input", function () {
      updateSubmitButton();
    });

  if (fileInput) fileInput.addEventListener("change", updateSubmitButton);

  // Validar al perder el foco (para mostrar errores inmediatos)
  if (hoursInput)
    hoursInput.addEventListener("blur", function () {
      validateForm(false);
    });

  if (dateInput)
    dateInput.addEventListener("blur", function () {
      validateForm(false);
    });

  if (descriptionInput)
    descriptionInput.addEventListener("blur", function () {
      validateForm(false);
    });

  if (form) {
    form.addEventListener("submit", function (e) {
      const isValid = validateForm(true);

      if (!isValid) {
        e.preventDefault();
        e.stopPropagation();

        const submitError = document.createElement("div");
        submitError.className = "alert alert-error submit-error";
        submitError.innerHTML = `
                    <i class="bi bi-x-circle"></i>
                    <strong>No se pudo crear la solicitud. Corrige los errores arriba.</strong>
                `;

        if (errorContainer.firstChild) {
          errorContainer.appendChild(submitError);
        } else {
          form.insertBefore(submitError, form.firstChild);
        }

        // Hacer scroll al error
        setTimeout(() => {
          submitError.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 100);

        return false;
      }

      // Si pasa validación, mostrar loading
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML =
        '<i class="bi bi-hourglass-split"></i> Creando solicitud...';
      submitBtn.classList.add("loading");

      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
        submitBtn.classList.remove("loading");
      }, 10000); // 10 segundos
    });
  }

  // Inicializar validación
  updateSubmitButton();
});
