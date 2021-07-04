$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorButton').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalButton').modal('show');
    }

});

$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorButtonRoot').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalButtonRoot').modal('show');
    }

});