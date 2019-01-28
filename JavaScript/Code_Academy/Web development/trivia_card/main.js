$(document).ready(() =>{
  /*
Let's start with the hint box. Select the hint box by its class, 'hint-box', and create an event handler for it on 'click'. Because we are selecting the element by its class, remember to use . when selecting it. Leave the callback function empty for now.*/
	$('.hint-box').on('click', () => {
    /*When the hint box is clicked on, we want the HTML element containing the hint to slide into view.

Inside the event handler's callback function, select the element with the class 'hint'. Call the .slideToggle() method on it. You can choose a parameter to determine how quickly it slides. We recommend something between 300 and 1000.

Save your code and click on the hint box to test it!*/
    $('.hint').slideToggle(300);
  });
  
  	/*Next, let's work on animating the wrong answers. When the user clicks on a wrong answer, we want the text of the wrong answer to fade out. There are three wrong answers, so we will want to create three different on 'click' event handlers. Each wrong answer has a different class. They are wrong-answer-one,wrong-answer-two, and wrong-answer-three. Leave all three callback functions empty for now.*/
  /*
Inside each event handler, target the corresponding wrong answer text by its class. The classes are 'wrong-text-one', 'wrong-text-two' , and 'wrong-text-three'. Call the .fadeOut() method on the correct text in each event handler.

Again, you can choose a parameter to determine how quickly it will disappear. You can experiment with 'slow', 'fast', or any number you choose.

Save your code and try clicking on all three.*/
		$('.wrong-answer-one').on('click', () => {
      $('.wrong-text-one').fadeOut('slow');
      $('.smiley').hide();
      $('.frown').show();
    });
  
		$('.wrong-answer-two').on('click', () => {
      $('.wrong-text-two').fadeOut();
      $('.smiley').hide();
      $('.frown').show();
    });
  
		$('.wrong-answer-three').on('click', () => {
      $('.wrong-text-three').fadeOut('fast');
      $('.smiley').hide();
      $('.frown').show();
    });
  
  	$('.correct-answer').on('click', () => {
      $('.frown').hide();
      $('.wrong-text-one').fadeOut('fast');
      $('.wrong-text-two').fadeOut('fast');
      $('.wrong-text-three').fadeOut('fast');
      $('.smiley').show();
    });
});
