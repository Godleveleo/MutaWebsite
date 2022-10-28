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