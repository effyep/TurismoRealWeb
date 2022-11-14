const tbNombres = document.getElementById("nombres");
const tbApellidos = document.querySelector("[name=apellidos]");
const tbUsuario= document.querySelector("[name=usuario]");
const tbEmail = document.querySelector("[name=email]");
const tbContrasena = document.querySelector("[name=contraseña]");
const tbRutPasaporte = document.querySelector("[name=identificacion]");
const tbCelular = document.querySelector("[name = celular]");
const tbPais = document.querySelector("[name = pais]");

async function traerUsuarios() {
    let response = await fetch('/ListarUsuarios')
    return await response.json();
}

const validarUsuario = e => {
    traerUsuarios().then(data => {
        for (x of data){
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

const validarCorreo = e => {
    traerUsuarios().then(data => {
        for (x of data){
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
        for (x of data){
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
        field.nextElementSibling.innerText = message;
        
    }
    else{
        field.nextElementSibling.classList.remove("error");
        field.nextElementSibling.innerText = "";
    }
}

const validarFormatoCorreo = e => {
    const field = e.target;
    const regex = new RegExp(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/);
    if(regex.test(field.value) == false){
        field.nextElementSibling.classList.add("error");
        field.nextElementSibling.innerText = "Ingrese un correo válido";
    }
    else{
        field.nextElementSibling.classList.remove("error");
        field.nextElementSibling.innerText = "";
    }
}







    
tbNombres.addEventListener("blur", (e) => validarCamposVacios("Los nombres no pueden quedar vacios",e));
tbApellidos.addEventListener("blur", (e) => validarCamposVacios("Los apellidos no pueden quedar vacios",e))
tbUsuario.addEventListener("blur", (e) => validarCamposVacios("El usuario no puede quedar vacio",e))
tbEmail.addEventListener("blur", (e) => validarCamposVacios("El correo no puede quedar vacio",e))
tbContrasena.addEventListener("blur", (e) => validarCamposVacios("Ingrese una contraseña",e))
tbRutPasaporte.addEventListener("blur", (e) => validarCamposVacios("La identificación no puede quedar vacia",e))
tbCelular.addEventListener("blur", (e) => validarCamposVacios("El celular no puede quedar vacio",e))
tbPais.addEventListener("blur", (e) => validarCamposVacios("El pais no puede quedar vacio",e))

tbEmail.addEventListener("blur", validarFormatoCorreo)

tbUsuario.addEventListener("blur", validarUsuario)
tbEmail.addEventListener("blur", validarCorreo)
tbRutPasaporte.addEventListener("blur",validarIdentificacion)
tbCelular.addEventListener("blur", validarCelular)