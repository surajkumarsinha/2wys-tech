
$(document).ready(function(){
    var $regexname=/^(([A-ZÁÉÍÓÚ a-zñáéíóú]{1}[a-zñáéíóú A-ZÁÉÍÓÚ ]+[\s]*)+)?$/;
    $('.NAME').on('keypress keydown keyup',function(){
             if (!$(this).val().match($regexname)) {
              // there is a mismatch, hence show the error message
                 $('#name').removeClass('hidden');
                 $('#name').show();
             }
           else{
                // else, do not display message
                $('#name').addClass('hidden');
               }
         });
});

$(document).ready(function(){
    var $regexDni=/^([\d]{10})?$/;
    $('.DNI').on('keypress keydown keyup',function(){
             if (!$(this).val().match($regexDni)) {
              // there is a mismatch, hence show the error message
                 $('#dni').removeClass('hidden');
                 $('#dni').show();
             }
           else{
                // else, do not display message
                $('#dni').addClass('hidden');
               }
         });
});

$(document).ready(function(){
    var $regexEmail=/^([\w]+@{1}[\w]+(\.[\w]+)*\.[a-z]{2,3})?$/;
    $('.EMAIL').on('keypress keydown keyup',function(){
             if (!$(this).val().match($regexEmail)) {
              // there is a mismatch, hence show the error message
                 $('#email').removeClass('hidden');
                 $('#email').show();
             }
           else{
                // else, do not display message
                $('#email').addClass('hidden');
               }
         });
});

$(document).ready(function(){
    var $regexEmail=/^([3]{1}[0|1|2]{1}[\d]{8})?$/;
    $('.TEL').on('keypress keydown keyup',function(){
             if (!$(this).val().match($regexEmail)) {
              // there is a mismatch, hence show the error message
                 $('#tel').removeClass('hidden');
                 $('#tel').show();
             }
           else{
                // else, do not display message
                $('#tel').addClass('hidden');
               }
         });
});

$(document).ready(function(){
    var $regexPassword=/^((?=(?:[a-zA-Z0-9]*[a-zA-Z]){2})(?=(?:[a-zA-Z0-9]*\d){2})[a-zA-Z0-9]{8,10})?$/;
    $('.PASS').on('keypress keydown keyup',function(){
             if (!$(this).val().match($regexPassword)) {
              // there is a mismatch, hence show the error message
                 $('#pass').removeClass('hidden');
                 $('#pass').show();
             }
           else{
                // else, do not display message
                $('#pass').addClass('hidden');
               }
         });
});