function delete_dato(id){
    Swal.fire({
      "title": "¿Estas seguro?",
    //   "text": "{{message}}",
      "icon": "question",
      "showCancelButton":true,
      "cancelButtonText":"No, Cancelar",
      "confirmButtonText":"Si, eliminar",
      "reverseButtons":true,
      "confirmButtonColor":"#bb2d3b"            

    })
    .then(function(result){
      if(result.isConfirmed){
        window.location.href = "/deletegym/"+id+"/"
      }
    })
  }

function delete_plan(id){
    Swal.fire({
      "title": "¿Estas seguro?",
    //   "text": "{{message}}",
      "icon": "question",
      "showCancelButton":true,
      "cancelButtonText":"No, Cancelar",
      "confirmButtonText":"Si, eliminar",
      "reverseButtons":true,
      "confirmButtonColor":"#bb2d3b"            

    })
    .then(function(result){
      if(result.isConfirmed){
        window.location.href = "/deleteplan/"+id+"/"
      }
    })
  }
function delete_clase(id){
    Swal.fire({
      "title": "¿Estas seguro?",
    //   "text": "{{message}}",
      "icon": "question",
      "showCancelButton":true,
      "cancelButtonText":"No, Cancelar",
      "confirmButtonText":"Si, eliminar",
      "reverseButtons":true,
      "confirmButtonColor":"#bb2d3b"            

    })
    .then(function(result){
      if(result.isConfirmed){
        window.location.href = "/deleteclase/"+id+"/"
      }
    })
  }

  function crear_gym()
  {
     var form=document.form;
     if(form.logo.value==0)
     {
         form.foto.value='vacio';
     }
     form.submit();
    }
  function editar_gym()
  {
     var form=document.form;
     if(form.logo.value==0)
     {
         form.foto.value='vacio';
     }
     form.submit();
    }
  
    function soloNumeros(evt) {
      key = (document.all) ? evt.keyCode : evt.which;
      //alert(key);
      if (key == 17) return false;
      /* digitos,del, sup,tab,arrows*/
      return ((key >= 48 && key <= 57) || key == 8 || key == 127 || key == 9 || key == 0);
  }

  function reservar()
  {
     var form=document.form;
     if(form.cupo_reservado.value==0)
     {
         form.reserva.value=form.cupo.value;
     }
     form.submit();
    }

