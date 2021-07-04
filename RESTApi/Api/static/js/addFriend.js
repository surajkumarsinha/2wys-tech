$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorFriend').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalFriend').modal('show');
    }

});

$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorCirFriend').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalCirFriend').modal('show');
    }

});

