var express = require('express');
var path = require('path');
var mongoose = require('mongoose');
var app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

mongoose.connect('mongodb://localhost/test');
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));


function getHomePage(req, res) {
    res.render('index.jade');
}

app.get('/', getHomePage);

var server = app.listen(3000, function() {
    console.log('Express.js is running...');
});
