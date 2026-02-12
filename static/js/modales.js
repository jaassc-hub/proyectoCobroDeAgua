document.addEventListener('htmx:beforeRequest', function (event) {
    const titulo = event.detail.elt.getAttribute('data-modal-title');
    const icon = event.detail.elt.getAttribute('data-modal-icon');

    if (titulo) {
        document.getElementById('modalTitulo').textContent = titulo;
    }
    
    if(icon){
        iconoModal = document.getElementById('iconModal');
        iconoModal.className = "text-primary " + icon;
    }
});

// Cerrar modal
document.body.addEventListener('cerrarModal', function () {
    const modal = bootstrap.Modal.getInstance(document.getElementById('modal_create'));
    if (modal) {
        modal.hide();
    }
});