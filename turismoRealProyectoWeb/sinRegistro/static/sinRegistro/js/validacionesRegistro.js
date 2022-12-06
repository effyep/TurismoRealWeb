const tbNombres = document.getElementById("nombres");
const tbApellidos = document.querySelector("[name=apellidos]");
const tbUsuario= document.querySelector("[name=usuario]");
const tbEmail = document.querySelector("[name=email]");
const tbContrasena = document.querySelector("[name=contraseña]");
const tbRepetirContrasena = document.getElementById("repcontraseña");
const tbRutPasaporte = document.querySelector("[name=identificacion]");
const tbCelular = document.querySelector("[name = celular]");
const tbPais = document.querySelector("[name = pais]");

const form = document.getElementById('post-form');

async function traerUsuarios() {
    let response = await fetch('/ListarUsuarios')
    return await response.json();
}

const validarUsuario = e => {
    traerUsuarios().then(data => {
        for (let x of data){
            const field = e.target.value;
            const f = e.target;
            if(field == x.usuario){
                f.nextElementSibling.classList.add("error");
                f.nextElementSibling.innerText = "El nombre de usuario ya está en uso";

                break
            }
            else{
                f.nextElementSibling.classList.remove("error");
                f.nextElementSibling.innerText = "";
            }
        }
    })
}

const validarCorreoExistente = e => {
    traerUsuarios().then(data => {
        for (let x of data){
            const field = e.target.value;
            const f = e.target;
            if(field == x.correo){
                f.nextElementSibling.classList.add("error");
                f.nextElementSibling.innerText = "El correo ya está en uso";

                break
            }
            else{
                f.nextElementSibling.classList.remove("error");
                f.nextElementSibling.innerText = "";

            }
        }
    })
}

const validarIdentificacion = e => {
    traerUsuarios().then(data => {
        for (let x of data){
            const field = e.target.value;
            const f = e.target;
            if(field == x.identificacion){
                f.nextElementSibling.classList.add("error");
                f.nextElementSibling.innerText = "El rut/pasaporte ya está en uso";

                break
            }
            else{
                f.nextElementSibling.classList.remove("error");
                f.nextElementSibling.innerText = "";

            }
        }
    })
}

const validarCelular = e => {
    traerUsuarios().then(data => {
        for (x of data){
            const field = e.target.value;
            const f = e.target;
            if(field == x.celular){
                f.nextElementSibling.classList.add("error");
                f.nextElementSibling.innerText = "El celular ya está en uso";

                break
            }
            else{
                f.nextElementSibling.classList.remove("error");
                f.nextElementSibling.innerText = "";
            }
        }
    })
}


const validarCamposVacios = (message, e) => {
    const field = e.target;
    const valorCampo = e.target.value;
    if(valorCampo.trim().length == 0 ){
        field.nextElementSibling.classList.add("error");
        field.nextElementSibling.innerText = message;}

    else
    {
        field.nextElementSibling.classList.remove("error");
        field.nextElementSibling.innerText = "";
    }
}

var Fn = {
	// Valida el rut con su cadena completa "XXXXXXXX-X"
	validaRut : function (rutCompleto) {
		if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test( rutCompleto ))
			return false;
		var tmp 	= rutCompleto.split('-');
		var digv	= tmp[1]; 
		var rut 	= tmp[0];
		if ( digv == 'K' ) digv = 'k' ;
		return (Fn.dv(rut) == digv );
	},
	dv : function(T){
		var M=0,S=1;
		for(;T;T=Math.floor(T/10))
			S=(S+T%10*(9-M++%6))%11;
		return S?S-1:'k';
	}
}


const validarSintaxisRut = e =>{
    const field = e.target;
    const valor = e.target.value
    const rut = valor.toString()

    if(!Fn.validaRut(rut)){
        field.nextElementSibling.classList.add("error");
        field.nextElementSibling.innerText = "Ingrese un rut válido";
    }
    else{
        field.nextElementSibling.classList.remove("error");
        field.nextElementSibling.innerText = "";
        validarCorreoExistente(e)
    }
}

const validarCorreo = e => {
    const field = e.target;
    const regex = new RegExp(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/);
    if(!regex.test(field.value)){
        field.nextElementSibling.classList.add("error");
        field.nextElementSibling.innerText = "Ingrese un correo válido";

    }
    else{
        field.nextElementSibling.classList.remove("error");
        field.nextElementSibling.innerText = "";
        validarCorreoExistente(e)}}

tbNombres.addEventListener("blur",(e) => validarCamposVacios("Los nombres no pueden quedar vacios",e))
tbApellidos.addEventListener("blur", (e) => validarCamposVacios("Los apellidos no pueden quedar vacios",e))

tbCelular.addEventListener("blur",(e) => validarCamposVacios("El celular no puede quedar vacio",e))
tbCelular.addEventListener("blur",(e)=> validarCelular(e))
tbCelular.addEventListener("blur",(e) => validarCelu("Ingrese 8 digitos para el celular",e))


tbRepetirContrasena.addEventListener("blur", (e) => {
    const field = e.target;
    const valor =  field.value;
    const valorContrasena = tbContrasena.value;
    if(valor != valorContrasena){
        field.nextElementSibling.classList.add("error");
        field.nextElementSibling.innerText = "Las contraseñas no son iguales";
        

    }
    else{
        field.nextElementSibling.classList.remove("error");
        field.nextElementSibling.innerText = "";
    }
})


tbContrasena.addEventListener("blur", (e) => validarCamposVacios("Ingrese una contraseña",e))


tbUsuario.addEventListener("blur",(e) => validarUsuario(e))
tbUsuario.addEventListener("blur",(e)=> validarCamposVacios("El usuario no puede quedar vacio",e))

tbPais.addEventListener("blur", (e) => validarCamposVacios("El pais no puede quedar vacio",e))



//detecta cualquier click en el input email y se hacen todas las validaciones para el campo Email 
tbEmail.addEventListener('blur', (e) =>{
    var valor = e.target.value;

    if(valor.length == 0){
        validarCamposVacios("El correo no puede quedar vacio",e)
    }
    else if(valor.length > 0){
        ///dentro de este metodo se valida la sintaxis del correo y de estar correcto, la disponibilidad de este
        validarCorreo(e)
    }})


const validarRut = (e,mensaje,tipo) =>{
    const field = e.target;
    valor = e.target.value

    switch(tipo){
        case tipo = 'rut':
            if(valor.length < 10 || valor.length >10){
                field.nextElementSibling.classList.add("error")
                field.nextElementSibling.innerText = mensaje;  
            }
            else{
                field.nextElementSibling.classList.remove("error")
                field.nextElementSibling.innerText = ""
            }
            break
        
        case tipo = 'pasaporte':
            if (valor.length < 7 || valor.length > 7){
                field.nextElementSibling.classList.add("error")
                field.nextElementSibling.innerText = mensaje;

            }
            else{
                field.nextElementSibling.classList.remove("error")
                field.nextElementSibling.innerText = ""
                }
            break
            }
}

const fnid = tbRutPasaporte.addEventListener("click", (e) => {
    var valor = e.target.value;
    primercaracter = valor.charAt(0)

    console.log(isNaN(primercaracter))
    if(valor.length === 0 ){
        validarCamposVacios("La identificación no puede quedar vacia",e)

    }
    else if((valor.length < 9) && isNaN(primercaracter) === false){
        validarRut(e,"Ingrese su rut sin puntos y con guión",'rut')
    }
    else if((valor.length > 10) && isNaN(primercaracter) === false){
        validarRut(e,"Ingrese su rut sin puntos y con guión",'rut')
    }
    else if((valor.length < 7) && isNaN(primercaracter) === true){
        validarRut(e,"Ingrese 7 digitos para el pasaporte",'pasaporte')
        
    }
    else if((valor.length > 7) && isNaN(primercaracter) === true){
        validarRut(e,"Ingrese 7 digitos para el pasaporte",'pasaporte')
      
    }
    else if(valor.length === 10 || valor.length === 9){
        validarSintaxisRut(e)
    }
})




const validarCelu = (message, e) => {
    const field = e.target;
    const valorCampo = e.target.value;
    if(valorCampo.length < 8){
        field.nextElementSibling.classList.add("error");
        field.nextElementSibling.innerText = message;
        
    }
    else if(valorCampo.length > 8){
        field.nextElementSibling.classList.add("error");
        field.nextElementSibling.innerText = message;
    }

    else if((valorCampo.length === 8))
    {
        field.nextElementSibling.classList.remove("error");
        field.nextElementSibling.innerText = "";
    }
}

