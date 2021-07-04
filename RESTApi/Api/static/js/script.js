$(function(){
  $("#registro1").popover({
    placement: 'bottom',
    html: true,
    content : '<button type="button" class="btn btn-danger btn-sm" id="admReg" style=" background-color: #3a906d; border-color: #3a906d" >Administrador</button> <button type="button" id="egresadoReg" style=" background-color: #3a906d; border-color: #3a906d" class="btn btn-success btn-sm">Egresado</button>'
  })
  $('html').click(function() {
    $('#close').popover()
    .click(function(e){
      e.preventDefault();
      $(this).focus();
    });
  });
});

$('body').on('click', 'button#admReg', function() {
    $(location).attr('href','pre_registro_admin');
});
$('body').on('click', 'button#egresadoReg', function() {
    $(location).attr('href','pre_registro_egresado');
});

$(function(){
  $("#registro2").popover({
    placement: 'bottom',
    html: true,
    content : '<button type="button" class="btn btn-danger btn-sm" id="admReg2" style=" background-color: #3a906d; border-color: #3a906d" >Administrador</button> <button type="button" id="egresadoReg2" style=" background-color: #3a906d; border-color: #3a906d" class="btn btn-success btn-sm">Egresado</button>'
  })
  $('html').click(function() {
    $('#close').popover()
    .click(function(e){
      e.preventDefault();
      $(this).focus();
    });
  });
});
$('body').on('click', 'button#admReg2', function() {
    $(location).attr('href','pre_registro_admin');
});
$('body').on('click', 'button#egresadoReg2', function() {
    $(location).attr('href','pre_registro_egresado');
});

$(function(){
  $("#registro_nav").popover({
    placement: 'bottom',
    html: true,
    content : '<button type="button" class="btn btn-danger btn-sm" id="admReg3" style=" background-color: #3a906d; border-color: #3a906d" >Administrador</button> <button type="button" id="egresadoReg3" style=" background-color: #3a906d; border-color: #3a906d" class="btn btn-success btn-sm">Egresado</button>'
  })
  $('html').click(function() {
    $('#close').popover()
    .click(function(e){
      e.preventDefault();
      $(this).focus();
    });
  });
});
$('body').on('click', 'button#admReg3', function() {
    $(location).attr('href','pre_registro_admin');
});
$('body').on('click', 'button#egresadoReg3', function() {
    $(location).attr('href','pre_registro_egresado');
});



$(function(){
  $("#registro_nav_hide").popover({
    placement: 'bottom',
    html: true,
    content : '<center><button type="button" class="btn btn-danger btn-sm" id="admRegH" style=" background-color: #3a906d; border-color: #3a906d" >Administrador</button><br><br><button type="button" id="egresadoRegH" style=" background-color: #3a906d; border-color: #3a906d" class="btn btn-success btn-sm">Egresado</button></center>'
  })
  $('html').click(function() {
    $('#close').popover()
    .click(function(e){
      e.preventDefault();
      $(this).focus();
    });
  });
});

$('body').on('click', 'button#admRegH', function() {
    $(location).attr('href','pre_registro_admin');
});
$('body').on('click', 'button#egresadoRegH', function() {
    $(location).attr('href','pre_registro_egresado');
});

$(function(){
    $("#ingreso1").popover({
      placement: 'bottom',
      html: true,
      content : '<button type="button" class="btn btn-danger btn-sm" id="admIng" style=" background-color: #3a906d; border-color: #3a906d" >Administrador</button> <button type="button" id="egresadoIng" style=" background-color: #3a906d; border-color: #3a906d" class="btn btn-success btn-sm">Egresado</button>'
    })
  $('html').click(function() {
    $('#close').popover()
    .click(function(e){
      e.preventDefault();
      $(this).focus();
    });
  });
});
$('body').on('click', 'button#admIng', function() {
    $(location).attr('href','login_admin');
});
$('body').on('click', 'button#egresadoIng', function() {
    $(location).attr('href','login_egresado');
});

$(function(){
    $("#ingreso2").popover({
      placement: 'bottom',
      html: true,
      content : '<button type="button" class="btn btn-danger btn-sm" id="admIng2" style=" background-color: #3a906d; border-color: #3a906d" >Administrador</button> <button type="button" id="egresadoIng2" style=" background-color: #3a906d; border-color: #3a906d" class="btn btn-success btn-sm">Egresado</button>'
    })
  $('html').click(function() {
    $('#close').popover()
    .click(function(e){
      e.preventDefault();
      $(this).focus();
    });
  });
});
$('body').on('click', 'button#admIng2', function() {
    $(location).attr('href','login_admin');
});
$('body').on('click', 'button#egresadoIng2', function() {
    $(location).attr('href','login_egresado');
});

$(function(){
  $("#login_nav").popover({
    placement: 'bottom',
    html: true,
    content : '<center><button type="button" class="btn btn-danger btn-sm" id="admIn3" style=" background-color: #3a906d; border-color: #3a906d" >Administrador</button><br><br> <button type="button" id="egresadoIng3" style=" background-color: #3a906d; border-color: #3a906d" class="btn btn-success btn-sm">Egresado</button></center>'
  })
  $('html').click(function() {
    $('#close').popover()
    .click(function(e){
      e.preventDefault();
      $(this).focus();
    });
  });
});

$('body').on('click', 'button#admIn3', function() {
    $(location).attr('href','login_admin');
});
$('body').on('click', 'button#egresadoIng3', function() {
    $(location).attr('href','login_egresado');
});


$(function(){
  $("#registro_responsive").popover({
    placement: 'bottom',
    html: true,
    content : '<button type="button" class="btn btn-danger btn-sm" id="admRegR" style=" background-color: #3a906d; border-color: #3a906d" >Administrador</button> <button type="button" id="egresadoRegR" style=" background-color: #3a906d; border-color: #3a906d" class="btn btn-success btn-sm">Egresado</button>'
  })
  $('html').click(function() {
    $('#close').popover()
    .click(function(e){
      e.preventDefault();
      $(this).focus();
    });
  });
});

$('body').on('click', 'button#admRegR', function() {
    $(location).attr('href','pre_registro_admin');
});
$('body').on('click', 'button#egresadoRegR', function() {
    $(location).attr('href','pre_registro_egresado');
});

$(function(){
  $("#ingreso_responsive").popover({
    placement: 'bottom',
    html: true,
    content : '<button type="button" class="btn btn-danger btn-sm" id="admInR" style=" background-color: #3a906d; border-color: #3a906d" >Administrador</button> <button type="button" id="egresadoIngR" style=" background-color: #3a906d; border-color: #3a906d" class="btn btn-success btn-sm">Egresado</button>'
  })
  $('html').click(function() {
    $('#close').popover()
    .click(function(e){
      e.preventDefault();
      $(this).focus();
    });
  });
});

$('body').on('click', 'button#admInR', function() {
    $(location).attr('href','login_admin');
});
$('body').on('click', 'button#egresadoIngR', function() {
    $(location).attr('href','login_egresado');
});

$(function(){
     // Find any date inputs and override their functionality
     $('input[type="date"]').datepicker();
});
        



