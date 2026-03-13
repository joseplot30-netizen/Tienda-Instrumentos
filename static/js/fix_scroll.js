// Fix Scroll - Asegurar que el scroll funcione sin restricciones
document.addEventListener('DOMContentLoaded', function() {
    // Remover restricciones de altura en elementos principales
    function enableFullScroll() {
        const html = document.documentElement;
        const body = document.body;
        const wrapper = document.querySelector('.wrapper');
        const main = document.querySelector('main');
        const container = document.querySelector('.container');

        // Permitir scroll en html y body
        html.style.height = 'auto';
        html.style.overflow = 'visible';
        
        body.style.height = 'auto';
        body.style.minHeight = '100%';
        body.style.overflow = 'visible';

        // Asegurar que wrapper crezca según contenido
        if (wrapper) {
            wrapper.style.height = 'auto';
            wrapper.style.minHeight = 'auto';
        }

        // Asegurar que main crezca según contenido
        if (main) {
            main.style.height = 'auto';
            main.style.minHeight = 'auto';
            main.style.justifyContent = 'flex-start';
        }

        // Asegurar que container crezca
        if (container) {
            container.style.height = 'auto';
            container.style.minHeight = 'auto';
        }

        // Remover overflow hidden de contenedor de productos
        const contenedorProductos = document.querySelector('.contenedor-productos');
        if (contenedorProductos) {
            contenedorProductos.style.overflow = 'visible';
            contenedorProductos.style.height = 'auto';
            contenedorProductos.style.minHeight = 'auto';
        }
    }

    // Ejecutar al cargar
    enableFullScroll();

    // Ejecutar también después de que se carguen los productos
    setTimeout(enableFullScroll, 500);
    setTimeout(enableFullScroll, 1000);

    // Observer para cambios en el DOM
    const observer = new MutationObserver(function(mutations) {
        enableFullScroll();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class']
    });
});

// Asegurar scroll al redimensionar ventana
window.addEventListener('resize', function() {
    const html = document.documentElement;
    const body = document.body;
    html.style.height = 'auto';
    body.style.height = 'auto';
});
