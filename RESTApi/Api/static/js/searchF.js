$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorFinal').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalFinal').modal('show');
    }

});