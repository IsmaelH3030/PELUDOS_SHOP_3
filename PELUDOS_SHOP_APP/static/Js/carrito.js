// // Objeto para almacenar los productos en el carrito
// let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

// // Función para obtener los botones de "Agregar al carrito"
// const botonesAgregarAlCarrito = document.querySelectorAll(".producto-agregar");
// // Agregar evento click a cada botón de "Agregar al carrito"
// botonesAgregarAlCarrito.forEach((boton) => {
//   boton.addEventListener("click", () => {
//     const productoId = boton.dataset.id; // Usamos dataset.id para asegurar que obtenemos el ID correctamente
//     const card = boton.closest(".card");
//     const imagen = card.querySelector(".producto-imagen").src;
//     const nombre = card.querySelector(".card-title").textContent;
//     const descripcion = card.querySelector(".card-text").textContent;
//     const precio = parseFloat(card.querySelector(".producto-precio").textContent.replace("$", "").replace(".", ""));
//     const nuevoProducto = {
//                             id: productoId,
//                             imagen,
//                             nombre,
//                             descripcion,
//                             precio,
//                             cantidad: 0,
//                           };
//     agregarAlCarrito(nuevoProducto);
//   });
// });



// // Función para actualizar el contenido del carrito en la página
// function actualizarCarrito() {
//   const carritoContenido = document.getElementById("carrito-contenido");
//   const carritoTotal = document.getElementById("carrito-total");
//   carritoContenido.innerHTML = "";
//   carritoTotal.innerHTML = "";

//   let total = 0;

//   carrito.forEach((item) => {
//     const fila = document.createElement("div");
//     fila.classList.add("carrito-fila");
//     fila.innerHTML = `
//       <div class="carrito-producto">
//         <img src="${item.imagen}" alt="${item.nombre}" class="carrito-imagen" style="width: 100px;">
//         <div class="carrito-info">
//           <h4>${item.nombre}</h4>
//           <p>${item.descripcion}</p>
//           <p>Precio: $${item.precio.toLocaleString("es-CL")}</p>
//           <p>Cantidad: ${item.cantidad}</p>
//           <button class="btn btn-danger" onclick="eliminarDelCarrito('${item.id}')">Eliminar</button>
//         </div>
//       </div>
//     `;

//     carritoContenido.appendChild(fila);
//     total += item.precio * item.cantidad;
//   });

//   carritoTotal.innerText = `TOTAL: $${total.toLocaleString("es-CL")}`;
// }

// // Función para agregar un producto al carrito
// function agregarAlCarrito(producto) {
//   const productoExistente = carrito.find((item) => item.id === producto.id);
//   if (productoExistente) {
//     productoExistente.cantidad++;
//   } else {
//     producto.cantidad = 1;
//     carrito.push(producto);
//   }

//   guardarCarritoEnLocalStorage();
//   actualizarContadorCarrito();
//   actualizarCarrito();
  
// }

// //  boton click para pagar 
// document.querySelector(".btn-pagar").addEventListener("click", pagar);
// // Función para pagar y vaciar el carrito
// function pagar() {
//   if (carrito.length === 0) {
//     alert("No hay productos en el carrito.");
//     return; // Salir de la función si el carrito está vacío
//   }

//   carrito = []; // Vaciar el array del carrito
//   guardarCarritoEnLocalStorage(); // Borrar el carrito del localStorage
//   actualizarContadorCarrito();
//   actualizarCarrito(); // Actualizar la visualización del carrito
//   alert("¡GRACIAS POR TU COMPRA!");
// }

// // Función para eliminar un producto del carrito
// function eliminarDelCarrito(id) {
//   carrito = carrito.filter((item) => item.id !== id);

//   guardarCarritoEnLocalStorage();
//   actualizarContadorCarrito();
//   actualizarCarrito();
// }

// // Función para guardar el carrito en el localStorage
// function guardarCarritoEnLocalStorage() {
//   localStorage.setItem("carrito", JSON.stringify(carrito));
// }

// // Función para actualizar el contador del carrito en el HTML
// function actualizarContadorCarrito() {
//   const cantidadCarrito = document.getElementById("cantidadCarrito");
//   const cantidad = carrito.reduce((acc, item) => acc + item.cantidad, 0);

//   if (cantidad > 0) {
//     cantidadCarrito.innerText = cantidad;
//     cantidadCarrito.style.display = "inline"; // Mostrar el contador
//   } else {
//     cantidadCarrito.innerText = "";
//     cantidadCarrito.style.display = "none"; // Ocultar el contador
//   }
// }

// // Actualizar el carrito y el contador al cargar la página
// document.addEventListener("DOMContentLoaded", function () {
//   actualizarCarrito();
//   actualizarContadorCarrito();
// });

// // Función para abrir el carrito (modal)
// function abrirCarrito() {
//   $("#carritoModal").modal("show");
// }

// // Función para cerrar el carrito (modal)
// function cerrarCarrito() {
//   $("#carritoModal").modal("hide");
// }

 // Mostrar campos de dirección si se selecciona "Despacho a domicilio"
 document.getElementById('despacho').addEventListener('change', function() {
    var option = this.value;
    if (option === 'domicilio') {
        document.getElementById('direccion-domicilio').style.display = 'block';
    } else {
        document.getElementById('direccion-domicilio').style.display = 'none';
    }
});
