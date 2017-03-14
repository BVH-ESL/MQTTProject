function connectWIFI(){
  var wifi = require("Wifi");
  wifi.connect("ESL_Lab1", {password:"wifi@esl"}, function(err){
    console.log("connected? err=", err, "info=", wifi.getIP());
  });
}

function readDHT22(){
  var dhtPin = 4;
  var dhtValue = require("DHT22").connect(dhtPin);
  dhtValue.read(
    function (a) {
      console.log("Temp is "+a.temp.toString()+" and RH is"+a.rh.toString());
    }
  );
}


//connectWIFI();
//require("ESP8266").deepSleep(5000);
var btn=5; // D1
  pinMode(btn, 'input_pullup');

E.on('init', function(){
  console.log(digitalRead(btn));
  if(digitalRead(btn)){
    readDHT22();
  }
  //connectWIFI();
  //readDHT22();
});

save();
