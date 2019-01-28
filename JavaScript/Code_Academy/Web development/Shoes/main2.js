$(document).ready(() => {
 
  $('.login-button').on('click', () => {
    $('.login-form').toggle();
  });
  
  $('.menu-button').on('mouseenter', () => {
    $('.nav-menu').show();
    $('.menu-button').addClass('button-active');
    /*$('.menu-button').css({
      color: '#C3FF00',
    	backgroundColor: '#535353'
		});*/
    $('.menu-button').animate({
      fontSize: '24px'
    }, 200);
    $('.nav-menu').removeClass('hide');
  })
  
  $('.nav-menu').on('mouseleave', () => {
    $('.nav-menu').hide();
    $('.menu-button').removeClass('button-active');
    /*$('.menu-button').css({
      color: '#EFEFEF',
      backgroundColor: '#303030'
    });*/
    $('.menu-button').animate({
      fontSize: '18px'
    }, 200);
  })
  
}); 

/*$(document).ready(() => {
  $('.login-button').on('click', () => {
    $('.login-form').show();
  });
  
  $('.menu-button').on('click', () => {
   $('.nav-menu').toggleClass('hide');
   $('.menu-button').toggleClass('button-active');
  })  
}); 
*/
