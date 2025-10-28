import { obtenerPeriodoActual, registrarUsuario } from './comunicacion.js';

document.addEventListener('DOMContentLoaded', () => {
    //Lógica para cargar el periodo académico actual
    async function cargarPeriodoActual() {
        const periodoInput = document.getElementById('periodo');
        if (!periodoInput) return;

        try {
            const periodo = await obtenerPeriodoActual();
            periodoInput.value = periodo;
            periodoInput.parentElement.classList.add('filled');
        } catch (error) {
            periodoInput.value = 'Error al cargar';
        }
    }
    cargarPeriodoActual();

    const inputs = document.querySelectorAll('input, select');

    inputs.forEach(input => {
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

    //Lógica para mostrar campo de identificación
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
                inputIdentificacion.value = '';
                inputIdentificacion.parentElement.classList.remove('filled');
            } else if (selection === 'pasaporte') {
                campoIdentificacion.style.display = 'block';
                labelIdentificacion.textContent = 'Número de Pasaporte';
                inputIdentificacion.value = '';
                inputIdentificacion.parentElement.classList.remove('filled');
            } else {
                campoIdentificacion.style.display = 'none';
            }
        });
    }

    //Lógica para mostrar/ocultar contraseña
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

    //Lógica de validación del formulario de registro
    const registroForm = document.getElementById('registroForm');
    if (registroForm) {
        registroForm.addEventListener('submit', async (e) => {
            e.preventDefault(); //Evita el envío real del formulario por ahora

            const contrasena = document.getElementById('contrasena').value;
            const confirmarContrasena = document.getElementById('confirmarContrasena').value;

            if (contrasena !== confirmarContrasena) {
                alert('Las contraseñas no coinciden.');
                return;
            }

            //Recopila todos los datos del formulario
            const datosUsuario = {
                periodo: document.getElementById('periodo').value,
                nombre_completo: document.getElementById('nombreCompleto').value,
                universidad: document.getElementById('universidad').value,
                tipo_identificacion: document.getElementById('tipoId').value,
                identificacion: document.getElementById('identificacion').value,
                correo: document.getElementById('correo').value,
                contrasena: contrasena, //Envia la contraseña para que el backend la encripte
            };

            try {
                await registrarUsuario(datosUsuario);
                alert('¡Cuenta creada exitosamente!');
                window.location.href = 'index.html';
                
            } catch (error) {
                console.error('Error en el registro:', error);
                alert(`Error: ${error.message}`);
            }
        });
    }
});