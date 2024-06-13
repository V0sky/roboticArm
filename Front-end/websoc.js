var textConnectStat = document.getElementById("conStat");
//const websocket = new WebSocket("ws://192.168.50.97:3000");
const websocket = new WebSocket("ws://192.168.50.98:3000");
var bottleEfSetter = false;

/*Clicking on a button with bottle set autonomous behaviour*/
function setBottleEfTrue(){
    bottleEfSetter = true;
    //apiRequest("http://192.168.50.97:8000/autosetup/start")
    apiRequest("http://192.168.50.98:8000/autosetup/start");
}       

/*Clicking on any other end-effector button cancel autonomous behaviour*/
function setBottleEfFalse(){
    bottleEfSetter = false;
    //apiRequest("http://192.168.50.97:8000/autosetup/cancel")
    apiRequest("http://192.168.50.98:8000/autosetup/cancel");
}

/*Sending data (angles) to the server*/
function sendData(){

    if ((servoAngle[0] >= 0 && servoAngle[0] <= 180)
        && (servoAngle[1] >= 0 && servoAngle[1] <= 180)
        && (servoAngle[2] >= 0 && servoAngle[2] <= 180)
        && (servoAngle[3] >= 0 && servoAngle[3] <= 300)
        && (servoAngle[4] >= 0 && servoAngle[4] <= 180)
        && (servoAngle[5] >= 0 && servoAngle[5] <= 65) 
        && (servoAngle[6] >= 0 && servoAngle[6] <= 80)){

            const anglesValToSend = {
                s1: servoAngle[0],  //BASE
                s2: servoAngle[1],  //SHOULDER
                s3: servoAngle[2],  //ELBOW
                s4: servoAngle[3],  //WRIST
                s5: servoAngle[4],  //ROT WRIST
                s6: servoAngle[5],  //CLAWS W/O ROT
                s7: servoAngle[6],  //CLAWS WITH ROT
                bEfStat: bottleEfSetter
            };

            const jsonToSend = JSON.stringify(anglesValToSend);
            websocket.send(jsonToSend);
    }
}

/*Set angles manualy*/
document.querySelector(".angle_Bt").addEventListener("click", function(){
    sendData();
});

/*Home button - set default position for all servos*/
document.querySelector(".home_Bt").addEventListener("click", function(){
    sendData();
});

/*Bottle end effector (EF) button*/
document.querySelector(".bt_1").addEventListener("click", function(){
    setBottleEfTrue();
    sendData();
});

/*Non rotational EF button*/
document.querySelector(".bt_2").addEventListener("click", function(){
    setBottleEfFalse();
    sendData();
});

/*Rotational EF button*/
document.querySelector(".bt_3").addEventListener("click", function(){
    setBottleEfFalse();
    sendData();
});

websocket.onopen = function (event){
    textConnectStat.value = textConnectStat.value + 
    "Connection has been established.\n"

    sendData();
}

websocket.addEventListener("message", function(event) {
    textConnectStat.value = textConnectStat.value + event.data;
});

websocket.onclose = function (){
    textConnectStat.value = textConnectStat.value + "Connection has been closed.\n"
}

websocket.onerror = function (error){
    textConnectStat.value = textConnectStat.value + "Server has been shut down.\n"
}


