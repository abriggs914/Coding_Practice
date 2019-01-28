var typeQuiz = {
    types: [],
    addType: function(typeName, strongAtk, weakAtk, nodmgAtk) {
        this.types.push({
            typeName: typeName,
            strongAtk: strongAtk,
            weakAtk: weakAtk,
            nodmgAtk: nodmgAtk,
        });
    },
    checkGuesses: function(guessArray, randomTypeObj, questionNumber){
        var numberCorrect = 0;
        var numOfAnswers = 0;
        switch (questionNumber) {
            case 0:
                numOfAnswers = randomTypeObj.strongAtk.length;
                for(i=0; i<guessArray.length; i++) {
                    for(j=0; j<numOfAnswers; j++) {
                        if(randomTypeObj.strongAtk[j] == guessArray[i]) {
                            numberCorrect++;
                        }
                    }
                }
                break;
            case 1:
                numOfAnswers = randomTypeObj.weakAtk.length;
                for(i=0; i<guessArray.length; i++) {
                    for(j=0; j<numOfAnswers; j++) {
                        if(randomTypeObj.weakAtk[j] == guessArray[i]) {
                            numberCorrect++;
                        }
                    }
                }
                break;
            default:
                numOfAnswers = randomTypeObj.nodmgAtk.length;
                for(i=0; i<guessArray.length; i++) {
                    for(j=0; j<numOfAnswers; j++) {
                        if(randomTypeObj.nodmgAtk[j] == guessArray[i]) {
                            numberCorrect++;
                        }
                    }
                }
                break;
        }
        alert("You got " + numberCorrect + " correct!");
        typeQuiz.calculateScore(numberCorrect, numOfAnswers);
        if(typeQuiz.turnNumber < 10) {
            typeQuiz.getQuestion();
            typeQuiz.turnNumber +=1;
        }
        handlers.updateTurnAndScore();

    },
    getQuestion: function() {
        var randomType = Math.floor(Math.random() * (18));
        typeQuiz.randomTypeObj = this.types[randomType];
        typeQuiz.questionNumber = Math.floor(Math.random() * (3));
        handlers.displayQuestion();
        handlers.nextQuestion();
    },
    calculateScore: function(numberCorrect, numOfAnswers) {
        typeQuiz.score += Math.floor((numberCorrect/numOfAnswers) * 100);
    },
    questionNumber: 0,
    randomTypeObj: {},
    turnNumber: 1,
    score: 0
}

var handlers = {
    displayQuestion: function() {
        var questionNumber = typeQuiz.questionNumber;
        var randomTypeObj = typeQuiz.randomTypeObj;
        switch (questionNumber) {
            case 0:
                var question = "What is " + randomTypeObj.typeName + " super effective against?";
                var totalAnswers = randomTypeObj.strongAtk.length;
                break;
            case 1:
                var question = "What is " + randomTypeObj.typeName + " not very effective against?";
                var totalAnswers = randomTypeObj.weakAtk.length;
                break;
            default:
                var question = "What is " + randomTypeObj.typeName + " not effective at all against?";
                var totalAnswers = randomTypeObj.nodmgAtk.length;
                break;
        }

        view.displayQuestion(question, totalAnswers);
    },
    checkGuesses: function(guesses) {
        typeQuiz.checkGuesses(guesses, typeQuiz.randomTypeObj, typeQuiz.questionNumber);
    },
    nextQuestion: function() {
        view.uncheckAllBtns();
        view.numberOfCheckedTypes = 0;
        view.updateNumerator();
    },
    updateTurnAndScore: function() {
        var turnNumber = typeQuiz.turnNumber;
        var score = typeQuiz.score;
        view.updateTurnAndScore(turnNumber, score);
    }
}

var view = {
    setUpEventListeners: function() {
        document.querySelector(".btn-wrap").addEventListener("click", function(event){
            var elementClicked = event.target;
            if(elementClicked.type == "checkbox"){
                view.checkTotalChecked(elementClicked);
                view.updateNumerator();
            }

        });
    },
    uncheckAllBtns: function() {
        var w = document.getElementsByTagName("input");
        for(var i=0; i < w.length; i++) {
            if(w[i].type == "checkbox") {
                w[i].checked = false;
            }
        }
    },
    submitPop: function() {
        var submitBtn = document.getElementById("btn-submit");
        submitBtn.addEventListener("mousedown", function() {
            submitBtn.style.boxShadow = "none";
        });
        submitBtn.addEventListener("mouseup", function() {
            submitBtn.style.boxShadow = "0px 2px 2px #333";
        });
        submitBtn.addEventListener("click", function() {
            view.readInputs();
        })
    },
    displayQuestion: function(question, totalAnswers) {
        var questionElement = document.getElementById("question");
        questionElement.innerHTML = question;

        var numOfAnswersElement = document.querySelector(".denominator");
        numOfAnswersElement.innerHTML = totalAnswers;
        view.totalAnswers = totalAnswers;
    },
    readInputs: function() {
        var x = document.getElementsByTagName("input");

        var guesses = [];
        for(var i=0; i<x.length; i++) {
            if(x[i].checked == true) {
                guesses.push(x[i].id);
            }
        }
        handlers.checkGuesses(guesses);
    },
    updateNumerator: function() {
        var numerator = document.querySelector(".numerator");
        var types = document.getElementsByTagName("input");
        view.numberOfCheckedTypes = 0;
        for(var i=0; i<types.length; i++) {
            if(types[i].checked == true) {
                view.numberOfCheckedTypes++;
            }
        }
        view.checkTotalChecked
        numerator.innerHTML = view.numberOfCheckedTypes;
    },
    checkTotalChecked: function(elementClicked) {
         if(view.numberOfCheckedTypes == view.totalAnswers) {
            elementClicked.checked = false;
        } else {
            view.updateNumerator();
        }
    },
    updateTurnAndScore: function(turnNumber, score){
        var turnElement = document.querySelector(".turnNumber");
        var scoreElement = document.querySelector(".score");
        turnElement.innerHTML = turnNumber;
        scoreElement.innerHTML = score;
    },
    numberOfCheckedTypes: 0,
    totalAnswers: 0
}

//name, strongAtk, weakAtk, nodmgAtk
typeQuiz.addType("normal", ["nothing"], ["rock", "steel"], ["nothing"], ["ghost"]);
typeQuiz.addType("fire", ["grass", "ice", "bug", "steel"], ["fire", "water", "rock", "dragon"], ["nothing"]);
typeQuiz.addType("water", ["fire", "ground", "rock"], ["water", "grass", "dragon"], ["nothing"]);
typeQuiz.addType("electric", ["water", "flying"], ["electric", "grass", "dragon"], ["ground"]);
typeQuiz.addType("grass", ["water", "ground", "rock"], ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"], ["nothing"]);
typeQuiz.addType("ice", ["grass", "ground", "flying", "dragon"], ["fire", "water", "ice", "steel"], ["nothing"]);
typeQuiz.addType("fighting", ["normal", "ice", "rock", "dark", "steel"], ["poison", "flying", "psychic", "bug", "fairy"], ["ghost"]);
typeQuiz.addType("posion", ["grass", "fairy"], ["poison", "ground", "rock", "ghost"], ["steel"]);
typeQuiz.addType("ground", ["fire", "electric", "poison", "rock", "steel"], ["grass", "bug"], ["flying"]);
typeQuiz.addType("flying", ["grass", "fighting", "bug"], ["electric", "rock", "steel"], ["nothing"]);
typeQuiz.addType("psychic", ["fighting", "poison"], ["psychic", "steel"], ["dark"]);
typeQuiz.addType("bug", ["grass", "psychic", "dark"], ["fire", "fighting", "poison", "flying", "ghost", "steel", "fairy"], ["nothing"]);
typeQuiz.addType("rock", ["fire", "ice", "flying", "bug"], ["fighting", "ground", "steel"], ["nothing"]);
typeQuiz.addType("ghost", ["psychic", "ghost"], ["dark"], ["normal"]);
typeQuiz.addType("dragon", ["dragon"], ["steel"], ["fairy"]);
typeQuiz.addType("dark", ["psychic", "ghost"], ["fighting", "dark", "fairy"], ["nothing"]);
typeQuiz.addType("steel", ["ice", "rock", "fairy"], ["fire", "water", "electric", "steel"], ["nothing"]);
typeQuiz.addType("fairy", ["fighting", "dragon", "dark"], ["fire", "poison", "steel"], ["nothing"]);
//to compare against 'empty' arrays
typeQuiz.addType("nothing", ["nothing"], ["nothing"], ["nothing"]);


typeQuiz.getQuestion();
view.uncheckAllBtns();
view.submitPop();
view.setUpEventListeners();
