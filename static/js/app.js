// Informacion del pegue
const pegueSelect = document.getElementById("input-buscar-pegue");
const abonadoInfo = document.getElementById("abonado-info");
const dniInfo = document.getElementById("dni-info");
const tarifa = document.getElementById("tarifa-info");
const serviciosInfo = document.getElementById("servicios-info");
const barrioInfo = document.getElementById("barrio-info");
const totalPagar = document.getElementById("display-total-pagar");
const lineaDistribucionInfo = document.getElementById(
  "linea-distribucion-info"
);
const ultimoPagoInfo = document.getElementById("ultimo-pago-info");
const fechaUltimoPagoInfo = document.getElementById("fecha-ultimo-pago-info");
const aniosCancelados = document.querySelectorAll(`input[name="anio-cobro"]`);
const mesesCancelados = document.querySelectorAll(`input[name="meses-cobro"]`);

let tPS = document.getElementById("total-pagar-send");
let pIS = document.getElementById("pegue-id-send");

pegueSelect.value = "";

meses = [
  "ENE",
  "FEB",
  "MAR",
  "ABR",
  "MAY",
  "JUN",
  "JUL",
  "AGO",
  "SEP",
  "OCT",
  "NOV",
  "DIC",
];

// Buscador de pegue
document
  .getElementById("buscar-pegue")
  .addEventListener("click", capturarDatosAbonado);

function capturarDatosAbonado() {
  const pegue = pegueSelect.value.toUpperCase();
  fetch(`/pegues/obtener_informacion_pegue/${pegue}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(pegue + " No encontrado");
      }

      return response.json();
    })
    .then((data) => {
      limpiarCampos();
      let tieneUltimoPago = data.ultimo_pago != null ? true : false;
      abonadoInfo.classList.add("font-weight-bold", "text-success");
      dniInfo.textContent = data.dni;
      abonadoInfo.textContent = data.nombre;
      tarifa.textContent = data.tarifa_mensual;
      barrioInfo.textContent = data.barrio;
      lineaDistribucionInfo.textContent = data.linea_distribucion;
      serviciosInfo.textContent = data.servicios.join(" | ");
      console.log("Datos recibidos:", data);
      console.log("Ultimo Pago:", data.ultimo_pago);

      if (tieneUltimoPago) {
        ultimoPagoInfo.textContent =
          meses[data.ultimo_pago.mes - 1] + "/" + data.ultimo_pago.anio;
        fechaUltimoPagoInfo.textContent = new Date(
          data.ultimo_pago.fecha_pago
        ).toLocaleDateString("es-MX", {
          weekday: "long",
          day: "numeric",
          month: "long",
          year: "numeric",
        });

        checarMeses(data);
      } else {
        ultimoPagoInfo.textContent = "-- Sin pagos --";
        fechaUltimoPagoInfo.textContent = "-- Sin pagos --";
        aniosCancelados.forEach((a) => {
          a.checked = false;
          a.disabled = false;
        });
        mesesCancelados.forEach((m) => {
          m.checked = false;
          m.disabled = false;
        });
      }

      switch (data.tarifa_mensual) {
        case "50.00":
          tarifa.className = "";
          tarifa.classList.add("font-weight-bold");
          break;
        case "100.00":
          tarifa.className = "";
          tarifa.classList.add("font-weight-bold", "text-success");
          break;
        default:
          break;
      }
    })
    .catch((error) => {
      limpiarCampos(error);
      abonadoInfo.classList.add("font-weight-bold", "text-danger");
      abonadoInfo.textContent = error;
      console.error(error);
    });
}

function limpiarCampos() {
  abonadoInfo.className = "";
  abonadoInfo.className = "";
  dniInfo.textContent = "--";
  tarifa.textContent = "--";
  barrioInfo.textContent = "--";
  lineaDistribucionInfo.textContent = "--";
  serviciosInfo.textContent = "";
  ultimoPagoInfo.textContent = "--";
  fechaUltimoPagoInfo.textContent = "--";
  tarifa.value = "";
  totalPagar.textContent = "L 0.00";

  tPS.value = "";
  pIS.value = "";
  aniosCancelados.forEach((a) => {
    a.checked = false;
    a.disabled = true;
  });
  mesesCancelados.forEach((m) => {
    m.checked = false;
    m.disabled = true;
  });
}

function checarMeses(data) {
  const ultimoAnioPagado = data.ultimo_pago.anio;
  const ultimoMesPagado = data.ultimo_pago.mes;


  if (ultimoMesPagado != 12) {
    Array.from(mesesCancelados).forEach((mesInput, indice) => {
      if (indice >= ultimoMesPagado) {
        mesInput.checked = false;
        mesInput.disabled = false;
      }
    });
  } else {
    mesesCancelados.forEach((m) => {
      m.checked = false;
      m.disabled = false;
    });
  }
  
  habilitarSiguienteAnio = false;
  
  for (const a of aniosCancelados) {
    const anioActual = a.value;

    if(habilitarSiguienteAnio)
      a.disabled = false;
      habilitarSiguienteAnio = false;

    if (anioActual == ultimoAnioPagado && ultimoMesPagado != 12) {
        a.disabled = false;
      }else if(anioActual == ultimoAnioPagado && ultimoMesPagado == 12){
        habilitarSiguienteAnio=true;
        console.log(anioActual);
        
      }

  }

  console.log(
    "Pagado hasta: ",
    data.ultimo_pago.mes,
    " / ",
    data.ultimo_pago.anio,
    aniosCancelados
  );
}

mesesCancelados.forEach((checkbox) => {
  checkbox.addEventListener("change", calcularTotalAPagar);
});

function calcularTotalAPagar() {
  montoTotal = contarCheckboxMarcados() * parseInt(tarifa.textContent);
  totalPagar.textContent = `L ${montoTotal}.00`;

  llenarDatosHidden();
}

document.addEventListener("DOMContentLoaded", (event) => {
  limpiarCampos();
  const linkAbonadoElements = document.querySelectorAll(".link_abonado");
  linkAbonadoElements.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const codigoPegue = this.id;
      console.log("Codigo pegue seleccionado:", codigoPegue);
      pegueSelect.value = codigoPegue;
      capturarDatosAbonado();
    });
  });
});

// Asegúrate de que este script se ejecute DESPUÉS de que se cargue el formulario en el DOM.

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector('form[method="POST"]');

  // Función que valida si al menos un checkbox está marcado
  function validarMeses() {
    let checkedCount = contarCheckboxMarcados();
    console.log(checkedCount);

    return checkedCount > 0;
  }

  form.addEventListener("submit", function (event) {
    if (!validarMeses()) {
      event.preventDefault(); // Detiene el envío del formulario

      alert("¡Atención! Debe seleccionar al menos un mes para el cobro.");

      const primerCheckbox = document.querySelector(
        'input[name="meses-cobro"]'
      );
      if (primerCheckbox) primerCheckbox.focus();
    }
  });
});

function contarCheckboxMarcados() {
  let checkedCount = 0;
  // Contar los checkboxes marcados
  mesesCancelados.forEach((checkbox) => {
    if (checkbox.checked) {
      checkedCount++;
    }
  });

  return checkedCount;
}

function llenarDatosHidden() {
  tPS.value = montoTotal;
  pIS.value = pegueSelect.value;
}

// Informacion del Cobro
const fechaCobro = document.getElementById("fecha-cobro-info");
const anioAPagar = document.getElementById("anio-pagar-info");
const mesesAPagar = document.getElementById("meses-pagar-info");
const formaPago = document.getElementById("forma-pago-info");

fechaCobro.textContent = new Date().toLocaleString("es-MX");
//anioAPagar.add(document.createElement(new Date().getFullYear()));