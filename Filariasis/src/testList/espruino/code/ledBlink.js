var led=2; // D4
var state = false;
var count=0;

pinMode(led, 'output');

var t=setInterval( function() {
  state = !state;
  digitalWrite(led,state);
  console.log( 'state: ' + ((state) ? 'T':'F') 
             + ', count: ' + count++ );
  if (count > 10) {
    clearInterval(t);
    console.log('LED flashing stopped..' );
  }
}, 500);