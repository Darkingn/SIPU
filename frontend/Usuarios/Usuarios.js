document.addEventListener('DOMContentLoaded', () => {
    // Seleccionamos todos los elementos que pueden abrir un menú
    const dropdownToggles = document.querySelectorAll('.nav-link, #profileLogo');

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (event) => {
            // Evita que el clic en el toggle cierre el menú inmediatamente
            event.stopPropagation();

            // Encuentra el menú desplegable asociado a este toggle
            const currentMenu = toggle.nextElementSibling;

            // Cierra todos los demás menús abiertos
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                if (openMenu !== currentMenu) {
                    openMenu.classList.remove('show');
                }
            });

            // Muestra u oculta el menú actual
            if (currentMenu && currentMenu.classList.contains('dropdown-menu')) {
                currentMenu.classList.toggle('show');
            }
        });
    });

    // Cierra todos los menús si se hace clic en cualquier otro lugar de la página
    window.addEventListener('click', () => {
        document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
            openMenu.classList.remove('show');
        });
    });
});