// Función que se ejecuta cuando el DOM está listo
// Sincroniza el contador del carrito en todos los templates
function sincronizarCarrito() {
    // Obtener el contador desde localStorage
    let productosEnCarrito = localStorage.getItem("productos-en-carrito");
    let productos = [];
    
    if (productosEnCarrito) {
        try {
            productos = JSON.parse(productosEnCarrito);
        } catch (e) {
            productos = [];
        }
    }
    
    // Calcular el número total de items
    let nuevoNumerito = Array.isArray(productos) 
        ? productos.reduce((acc, producto) => acc + (producto.cantidad || 0), 0) 
        : 0;
    
    // Actualizar todos los elementos con el ID 'numerito'
    const numeritos = document.querySelectorAll("#numerito");
    numeritos.forEach(numerito => {
        numerito.innerText = nuevoNumerito;
    });
    
    // También actualizar numerito-drawer si existe
    const numerito_drawer = document.querySelector("#numerito-drawer");
    if (numerito_drawer) {
        numerito_drawer.innerText = nuevoNumerito;
    }
    
    return nuevoNumerito;
}

// Ejecutar sincronización al cargar la página
document.addEventListener('DOMContentLoaded', sincronizarCarrito);

// También sincronizar cuando hay cambios en localStorage (detecta cambios en otras pestañas/ventanas)
window.addEventListener('storage', (event) => {
    if (event.key === 'productos-en-carrito') {
        sincronizarCarrito();
    }
});

// Exportar la función si se usa como módulo
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { sincronizarCarrito };
}
