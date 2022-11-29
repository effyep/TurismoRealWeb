

function a(){
    const huespedes = document.getElementById("huespedes").textContent;
    var huesped = 0;
    huespedess = Number(huespedes) - 1

    while(huesped <= huespedess){

        const nombreHuesped = document.createElement('input');
        nombreHuesped.name="huesped"+huesped;
        nombreHuesped.placeholder="Nombres"
        nombreHuesped.id= "nombreHuesped"+huesped
        nombreHuesped.className = "nombres"
        nombreHuesped.required = true


        const identificacionHuesped = document.createElement('input');
        identificacionHuesped.name="rut"+huesped;
        identificacionHuesped.id = "identificacion"+huesped
        identificacionHuesped.placeholder="Rut o Pasaporte"
        identificacionHuesped.className = "rut"
        identificacionHuesped.required = true

        const apellidoHuesped = document.createElement('input');
        apellidoHuesped.name="apellido"+huesped;
        apellidoHuesped.id="apellidoHuesped"+huesped;
        apellidoHuesped.placeholder = "Apellidos"
        apellidoHuesped.className = "apellidos"
        apellidoHuesped.required=true

        const div = document.createElement('div');
        div.className ="divhuesped"
        div.id="divhuesped"+huesped

        ///aca agrego los elementos
        document.getElementById('agregarHuespedes').appendChild(div);
        document.getElementById('divhuesped'+huesped).appendChild(nombreHuesped);
        document.getElementById('divhuesped'+huesped).appendChild(apellidoHuesped);
        document.getElementById('divhuesped'+huesped).appendChild(identificacionHuesped);
        
        huesped++;
}}
a()





