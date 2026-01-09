// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    // FUERZA A USAR EL RENDERIZADO DE BOOTSTRAP PARA LA PÁGINACIÓN Y EL CONTENEDOR
    "renderer": "bootstrap", 
    // Asegura que los números de paginación se muestren correctamente
    "pagingType": "full_numbers" 
  });
});
