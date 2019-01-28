/*Note that the jQuery library has already been loaded for you at the bottom of the file.

In the header, there are three <div class="dropdown"> elements with the following ids: #cart, #account, and #help.

When a dropdown is moused over, we want its corresponding <ul class="dropdown-menu"> element to appear, then disappear when the mouse leaves the .dropdown-menu.

In main.js, start by using jQuery to add a ready method call to the document.*/

/*
In the .ready() callback function, add click event handlers to '#cart', '#account', and '#help'.

Add an empty callback function to each event.*/
$(document).ready(() => {
  $('#cart').on('click', () => {
    	$('#cartMenu').show();
    });
 $('#account').on('click', () => {
    	$('#accountMenu').show();
    });
  $('#help').on('click', () => {
    	$('#helpMenu').show();	
    });
  /*
Under the click event handlers, add a mouseleave event handler to each of the '.dropdown-menu's. Add an empty callback function.

Try targeting by class this time.*/
  /*
Inside of the callback function, use a jQuery method to make the drop-down menu disappear.*/
  $('#cartMenu').on('mouseleave', () => {
    	$('#cartMenu').hide();
    });
  $('#accountMenu').on('mouseleave', () => {
    	$('#accountMenu').hide();
    });
  $('#helpMenu').on('mouseleave', () => {
    	$('#helpMenu').hide();	
    });
});