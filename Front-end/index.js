let slidersAll = document.getElementById("sliders_all");
let subSlider1 = document.getElementById("subSlider1");
let cloneDiv = subSlider1.cloneNode(true);

//let textBoxes = document.getElementById("textBoxes");
let slideTextDiv5 = document.getElementById("slideText5");
let slideTextDiv6 = document.getElementById("slideText6");
let slideTextDiv7 = document.getElementById("slideText7");
let manualJointText = document.getElementById("manualJointText");
//let setBtn = document.getElementById("angleButton");
let pageBlock2 = document.getElementById("pageBlock2");

var slider1 = document.getElementById("myRange1");
var textBox1 = document.getElementById("slideText1");

var slider2 = document.getElementById("myRange2");
var textBox2 = document.getElementById("slideText2");

var slider3 = document.getElementById("myRange3");
var textBox3 = document.getElementById("slideText3");

var slider4 = document.getElementById("myRange4");
var textBox4 = document.getElementById("slideText4");

var slider5 = document.getElementById("myRange5");
var slider5Container = document.getElementById("slider5");
var textBox5 = document.getElementById("slideText5");

var slider6 = document.getElementById("myRange6");
var slider6Container = document.getElementById("slider6");
var textBox6 = document.getElementById("slideText6");

var slider7 = document.getElementById("myRange7");
var slider7Container = document.getElementById("slider7");
var textBox7 = document.getElementById("slideText7");

var degBaseValue = document.getElementById("baseValue");
var degShoulderValue = document.getElementById("shoulderValue");
var degElbowValue = document.getElementById("elbowValue");
var degWristValue = document.getElementById("wristValue");
var degRotValue = document.getElementById("rotValue");
var degClawValue = document.getElementById("clawValue");
var degClawValue2 = document.getElementById("clawValue2");

/*Bottle End-Effector changes front-end*/
function hideAllSliders(){

    slidersAll.style.visibility = "hidden";
    slidersAll.replaceWith(cloneDiv);
    cloneDiv.style.display = "block";
    manualJointText.style.visibility = "hidden";
    pageBlock2.style.display = "none";

    /*
    textBoxes.style.visibility = "hidden";
    setBtn.style.visibility = "hidden";
    */

}

/*Non-rotational End-effector*/
function changeSliders(){

    cloneDiv.replaceWith(slidersAll);
    slidersAll.style.visibility = "visible";
    cloneDiv.style.display = "none";
    slider5.disabled = true;
    slider5Container.style.opacity = 0.2;
    slideTextDiv5.disabled = true;
    slideTextDiv5.style.opacity = 0.2;
    slider7.disabled = true;
    slider7Container.style.opacity = 0.2;
    slideTextDiv7.disabled = true;
    slideTextDiv7.style.opacity = 0.2;

    manualJointText.style.visibility = "visible"
    pageBlock2.style.display = "block";

    /*
    textBoxes.style.visibility = "visible";
    setBtn.style.visibility = "visible";
    */
}

/*Rotational End-effector*/
function showAllSliders(){

    cloneDiv.style.display = "none";
    cloneDiv.replaceWith(slidersAll);
    slidersAll.style.visibility = "visible";
    slider5.disabled = false;
    slider5Container.style.opacity = 1;
    slideTextDiv5.disabled = false;
    slideTextDiv5.style.opacity = 1;
    slider7.disabled = false;
    slider7Container.style.opacity = 1;
    slideTextDiv7.disabled = false;
    slideTextDiv7.style.opacity = 1;
    manualJointText.style.visibility = "visible";
    pageBlock2.style.display = "block";

    /*
    textBoxes.style.visibility = "visible";
    setBtn.style.visibility = "visible";
    */
}

/*Servo default angles' values*/
var servoAngle = [115, 0, 180, 130, 140, 0, 0];

function setSliderAndTextBox(slider, textBox, jointValue, index){
    servoAngle[index] = parseInt(slider.value);
    textBox.value = servoAngle[index];
    jointValue.textContent = servoAngle[index];
    sendData();
}

slider1.onchange = function(){
    setSliderAndTextBox(slider1, textBox1, degBaseValue, 0);
};

slider2.onchange = function(){
    setSliderAndTextBox(slider2, textBox2, degShoulderValue, 1);
};

slider3.onchange = function(){
    setSliderAndTextBox(slider3, textBox3, degElbowValue, 2);
};

slider4.onchange = function(){
    setSliderAndTextBox(slider4, textBox4, degWristValue, 3);
};

slider5.onchange = function(){
    setSliderAndTextBox(slider5, textBox5, degRotValue, 4);
};

slider6.onchange = function(){
    setSliderAndTextBox(slider6, textBox6, degClawValue, 5);
};

slider7.onchange = function(){
    setSliderAndTextBox(slider7, textBox7, degClawValue2, 6);
};

function setValuesByButton(slider, textBox, jointValue, 
                            condition1, condition2, index){
    servoAngle[index] = Math.round(textBox.value);      
    if (servoAngle[index] >= condition1 && servoAngle[index] <= condition2){
        slider.value = servoAngle[index];
        jointValue.textContent = servoAngle[index];
    }
    else{
        alert("Wrong value inserted. " 
        + "Please insert appropriate angle values.");
    }
}

function setAnglesManualy(){
    setValuesByButton(slider1, textBox1, degBaseValue, 0, 180, 0);
    setValuesByButton(slider2, textBox2, degShoulderValue, 0, 180, 1);
    setValuesByButton(slider3, textBox3, degElbowValue, 0, 180, 2);
    setValuesByButton(slider4, textBox4, degWristValue, 0, 300, 3);
    setValuesByButton(slider5, textBox5, degRotValue, 0, 180, 4);
    setValuesByButton(slider6, textBox6, degClawValue, 0, 65, 5);
    setValuesByButton(slider7, textBox7, degClawValue2, 0, 80, 6);
}

function setDefAngleValue(slider, textBox, jointValue, index, defaultValue){
    slider.value = defaultValue;
    textBox.value = defaultValue;
    jointValue.textContent = defaultValue;
    servoAngle[index] = defaultValue;
}

function homePos(){
    setDefAngleValue(slider1, textBox1, degBaseValue, 0, 115);
    setDefAngleValue(slider2, textBox2, degShoulderValue, 1, 0);
    setDefAngleValue(slider3, textBox3, degElbowValue, 2, 180);
    setDefAngleValue(slider4, textBox4, degWristValue, 3, 130);
    setDefAngleValue(slider5, textBox5, degRotValue, 4, 140);
    setDefAngleValue(slider6, textBox6, degClawValue, 5, 0);
    setDefAngleValue(slider7, textBox7, degClawValue2, 6, 0);
}
