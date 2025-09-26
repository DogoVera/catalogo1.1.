// Variables para el lightbox
const lightbox = document.getElementById('lightbox');
const lightboxImage = document.getElementById('lightboxImage');
const productInfo = document.getElementById('productInfo');
const closeBtn = document.getElementById('closeBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const thumbnailsContainer = document.getElementById('thumbnails');
const gallery = document.getElementById('gallery');

let currentProductId = 0;
let currentImageIndex = 0;
let currentProductImages = [];
let products = [];

// Función para procesar el contenido de images.js
function loadImageCatalog() {
    try {
        products = [];

        // Dividir el texto por bloques de productos usando '('
        const blocks = rawProducts
            .split('(')
            .map(block => block.trim())
            .filter(block => block.length > 0);

        blocks.forEach(block => {
            // Limpiar y separar líneas
            const cleanBlock = block.replace(')', '').trim();
            const lines = cleanBlock.split('\n')
                .map(line => line.trim())
                .filter(line => line !== '');

            // La primera línea es el nombre del producto
            const name = lines[0];
            // El resto son URLs de imágenes
            const images = lines.slice(1);

            products.push({
                id: products.length + 1,
                title: name,
                images: images
            });
        });

        renderGallery();
    } catch (error) {
        console.error('Error al cargar el catálogo:', error);
        // Producto de ejemplo si hay error
        products = [{
            id: 1,
            title: "Producto de ejemplo",
            images: [
                "https://images.unsplash.com/photo-1525299374597-911581e1bdef?auto=format&fit=crop&w=800&q=80"
            ]
        }];
        renderGallery();
    }
}

// Renderizar la galería en el DOM
function renderGallery() {
    gallery.innerHTML = '';

    products.forEach((product) => {
        const itemElement = document.createElement('div');
        itemElement.className = 'item';
        itemElement.setAttribute('data-product', product.id);

        itemElement.innerHTML = `
            <img src="${product.images[0]}" alt="${product.title}" loading="lazy">
        `;

        itemElement.addEventListener('click', () => {
            openLightbox(product.id);
        });

        gallery.appendChild(itemElement);
    });
}

// Abrir el lightbox con las imágenes del producto
function openLightbox(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    currentProductId = productId;
    currentProductImages = product.images;
    currentImageIndex = 0;

    updateLightbox();
    renderThumbnails();

    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
}

// Cerrar el lightbox
function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
}

// Actualizar imagen en lightbox
function updateLightbox() {
    lightboxImage.src = currentProductImages[currentImageIndex];
    productInfo.textContent = products.find(p => p.id === currentProductId).title;

    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach((thumb, index) => {
        thumb.classList.toggle('active', index === currentImageIndex);
    });
}

// Renderizar miniaturas
function renderThumbnails() {
    thumbnailsContainer.innerHTML = '';

    currentProductImages.forEach((image, index) => {
        const thumbnail = document.createElement('div');
        thumbnail.className = 'thumbnail';
        if (index === currentImageIndex) thumbnail.classList.add('active');

        thumbnail.innerHTML = `<img src="${image}" alt="Miniatura ${index + 1}">`;

        thumbnail.addEventListener('click', () => {
            currentImageIndex = index;
            updateLightbox();
        });

        thumbnailsContainer.appendChild(thumbnail);
    });
}

// Navegar a la imagen anterior
function showPrevImage() {
    currentImageIndex = (currentImageIndex - 1 + currentProductImages.length) % currentProductImages.length;
    updateLightbox();
}

// Navegar a la siguiente imagen
function showNextImage() {
    currentImageIndex = (currentImageIndex + 1) % currentProductImages.length;
    updateLightbox();
}

// Inicializar la galería
document.addEventListener('DOMContentLoaded', function() {
    loadImageCatalog();

    closeBtn.addEventListener('click', closeLightbox);
    prevBtn.addEventListener('click', showPrevImage);
    nextBtn.addEventListener('click', showNextImage);

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
    });

    document.addEventListener('keydown', (e) => {
        if (lightbox.classList.contains('open')) {
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowLeft') showPrevImage();
            if (e.key === 'ArrowRight') showNextImage();
        }
    });
});
