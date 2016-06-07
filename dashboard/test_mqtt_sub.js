var mqtt   = require('mqtt');
var client = mqtt.connect({host:'192.168.1.198',port:1883});

client.on('connect', function () { // callback on MQTT 'connect'
   console.log('Connected...')
   client.subscribe('#')
});

client.on('message', function (topic, msg, packet) { // callback on MQTT 'message'
   console.log('Message received: "' + msg.toString() + '", topic: ' + topic )
});

/////////////////////////////////////////////////////////////////////
