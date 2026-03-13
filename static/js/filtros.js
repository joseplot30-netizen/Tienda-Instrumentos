/*
 * Lógica de filtros independiente para catálogo de productos
 * depende de los arrays globales `productos` y la función `cargarProductos`
 */

function inicializarFiltros() {
    const aplicarBtn = document.getElementById('aplicar-filtros');
    if (aplicarBtn) {
        aplicarBtn.addEventListener('click', aplicarFiltros);
    }
}

function aplicarFiltros() {
    const marcasSeleccionadas = Array.from(document.querySelectorAll('.marca-filter:checked')).map(cb => cb.value);
    const precioMin = parseInt(document.getElementById('precio-min').value) || 0;
    const precioMax = parseInt(document.getElementById('precio-max').value) || Infinity;

    let resultado = productos || [];

    if (marcasSeleccionadas.length) {
        resultado = resultado.filter(p => marcasSeleccionadas.includes(p.categoria.id));
    }

    resultado = resultado.filter(p => p.precio >= precioMin && p.precio <= precioMax);

    if (typeof cargarProductos === 'function') {
        cargarProductos(resultado);
    }
}

// ejecuta al cargar el DOM para enganchar el botón si existe
document.addEventListener('DOMContentLoaded', () => {
    inicializarFiltros();
});
