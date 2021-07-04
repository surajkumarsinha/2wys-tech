$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valorCheckBox').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modalCheckBox').modal('show');
    }

});