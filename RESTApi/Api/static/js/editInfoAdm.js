$(document).ready(function(){
    var flag = false;
    try{
      flag = $('#valor2').val();
    }catch(err){
      flag = false;
    }
    console.log(flag);
    if (flag) {
       $('#modal2').modal('show');
    }

});

$(document).ready(function(){
    var $regexEmail=/^([\w]+@{1}[\w]+(\.[\w]+)*\.[a-z]{2,3})?$/;
    $('.EMAIL2').on('keypress keydown keyup',function(){
             if (!$(this).val().match($regexEmail)) {
              // there is a mismatch, hence show the error message
                 $('#email2').removeClass('hidden');
                 $('#email2').show();
             }
           else{
                // else, do not display message
                $('#email2').addClass('hidden');
               }
         });
});