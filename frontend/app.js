document.addEventListener('DOMContentLoaded', () => {
    // --- Lógica para cargar el periodo académico actual ---
    async function cargarPeriodoActual() {
        const periodoInput = document.getElementById('periodo');
        try {
            // --- SIMULACIÓN DE LLAMADA AL BACKEND ---
            // Cuando tu backend esté listo, reemplazarás esta simulación
            // por una llamada real con fetch().
            const simularLlamadaBackend = new Promise(resolve => {
                setTimeout(() => {
                    // Aquí tu backend devolvería el periodo que está "activo"
                    // en tu tabla de "universidades" o "periodos".
                    resolve({ periodo_activo: '2025-2' }); 
                }, 500); // Pequeño retraso para simular la red
            });

            const data = await simularLlamadaBackend; // Reemplazar con: await fetch('/api/periodo-actual');
            periodoInput.value = data.periodo_activo;

        } catch (error) {
            periodoInput.value = 'Error al cargar';
            console.error('No se pudo obtener el periodo:', error);
        }
    }
    cargarPeriodoActual();

    const inputs = document.querySelectorAll('input, select');

    inputs.forEach(input => {
        // Para inputs que ya tienen valor al cargar la página (como el periodo)
        if (input.value.trim() !== '' || (input.type === 'select-one' && input.selectedIndex > 0)) {
            input.parentElement.classList.add('filled');
        }

        input.addEventListener('focus', () => {
            input.parentElement.classList.add('filled');
        });

        input.addEventListener('blur', () => {
            if (input.value.trim() === '' && (input.type !== 'select-one' || input.selectedIndex === 0)) {
                input.parentElement.classList.remove('filled');
            }
        });

        if (input.type === 'select-one') {
            input.addEventListener('change', () => {
                if (input.selectedIndex > 0) {
                    input.parentElement.classList.add('filled');
                } else {
                    input.parentElement.classList.remove('filled');
                }
            });
        }
    });

    // --- Lógica para mostrar campo de identificación ---
    const tipoIdSelect = document.getElementById('tipoId');
    const campoIdentificacion = document.getElementById('campoIdentificacion');
    const labelIdentificacion = document.getElementById('labelIdentificacion');
    const inputIdentificacion = document.getElementById('identificacion');

    if (tipoIdSelect && campoIdentificacion && labelIdentificacion) {
        tipoIdSelect.addEventListener('change', (e) => {
            const selection = e.target.value;
            if (selection === 'cedula') {
                campoIdentificacion.style.display = 'block';
                labelIdentificacion.textContent = 'Número de Cédula';
                inputIdentificacion.value = ''; // Limpiar campo al cambiar
                inputIdentificacion.parentElement.classList.remove('filled');
            } else if (selection === 'pasaporte') {
                campoIdentificacion.style.display = 'block';
                labelIdentificacion.textContent = 'Número de Pasaporte';
                inputIdentificacion.value = ''; // Limpiar campo al cambiar
                inputIdentificacion.parentElement.classList.remove('filled');
            } else {
                campoIdentificacion.style.display = 'none';
            }
        });
    }

    // --- Lógica para mostrar/ocultar contraseña ---
    const togglePasswordIcons = document.querySelectorAll('.toggle-password');
    togglePasswordIcons.forEach(icon => {
        icon.addEventListener('click', () => {
            const passwordInput = icon.previousElementSibling;
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.textContent = '🙈';
            } else {
                passwordInput.type = 'password';
                icon.textContent = '👁️';
            }
        });
    });

    // --- Lógica de validación del formulario de registro ---
    const registroForm = document.getElementById('registroForm');
    if (registroForm) {
        registroForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Evita el envío real del formulario por ahora

            const contrasena = document.getElementById('contrasena').value;
            const confirmarContrasena = document.getElementById('confirmarContrasena').value;

            if (contrasena !== confirmarContrasena) {
                alert('Las contraseñas no coinciden.');
                return;
            }

            // Recopilar todos los datos del formulario
            const datosUsuario = {
                periodo: document.getElementById('periodo').value,
                nombre_completo: document.getElementById('nombreCompleto').value,
                tipo_identificacion: document.getElementById('tipoId').value,
                identificacion: document.getElementById('identificacion').value,
                correo: document.getElementById('correo').value,
                contrasena: contrasena, // Enviar la contraseña para que el backend la encripte
            };

            try {
                // Enviar los datos al backend
                // NOTA: Debes crear un endpoint en tu backend que reciba esta petición en la ruta '/api/registro'
                const respuesta = await fetch('/api/registro', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(datosUsuario),
                });

                const resultado = await respuesta.json();

                if (respuesta.ok) {
                    alert('¡Cuenta creada exitosamente!');
                    // Opcional: redirigir al login
                    window.location.href = 'index.html';
                } else {
                    // Mostrar el mensaje de error que envía el backend
                    alert(`Error: ${resultado.error || 'No se pudo crear la cuenta.'}`);
                }
            } catch (error) {
                console.error('Error al conectar con el servidor:', error);
                alert('Hubo un problema de conexión. Inténtalo de nuevo más tarde.');
            }
        });
    }
});