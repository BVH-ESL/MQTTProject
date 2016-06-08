var mqtt   = require('mqtt');
var subscriber = mqtt.connect({host:'192.168.1.198',port:1883});

subscriber.on('connect', function () { // callback on MQTT 'connect'
   console.log('Connected...')
   subscriber.subscribe('/#')
});

var mongoose = require('mongoose');

mongoose.connect('mongodb://localhost/mqtt');
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));

var Schema = mongoose.Schema;
var MessageSchema = new Schema(
  {
    topic: String,
    msg: String
  },
  {
    collection : 'message'
  }
);

var Message = mongoose.model('Devices', MessageSchema);

subscriber.on('message', function (topic, msg, packet) { // callback on MQTT 'message'
   console.log('Message received: "' + msg.toString() + '", topic: ' + topic );
   var newMsg = new Message(
     {
       topic  : topic,
       msg    : msg.toString()
     }
   );
   newMsg.save(function(err){
     if(err) throw err;
     console.log('User saved successfully!');
   });
});

/////////////////////////////////////////////////////////////////////
