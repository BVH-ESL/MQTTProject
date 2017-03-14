//-----------------------------------------------------------------------------
// espruino on ESP8266 (ESP-12E, 4MB Flash)

var led=4; // D2
var btn=5; // D1

var running = true;
var state = false;
var last_seen = 0;

pinMode(btn, 'input_pullup');
pinMode(led, 'output');

setWatch( function(e) {
  var ts = parseInt(e.time);
  console.log( 'button presss@ ' + e.time.toFixed(3) );
  if (ts - last_seen >= 1 ) {
    running = !running;
    last_seen = ts;
    console.log('LED toggle: ' + (running ? 'on':'off'));
  }
}, btn, { repeat: true, edge: "falling" } );

var t=setInterval( function() {
  if (running) {
     state = !state;
     digitalWrite(led,state);
     console.log( 'state: ' + ((state) ? 'T':'F') );
  }
}, 500);
