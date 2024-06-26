/* FUNCION PARA VALIDACIONES DE REGISTRO*/
/*para que se pueda validar la estructura del correo*/
var expr = /^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-\.]+$/;
$(document).ready(function(){
    $("#enviar").submit(function(event){
        // Evitar que el formulario se envíe automáticamente
        event.preventDefault();
        
        // Realizar las validaciones inicio sesión
        var nombre = $("#nombre").val();
        var apellido = $("#apellido").val();
        var Username = $("#Username").val();
        var Email = $("#Email").val();
        var contrasena = $("#contrasena").val();
        var direccion = $("#direccion").val();

        // Realizar validaciones registro
        var nombre1 = $("#nombre1").val();
        var correo = $("#correo").val();
        var contrasena1 = $("#contrasena1").val();
        var contrasena2 = $("#contrasena2").val();
        var check = $("#checkbox").prop("checked");

        // Validacion registro
        if(nombre1 === ""){
            $("#mensaje1").fadeIn(); 
            return false; 
        }else{
            $("#mensaje1").fadeOut();
            if(correo === "" || !expr.test(correo)){ 
                $("#mensaje2").fadeIn();
                return false;
            }else{
                $("#mensaje2").fadeOut();
                if(contrasena1 === ""){
                    $("#mensaje3").fadeIn();
                    return false;
                }else{
                    $("#mensaje3").fadeOut();
                    if(contrasena2 === ""){
                        $("#mensaje4").fadeIn();
                        return false;
                    }else{
                        $("#mensaje4").fadeOut();
                        if(check === false){
                            $("#mensaje5").fadeIn();
                            return false;
                        }else{
                            $("#mensaje5").fadeOut();
                            alert("Registro exitoso");
                        }
                    }
                }
            }
        }
        
        // Validación inicio sesión
        // Nombre: largo entre 3 y 20 caracteres
        if(nombre.length < 3 || nombre.length > 20){
            alert("El Nombre deben tener entre 3 y 20 caracteres.");
            return;
        }

        // Apellidos: largo entre 3 y 20 caracteres
        if(apellido.length < 3 || apellido.length > 20){
            alert("El Apellidos deben tener entre 3 y 20 caracteres.");
            return;
        }

        // Username: largo entre 3 y 20 caracteres
        if(Username.length < 3 || Username.length > 20){
            alert("El Username deben tener entre 3 y 20 caracteres.");
            return;
        }

        // contraseña: largo entre 8 y 15 caracteres
        if(contrasena.length < 8 || contrasena.length > 15){
            alert("la contraseña debe tener entre 8 y 15 caracteres.");
            return;
        }

        // Email: largo entre 10 y 30 caracteres
        if(Email.length < 10 || Email.length > 30){
            alert("El Email deben tener entre 10 y 30 caracteres.");
            return;
        }

        // Verificar si el Email termina con .com o .cl
        var dominioValido = /\.com$|\.cl$/;
        if (!dominioValido.test(Email)) {
            alert("El Email debe terminar en .com o .cl.");
            return;
        }

        // Email: largo entre 5 y 25 caracteres
        if(direccion.length < 5 || direccion.length > 25){
            alert("La direccion deben tener entre 5 y 25 caracteres.");
            return;
        }

        // alert("Registro exitoso")
        
        // Restablecer el formulario
        $("#registroForm")[0].reset();

        // Aquí podrías enviar el formulario utilizando AJAX o cualquier otro método
    });
});




/* FUNCION PARA VALIDACIONES DE SUSCRIPCION*/






