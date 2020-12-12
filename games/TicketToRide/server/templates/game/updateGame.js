	var canvas = document.getElementById('game_canvas');
	var ctx = canvas.getContext('2d');
	const colors = ["blue", "red"];
	var players = [{},{}];

	/**
	 * Draw a <color> rectangle centered on <pos>, and rotated <angle> degrees.
	 **/
	function drawRectangle(pos, angle, color) {
		ctx.save();

		ctx.fillStyle = "black";
		ctx.translate(pos[0], pos[1]);
		ctx.rotate(angle * Math.PI / 180);
		ctx.fillRect(-7, -20, 13, 40);
		ctx.fillStyle = color;
		ctx.fillRect(-6, -19, 11 ,38);

		ctx.restore();
	}

	/* function run by Game.html and Player.html */
	function updateWebSocket(){
		/* when received update about a Game, just display it */
		socket.on('update{{ GameName }}', function (msg) {
			var data = JSON.parse(msg);

			// load image and get players names only first time
			if (data.hasOwnProperty('map_name')) {
				let map_bg = new Image();
				map_bg.onload = function () {
					canvas.setAttribute("width", maps[data['map_name']].width);
					canvas.setAttribute("height", maps[data['map_name']].height);
					ctx.drawImage(map_bg, 0, 0, canvas.getAttribute('width'), canvas.getAttribute('height'));
					// draw all rectangles (only for testing)
					/*for (let key in data.coordinates.tracks) {
						if (data.coordinates.tracks.hasOwnProperty(key)) {
							let rect_list = data.coordinates.tracks[key];
							for (let i = 0; i < rect_list.length; i++) {
								let rect = rect_list[i];
								drawRectangle(rect[0], rect[1], "green");
							}
						}
					}*/
					// draw already claimed tracks
                    for (let i = 0; i < data.p1.tracks.length; i++) {
                        for (let j = 0; j < data.p1.tracks[i].length; j++) {
                            let rect = data.p1.tracks[i][j];
                            drawRectangle(rect[0], rect[1], "blue");
                        }
                    }
                    for (let i = 0; i < data.p2.tracks.length; i++) {
                        for (let j = 0; j < data.p2.tracks[i].length; j++) {
                            let rect = data.p2.tracks[i][j];
                            drawRectangle(rect[0], rect[1], "red");
                        }
                    }
				}
				players[0] = data.p1;
				players[1] = data.p2;
				map_bg.src = maps[data['map_name']].data;
			}

			// a player claimed a track, draw it
			if (data.hasOwnProperty('claimed')) {
				console.log("track claimed by player ", data.claimed.player, data.claimed.track)
				players[data.claimed.player].wagons -= data.claimed.track.length;
				for (let i = 0; i < data.claimed.track.length; i++) {
					drawRectangle(data.claimed.track[i][0], data.claimed.track[i][1], colors[data.claimed.player]);
				}
			}
			// update players wagons number
			for(let i=0; i<2; i++){
				document.getElementById('p' + (i+1) + '-info').innerHTML =
				"<B>" + players[i].name + "</B><BR/>" +
				"Score : " + players[i].score + "pts, " +
				"Wagons : " + players[i].wagons + ", " +
				"Cartes : " + players[i].nbCards;
			}

			// update comments
			let comments = document.getElementById('comments');
			comments.innerHTML += data['comments'];
			comments.scrollTop = comments.scrollHeight;
		});
	}
	/* register to endOfGame and display it when received*/
	function displayEndOfGame(){
		socket.on('endOfGame', function(msg){
			document.getElementById('endOfGame').innerHTML = msg;
		});
	}