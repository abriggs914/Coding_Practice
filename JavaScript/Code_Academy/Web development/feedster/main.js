$(document).ready(() => {
  /*In the next two steps, you will make a navigation menu appear when you hover over menu, and make it disappear when you navigate away from the navigation menu.

Add an event handler to main.js that shows the .nav-menu element when a user mouses over the .menu element.*/
	$('.menu').on('mouseenter', () => {
    $('.nav-menu').show();
  });
  /*
Add an event handler to main.js that hides the .nav-menu element when a user's mouse leaves the .nav-menu element.*/
	$('.nav-menu').on('mouseleave', () => {
    $('.nav-menu').hide();
  });
  
  /*
In the next three steps, you will add hover functionality to the +1 button elements.

Add an event handler to main.js that adds the .btn-hover class to .btn elements when a user mouses over a .btn element.*/
  /*Chain a mouse leave event handler to the mouse enter event handler you added the last step.

Inside the callback function, remove the .btn-hover class from .btn.*/
  /*feedster wants to display the remaining number of characters that a user can enter into their comment box.

Each time the user types a letter, we want to change the character count. For this we can use the keyup event listener.

In main.js, use the .on() method to add a keyup event listener to the '.postText' element. Leave the callback function empty until the next step.*/
  $('.btn').on('mouseenter', event => {
    $(event.currentTarget).addClass('btn-hover');
  }).on('mouseleave', event => {
    $(event.currentTarget).removeClass('btn-hover');
  })
  
  /*There are multiple +1 buttons, and we only want the current button to change when a user's mouse enters and leaves.

Change the .btn callback functions so only the current button is impacted by mouse enter and mouse leave events.*/
  $('.postText').on('keyup', event => {
    /*In main.js, call jQuery's .focus() method on '.postText'. This will cause the <textarea> to expect typed text as soon as the page loads.*/
    $('.postText').focus();
    /*
After each keyup event, we want to count the number of characters in the new post.

Add an event argument to the keyup event listener's callback function.

Inside the callback function, declare a variable called post and set it equal to $(event.currentTarget).val(). This will set post equal to the string inside the .postText element.*/
    let post = $(event.currentTarget).val();
    /*Now let's use a bit of JavaScript and math to determine the number of characters a user has left for their comment.

Under the post variable, declare another variable called remaining and set it to 140 minus the length of post.*/
    let remaining = 140 - post.length;
    /*Now that we know how many characters the user has left, we need to update that number in the HTML.

Still in the keyup callback function, add the following jQuery code.

$('.characters').html(remaining);
The code above will update the number of characters remaining.

Run the code and try typing a new post. You should see the character number change after each keystroke.*/
    /*To finish, let's make the '.wordcount' message turn red if the user runs out of characters. To do this, we will use a simple if/else statement.

Under the remaining variable declaration, add an if statement with a condition of remaining <=0. If remaining is less than or equal to 0, use the addClass method to give '.wordcount' a class of 'red'.*/
    /*Finally, add an else statement to the if condition you just created. If the value of remaining is above 0, remove the 'red' class from '.wordcount'.*/
    if(remaining <= 0){
      $('.wordcount').addClass('red')
    }
    else{
      $('.wordcount').removeClass('red')
    }
    $('.characters').html(remaining);
  })
}); 
