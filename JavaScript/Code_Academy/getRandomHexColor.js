function getRandomColor(){
    let letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
		
function changeColor(){
    let newColor = getRandomColor();
	// this was taken from a html script tag so the 
	// document.body doesnt work independently.
    //document.body.style.backgroundColor = newColor;
}