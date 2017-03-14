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
//require("ESP8266").deepSleep(2000);
var btn=5; // D1
pinMode(btn, 'input_pullup');
var led=2;
pinMode(led, 'output');

var server = "192.168.1.183"; // the ip of your MQTT broker

var options = { // all optional - the defaults are below
  client_id : "random", // the client ID sent to MQTT - it's a good idea to define your own static one based on `getSerial()`
  keep_alive: 60, // keep alive time in seconds
  port: 1883, // port number
  clean_session: true,
};

E.on('init', function(){
  //console.log(digitalRead(btn));
  if(digitalRead(btn)){
    digitalWrite(led, HIGH);
    var wifi = require("Wifi");
    wifi.connect("ESL_Lab1", {password:"wifi@esl"}, function(err){
      if(err === null){
        digitalWrite(led, LOW);
        var mqtt = require("MQTT").create(server, options /*optional*/);
        mqtt.connect();
        mqtt.on('connected', function() {
          digitalWrite(led, HIGH);
          var dhtPin = 4;
          var dhtValue = require("DHT22").connect(dhtPin); 
          dhtValue.read(
            function (a) {
              mqtt.publish("outTopic", a.rh.toFixed(2).toString()+','+a.temp.toFixed(2).toString());
              //console.log("Temp is "+a.temp.toString()+" and RH is"+a.rh.toString());
               digitalWrite(led, LOW);
              setTimeout(function(){ require("ESP8266").deepSleep(2000); }, 3000);
              //require("ESP8266").deepSleep(5000);
            }
          );
        });
      }
    });
  }
  //connectWIFI();
  //readDHT22();
});

save();
