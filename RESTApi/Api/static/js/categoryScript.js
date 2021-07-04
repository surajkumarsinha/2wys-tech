$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorMsg').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalMsg').modal('show');
    }

});

$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorMsgSuccess').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalMsgSuccess').modal('show');
    }

});

$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorCategory').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalCategory').modal('show');
    }

});