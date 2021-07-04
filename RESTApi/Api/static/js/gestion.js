$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorGestion').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalGestion').modal('show');
    }

});

