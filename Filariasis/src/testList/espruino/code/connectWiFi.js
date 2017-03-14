var wifi = require("Wifi");
wifi.connect("ESL_Lab1", {password:"wifi@esl"}, function(err){
  console.log("connected? err=", err, "info=", wifi.getIP());
});