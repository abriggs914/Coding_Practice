$(document).ready(() => {
  /*In the main function in main.js, add a keyup event handler to '#text'. Make sure it takes a parameter: event.*/
  $('#text').on('keyup', event =>{
    /*
In the keyup callback function, call the html method on the '.preview' element and pass it the current value of $(event.currentTarget), the updated input field, by using the .val() method.

Then test that entered text is being added to the preview after each keystroke.*/
  	$('.preview').html($(event.currentTarget).val());
    /*Under the keyup method, attach a change event handler to the <select> field with an id of "font".

The change event handler will fire anytime the selected value of the '#font' menu changes.*/
    /*n the callback function of the change event handler, use the css method to change the value of the '.preview' element's font-family property to the current value of this menu.

Now test your app to see that the font of the preview text changes when you select a different font.*/
    $('#font').on('change', event => {
      $('.preview').css('font-family', $(event.currentTarget).val());
    });
    
    /*
Now add another change event handler, this time to the weight menu.

Just like in the last task, have the callback function set the preview element's font-weight property to the current value of this menu.

Test that the font-weight changes.*/
    $('#weight').on('change', event => {
      $('.preview').css('font-weight', $(event.currentTarget).val());
    });
    
    /*
Since the font-size input field requires text to be entered, we'll use a keyup event handler to change the font-weight of the preview text.

Add a keyup event handler to the font-size field.*/
    $('#size').on('keyup', event => {
      /*
In the callback function of the keyup event handler, create a variable called fontSize. Set it to the current value of this field, and use the + operator to add 'px'. We do this because we will need to specify the unit for the CSS font-size property in the next step.*/
      let fontSize = $(event.currentTarget).val() + 'px';
      //alert(fontSize);
      $('.preview').css({
        fontSize:  fontSize
      });
    });
  });
})