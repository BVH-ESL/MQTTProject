var wifi = require("Wifi");
wifi.connect("ESL_Lab1", {password:"wifi@esl"}, function(err){
  //console.log("connected? err=", err, "info=", wifi.getIP());
});

var server = "192.168.1.183"; // the ip of your MQTT broker

var options = { // all optional - the defaults are below
  client_id : "random", // the client ID sent to MQTT - it's a good idea to define your own static one based on `getSerial()`
  keep_alive: 60, // keep alive time in seconds
  port: 1883, // port number
  clean_session: true,
};

var mqtt = require("MQTT").create(server, options /*optional*/);

mqtt.on('connected', function() {
  //mqtt.subscribe("test");
});
mqtt.connect();

setInterval(
  function(){
    var topic = "outTopic";
    //var message = "hello, world";
    //mqtt.publish(topic, message);
    var dhtPin = 4;
    var dhtValue = require("DHT22").connect(dhtPin);
    dhtValue.read(
      function (a) {
        mqtt.publish(topic, a.rh.toString()+','+a.temp.toString());
        //console.log("Temp is "+a.temp.toString()+" and RH is"+a.rh.toString());
      }
    );
  }, 5000
);