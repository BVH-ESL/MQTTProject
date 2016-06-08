

var mongoose = require('mongoose');
// mongoose.connect('mongodb://localhost/mqtt');
// mongoose.connection.on('error',function (err) {
//   console.log('Mongoose default connection error: ' + err);
// });
//
// mongoose.connection.on('open', function (err) {
//     // assert.equal(null, err);
//     mongoose.connection.db.listCollections().toArray(function(err, collections) {
//         // assert.equal(null, err);
//         collections.forEach(function(collection) {
//             console.log(collection);
//         });
//         mongoose.connection.db.close();
//         // process.exit(0);
//     })
// });
mongoose.connect('mongodb://localhost/mqtt');
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
// db.once('open', function() {
//   // we're connected!
//   // console.log("eiei");
// });
// var Schema =  mongoose.Schema();
var Schema = mongoose.Schema;
var DeviceSchema = new Schema(
  {
    type: String,
    role: String
  },
  {
    collection : 'device'
  }
);

var Device = mongoose.model('Devices', DeviceSchema);
//
// var rpi = new Device({
//   type: "RPi3#2",
//   role: "PUB"
// });
//
// // rpi.save(function(err) {
// //   if (err) throw err;
// //
// //   console.log('User saved successfully!');
// // });
//
// // Device.find({},function (err, deices) {
// //   if (err) return console.error(err);
// //   console.log(deices);
// // })
//
Device.find({}).exec(function(err, result) {
 if (!err) {
   // handle result
   console.log(result);
 } else {
   // error handling
 };
});
