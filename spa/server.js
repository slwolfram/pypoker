var express = require('express');
var app = express();
app.use(express.static('.'));
app.get('/', function (req, res,next) {
 res.redirect('/'); 
});
app.listen(8080, 'localhost');
console.log('WolfPoker-frontend server is listening on port 8080');