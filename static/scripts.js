// static/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('nav::before');
    const navMenu = document.querySelector('nav ul');

    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    });
});


//carrusel

const carouselSlide = document.querySelector('.carousel-slide');
const carouselImages = document.querySelectorAll('.carousel-slide img');

// Configuración del carrusel
const intervalo = 3000; // Cambia esto para ajustar la velocidad del carrusel

let index = 0;
let interval;

function iniciarCarrusel() {
    interval = setInterval(() => {
        moverCarrusel();
    }, intervalo);
}

function moverCarrusel() {
    index++;

    if (index >= carouselImages.length) {
        index = 0;
    }

    carouselSlide.style.transform = `translateX(${-index * 100}%)`;
}

// Inicia el carrusel al cargar la página
window.addEventListener('load', () => {
    iniciarCarrusel();
});
