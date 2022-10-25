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