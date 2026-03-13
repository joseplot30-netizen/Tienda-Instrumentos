/**
 * Gestor genérico de productos desde API
 * Reemplaza: main_bajo.js, main_bateria.js, main_guitarra.js
 * Uso: cargarCatalogo('bajos', 'bajo') en bajos.html
 */

let productos = [];
let productosEnCarrito = [];
const contenedorProductos = document.querySelector("#contenedor-productos");
let botonesAgregar = document.querySelectorAll(".producto-agregar");
const numerito = document.querySelector("#numerito");

// Cargar productos desde la API
async function cargarCatalogo(endpoint, prefijo) {
    try {
        const response = await fetch(`/api/productos/${endpoint}`);
        const data = await response.json();
        
        if (Array.isArray(data)) {
            productos = data.map((prod, index) => ({
                id: `${prefijo}-${index + 1}`,
                titulo: prod.titulo,
                imagen: prod.imagen,
                categoria: {
                    nombre: prod.brand || 'sin marca',
                    id: prod.brand || 'sin marca'
                },
                precio: prod.precio
            }));
            
            cargarProductos(productos);
        }
    } catch (error) {
        console.error('Error al cargar productos:', error);
        contenedorProductos.innerHTML = '<p>Error al cargar productos</p>';
    }
}

// Inicializar carrito desde localStorage
function inicializarCarrito() {
    const productosEnCarritoLS = localStorage.getItem("productos-en-carrito");
    if (productosEnCarritoLS) {
        productosEnCarrito = JSON.parse(productosEnCarritoLS);
        actualizarNumerito();
    } else {
        productosEnCarrito = [];
    }
}

// Renderizar productos en la página
function cargarProductos(productosElegidos) {
    contenedorProductos.innerHTML = "";

    productosElegidos.forEach(producto => {
        const div = document.createElement("div");
        div.classList.add("producto");
        div.innerHTML = `
            <img class="producto-imagen" src="${producto.imagen}" alt="${producto.titulo}">
            <div class="producto-detalles">
                <h3 class="producto-titulo">${producto.titulo}</h3>
                <p class="producto-precio">$${producto.precio}</p>
                <button class="producto-agregar" id="${producto.id}">Agregar</button>
            </div>
        `;

        contenedorProductos.append(div);
    })

    actualizarBotonesAgregar();
}

// Actualizar event listeners de botones de agregar
function actualizarBotonesAgregar() {
    botonesAgregar = document.querySelectorAll(".producto-agregar");

    botonesAgregar.forEach(boton => {
        boton.addEventListener("click", agregarAlCarrito);
    });
}

// Agregar producto al carrito
function agregarAlCarrito(e) {
    const idBoton = e.currentTarget.id;
    const productoAgregado = productos.find(producto => producto.id === idBoton);

    if(productosEnCarrito.some(producto => producto.id === idBoton)) {
        const index = productosEnCarrito.findIndex(producto => producto.id === idBoton);
        productosEnCarrito[index].cantidad++;
    } else {
        productoAgregado.cantidad = 1;
        productosEnCarrito.push(productoAgregado);
    }

    actualizarNumerito();
    localStorage.setItem("productos-en-carrito", JSON.stringify(productosEnCarrito));
    mostrarAnuncio();
}

// Actualizar el contador del carrito
function actualizarNumerito() {
    let nuevoNumerito = productosEnCarrito.reduce((acc, producto) => acc + producto.cantidad, 0);
    numerito.innerText = nuevoNumerito;
    const numerito_drawer = document.querySelector("#numerito-drawer");
    if (numerito_drawer) {
        numerito_drawer.innerText = nuevoNumerito;
    }
}

// Mostrar anuncio de producto agregado
function mostrarAnuncio() {
    const anuncio = document.getElementById('anuncio-carrito');
    if (anuncio) {
        anuncio.classList.remove('oculto');
    }
}



// Manejar botones del anuncio
function inicializarAnuncio() {
    const irCarritoBtn = document.getElementById('ir-carrito');
    const seguirComprandoBtn = document.getElementById('seguir-comprando');

    if (irCarritoBtn) {
        irCarritoBtn.addEventListener('click', () => {
            window.location.href = '/carrito';
        });
    }

    if (seguirComprandoBtn) {
        seguirComprandoBtn.addEventListener('click', () => {
            const anuncio = document.getElementById('anuncio-carrito');
            if (anuncio) {
                anuncio.classList.add('oculto');
            }
        });
    }
}

// Inicializar todo al cargar el DOM
document.addEventListener('DOMContentLoaded', () => {
    inicializarCarrito();
    inicializarAnuncio();
});
