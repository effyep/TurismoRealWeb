$("#fechaInicio" && "#fechaSalida").change(function () {
    var fechaInicio = $(this).val();
    var fechaSalida = $(this).val();
    
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    $.ajax({
    url: 'detalleParaReservar',
    method: 'POST',
    data: {
        'fechaInicio': fechaInicio,
        'fechaSalida': fechaSalida
    },
    dataType: 'json',
    success: function (data) {
        if (data.disponibilidad) {
        alert("Username taken");
        }
    }
    });
});
