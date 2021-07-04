$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#txt_name').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#server_msg_modal').modal('show');
    }

});