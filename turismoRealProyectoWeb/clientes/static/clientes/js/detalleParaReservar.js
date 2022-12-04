const txtCantidad = document.querySelectorAll('.cantidad');
const checkboxs = document.querySelectorAll('.checkbox');
const fechaInicio = document.getElementById('inicio');
const fechaSalida = document.getElementById('fechaSalida')
const form = document.getElementById('post-form');

txtCantidad.forEach(cantidad => {
    cantidad.addEventListener("change", function(e){
        a = e.target.value
        if(a > 0){
            cantidad.nextElementSibling.checked = true;
        }
        else{
            cantidad.nextElementSibling.checked = false;
            a= NaN
        }
    })
})

var fechaI = fechaInicio.addEventListener('change',function(){
    valor = String(this.value)
    let fi = new Date(valor)
    console.log(fi)
    fechaI= fi
})

var fechaS= fechaSalida.addEventListener('change',function(){
    valor = String(this.value)
    let fs = new Date(valor)
    console.log(fs)
    fechaS = fs
})

function compararFechas(fechaInicio, fechaSalida){
    if (fechaInicio > fechaSalida){
        return 1;
    }
    else
        return 0
    }

form.addEventListener('submit', function(e) {
    console.log("se presiono")
    var result = compararFechas(fechaI,fechaS)
    if(result == 1){
        e.preventDefault()
        Swal.fire({
            "title": "Atención",
            "text": "La fecha de ingreso no debe ser menor a la de la salida, revise sus datos",
            "icon": "warning"
        })
        document.getElementById('inicio').value = ""
        document.getElementById('fechaSalida').value = ""
        
    }  
})
