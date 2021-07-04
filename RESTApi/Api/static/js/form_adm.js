$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valor').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modal').modal('show');
    }

});