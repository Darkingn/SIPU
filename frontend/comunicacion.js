/**
 * Carga el período académico actual desde el backend.
 * @returns {Promise<string>} El período académico activo (ej. '2025-2').
 */
export async function obtenerPeriodoActual() {
    try {
        // --- SIMULACIÓN DE LLAMADA AL BACKEND ---
        const simularLlamadaBackend = new Promise(resolve => {
            setTimeout(() => {
                resolve({ periodo_activo: '2025-2' }); 
            }, 500);
        });

        const data = await simularLlamadaBackend; // Reemplazar con: await fetch('/api/periodo-actual');
        return data.periodo_activo;
    } catch (error) {
        console.error('No se pudo obtener el periodo:', error);
        throw new Error('Error al cargar el periodo');
    }
}

/**
 * Registra un nuevo usuario en el backend.
 * @param {object} datosUsuario - Los datos del usuario a registrar.
 * @returns {Promise<object>} El resultado de la operación de registro.
 */
export async function registrarUsuario(datosUsuario) {
    // NOTA: Debes crear un endpoint en tu backend que reciba esta petición en la ruta '/api/registro'
    const respuesta = await fetch('/api/registro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(datosUsuario),
    });

    const resultado = await respuesta.json();

    if (!respuesta.ok) {
        throw new Error(resultado.error || 'No se pudo crear la cuenta.');
    }

    return resultado;
}