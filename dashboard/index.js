var express = require('express');
var path = require('path');
var mongoose = require('mongoose');
var app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// mongoose.connect('mongodb://localhost/test');
// var db = mongoose.connection;
// db.on('error', console.error.bind(console, 'connection error:'));


function getHomePage(req, res) {
    res.render('index.jade');
}

function getJSON(req, res){
    res.json({
      // "payloadsize" : [2],
      // "msgrate"     : [20000, 22000],
      // "steprate"    : 5000,
              "payloadsize" : [2, 4, 8, 16, 32, 64],
              // "payloadsize" : [16, 32, 64, 128],
              // QoS 0
              // "msgrate"     : [1000, 20000],
              // "steprate"    : 1000,
              // QoS 1
              // "msgrate"     : [1000, 5000],
              // "steprate"    : 250,
              // QoS2
              "msgrate"     : [100, 2000],
              "steprate"    : 100,
              "totalmsg"    : 5000,
              "timeout"     : 30
              });
}

function getUPDTest(req, res){
  res.json(
    {
      "payloadsize" : [2],
      "msgrate"     : [100, 300],
      "steprate"    : 100,
      "totalmsg"    : 5000,
      "timeout"     : 30,
    }
  )
}

app.get('/', getHomePage);
app.get('/jsontest', getJSON);
app.get('/udptest', getUPDTest);

var server = app.listen(3000, function() {
    console.log('Express.js is running...');
});
