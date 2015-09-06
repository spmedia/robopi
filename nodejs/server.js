var express = require('express'),
	app = express(),
	http = require('http').createServer(app).listen(61337),
	io = require('socket.io')(http),
	sys = require('util'),
	exec = require('child_process').exec,
	fs = require('fs');

app.use('/assets', express.static('../public_html/assets'));

function puts(error, stdout, stderr) { }

app.get("/", function(req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
		fs.readFile('../public_html/index.html', 'utf8', function (err,data) {
			res.end(data);
		});
});

app.get("/favicon.ico", function(req, res) {
    res.writeHead(200, {'Content-Type': 'image/x-icon'});
		fs.readFile("../public_html/assets/images/favicon.ico", function (err,data) {
			res.end(data);
		});
});

app.get("/update", function(req, res) {
	exec("sh /home/pi/robopi/update.sh &", puts);

  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('1');
});

app.get("/dpad", function(req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
		fs.readFile('../public_html/dpad.html', 'utf8', function (err,data) {
			res.end(data);
		});
});

app.get("/display", function(req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
		fs.readFile('../public_html/display.html', 'utf8', function (err,data) {
			res.end(data);
		});
});

io.sockets.on('connection', function (socket) {

});
