const txtCantidad = document.querySelectorAll('.cantidad');
const checkboxs = document.querySelectorAll('.checkbox');

const fechaInicio = document.getElementById('inicio');

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


fechaInicio.addEventListener('change',function(){
    console.log(this.value)
    
})



