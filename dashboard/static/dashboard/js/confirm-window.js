document.addEventListener("DOMContentLoaded", () => {
  let activeForm = null;
  let activeCallback = null; // Para manejar callbacks como el fetch del botón Complete

  const createEditModal = document.getElementById("customModal");
  const deleteModal = document.getElementById("deleteModal");
  const completeModal = document.getElementById("completeModal"); // Nuevo modal para Complete

  const openBtn = document.getElementById("triggerModal");
  const createForm = document.getElementById("reportForm");

  const cancelCreateBtn = document.getElementById("cancelModal");
  const confirmCreateBtn = document.getElementById("submitReport");

  console.log("confirm-window.js loaded");

  // CREAR / EDITAR
  if (openBtn && createForm) {
    openBtn.addEventListener("click", () => {
      console.log("Triggering create/edit modal");
      activeForm = createForm;
      createEditModal.style.display = "flex";
    });
  }

  if (cancelCreateBtn) {
    cancelCreateBtn.addEventListener("click", () => {
      console.log("Cancel create/edit modal");
      createEditModal.style.display = "none";
      activeForm = null;
    });
  }

  if (confirmCreateBtn) {
    confirmCreateBtn.addEventListener("click", () => {
      if (activeForm) {
        console.log("Submitting create/edit form");
        activeForm.submit();
      }
    });
  }

  // DELETE (usar delegación de eventos para botones dinámicos)
  document.body.addEventListener("click", (event) => {
    if (event.target.classList.contains("triggerDeleteModal")) {
      console.log("Delete button clicked:", event.target);
      const formId = event.target.getAttribute("data-form-id");
      activeForm = document.getElementById(formId);
      if (activeForm) {
        console.log("Setting active form:", formId, activeForm);
        if (deleteModal) {
          console.log("Showing delete modal");
          deleteModal.style.display = "flex";
        } else {
          console.error("Delete modal not found in DOM");
        }
      } else {
        console.error("Form not found for ID:", formId);
      }
    }
  });

  // COMPLETE (usar delegación de eventos para botones dinámicos)
  document.body.addEventListener("click", (event) => {
    if (event.target.classList.contains("complete-btn") && !event.target.classList.contains("disabled")) {
      console.log("Complete button clicked:", event.target);
      const url = event.target.getAttribute("data-url");
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      activeCallback = () => {
        fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken
          }
        }).then(response => response.json()).then(data => {
          if (data.status === 'success') {
            window.location.reload();
          } else {
            alert(data.message || 'Error completing characteristic.');
          }
        }).catch(error => {
          console.error('Error:', error);
          alert('Error completing characteristic.');
        });
      };
      if (completeModal) {
        console.log("Showing complete modal");
        completeModal.style.display = "flex";
      } else {
        console.error("Complete modal not found in DOM");
      }
    }
  });

  // Configurar botones para el modal de Delete
  const cancelDeleteBtn = document.querySelector(".cancel-delete-btn");
  const confirmDeleteBtn = document.querySelector(".confirm-delete-btn");

  if (cancelDeleteBtn) {
    cancelDeleteBtn.addEventListener("click", () => {
      console.log("Cancel delete modal");
      deleteModal.style.display = "none";
      activeForm = null;
    });
  }

  if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener("click", () => {
      if (activeForm) {
        console.log("Submitting delete form:", activeForm);
        activeForm.submit();
      } else {
        console.log("No active form set for delete.");
      }
      deleteModal.style.display = "none";
      activeForm = null;
    });
  }

  // Configurar botones para el modal de Complete
  const cancelCompleteBtn = document.querySelector(".cancel-complete-btn");
  const confirmCompleteBtn = document.querySelector(".confirm-complete-btn");

  if (cancelCompleteBtn) {
    cancelCompleteBtn.addEventListener("click", () => {
      console.log("Cancel complete modal");
      completeModal.style.display = "none";
      activeCallback = null;
    });
  }

  if (confirmCompleteBtn) {
    confirmCompleteBtn.addEventListener("click", () => {
      if (activeCallback) {
        console.log("Executing complete callback");
        activeCallback();
      } else {
        console.log("No active callback set for complete.");
      }
      completeModal.style.display = "none";
      activeCallback = null;
    });
  }

  // Cerrar modales al hacer clic fuera
  window.addEventListener("click", (event) => {
    if (event.target === createEditModal) {
      console.log("Click outside create/edit modal");
      createEditModal.style.display = "none";
      activeForm = null;
    }
    if (event.target === deleteModal) {
      console.log("Click outside delete modal");
      deleteModal.style.display = "none";
      activeForm = null;
    }
    if (event.target === completeModal) {
      console.log("Click outside complete modal");
      completeModal.style.display = "none";
      activeCallback = null;
    }
  });
});