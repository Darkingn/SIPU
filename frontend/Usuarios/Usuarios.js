document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggles = document.querySelectorAll('.nav-link, #profileLogo');

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (event) => {
            event.stopPropagation();

            //Encuentra el menú desplegable asociado a este toggle
            const currentMenu = toggle.nextElementSibling;

            //Cierra todos los demás menús abiertos
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                if (openMenu !== currentMenu) {
                    openMenu.classList.remove('show');
                }
            });

            //Muestra u oculta el menú actual
            if (currentMenu && currentMenu.classList.contains('dropdown-menu')) {
                currentMenu.classList.toggle('show');
            }
        });
    });

    //Cierra todos los menús si se hace clic en cualquier otro lugar de la página
    window.addEventListener('click', () => {
        document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
            openMenu.classList.remove('show');
        });
    });

    //Lógica para la barra lateral de la página de inscripción
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    const contentSections = document.querySelectorAll('.content-section');

    sidebarLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();

            const targetId = link.getAttribute('data-target');

            contentSections.forEach(section => {
                section.classList.remove('active');
            });
            sidebarLinks.forEach(s_link => {
                s_link.classList.remove('active');
            });

            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.add('active');
                link.classList.add('active');
            }
        });
    });
});