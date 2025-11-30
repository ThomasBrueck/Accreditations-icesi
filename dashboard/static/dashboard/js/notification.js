// notification.js - Sistema de notificaciones para el navbar
document.addEventListener("DOMContentLoaded", function() {
    // Elementos del DOM
    const notificationIcon = document.getElementById("notification-icon");
    const notificationDropdown = document.getElementById("notification-dropdown");
    const notificationBadge = document.getElementById("notification-badge");
    const userProfile = document.getElementById("user-profile");
    const profileDropdown = document.getElementById("profile-dropdown");
    
    // Verificar que los elementos existan
    if (!notificationIcon || !notificationDropdown) {
        console.error("Elementos de notificación no encontrados");
        return;
    }
    
    // Obtener datos de atributos
    const csrfToken = notificationIcon.getAttribute("data-csrf-token");
    const markReadUrl = notificationIcon.getAttribute("data-mark-read-url");
    
    if (!csrfToken || !markReadUrl) {
        console.error("Token CSRF o URL de marcado como leído no encontrados");
        return;
    }
    
    // Función para mostrar/ocultar el dropdown de notificaciones
    function toggleNotificationDropdown(event) {
        event.stopPropagation();
        
        // Si el dropdown del perfil está abierto, cerrarlo
        if (profileDropdown && profileDropdown.classList.contains("show")) {
            profileDropdown.classList.remove("show");
        }
        
        const isVisible = notificationDropdown.classList.contains("show");
        
        if (!isVisible) {
            // Mostrar el dropdown
            notificationDropdown.classList.add("show");
            
            // Marcar notificaciones como leídas si hay alguna no leída
            if (notificationBadge) {
                markNotificationsAsRead();
            }
        } else {
            // Ocultar el dropdown
            notificationDropdown.classList.remove("show");
        }
    }
    
    // Función para marcar notificaciones como leídas
    function markNotificationsAsRead() {
        fetch(markReadUrl, {
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {
                // Eliminar el contador de notificaciones con animación
                if (notificationBadge) {
                    notificationBadge.style.transition = "opacity 0.5s ease";
                    notificationBadge.style.opacity = "0";
                    
                    // Eliminar el badge después de la animación
                    setTimeout(() => {
                        notificationBadge.style.display = "none";
                    }, 500);
                }
                
                // Marcar todas las notificaciones como leídas en la UI
                const unreadItems = document.querySelectorAll(".notification-item.unread");
                unreadItems.forEach(item => {
                    item.classList.remove("unread");
                });
            } else {
                console.error("Error al marcar notificaciones como leídas:", response.statusText);
            }
        })
        .catch(error => {
            console.error("Error en la petición:", error);
        });
    }
    
    // Función para manejar el dropdown del perfil
    function toggleProfileDropdown(event) {
        if (!profileDropdown) return;
        
        event.stopPropagation();
        
        // Si el dropdown de notificaciones está abierto, cerrarlo
        if (notificationDropdown.classList.contains("show")) {
            notificationDropdown.classList.remove("show");
        }
        
        // Toggle del dropdown del perfil
        profileDropdown.classList.toggle("show");
    }
    
    // Event listeners
    notificationIcon.addEventListener("click", toggleNotificationDropdown);
    
    // Si existe el perfil de usuario, añadir event listener
    if (userProfile) {
        userProfile.addEventListener("click", toggleProfileDropdown);
    }
    
    // Cerrar los dropdowns cuando se hace clic fuera
    document.addEventListener("click", function(event) {
        // Cerrar dropdown de notificaciones
        if (notificationDropdown.classList.contains("show") && 
            !notificationIcon.contains(event.target) && 
            !notificationDropdown.contains(event.target)) {
            notificationDropdown.classList.remove("show");
        }
        
        // Cerrar dropdown del perfil
        if (profileDropdown && profileDropdown.classList.contains("show") && 
            !userProfile.contains(event.target) && 
            !profileDropdown.contains(event.target)) {
            profileDropdown.classList.remove("show");
        }
    });
    
    // Añadir efecto de pulso a las nuevas notificaciones
    if (notificationBadge) {
        notificationBadge.classList.add("new-notification");
    }
    
    // Función para manejar el toggle del sidebar
    const sidebarToggle = document.getElementById("sidebar-toggle");
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", function() {
            document.body.classList.toggle("sidebar-collapsed");
            
            // Guardar el estado del sidebar en localStorage
            const isCollapsed = document.body.classList.contains("sidebar-collapsed");
            localStorage.setItem("sidebar-collapsed", isCollapsed);
        });
        
        // Restaurar el estado del sidebar al cargar la página
        const savedState = localStorage.getItem("sidebar-collapsed");
        if (savedState === "true") {
            document.body.classList.add("sidebar-collapsed");
        }
    }
});