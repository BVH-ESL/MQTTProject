

function readDHT22(){
  var dhtPin = 5;
  var dhtValue = require("DHT22").connect(dhtPin);
  dhtValue.read(
    function (a) {
      console.log("Temp is "+a.temp.toString()+" and RH is "+a.rh.toString());
    }
  );
}

setInterval( readDHT22, 1000 );
