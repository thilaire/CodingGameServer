	// function run by Game.html and Player.html
	function updateWebSocket(){
		// when received update about a Game, just display it
		socket.on('update{{ GameName }}', function (msg) {
           var data = JSON.parse(msg);

		   console.log(data);

			// update comments
			if (data.comments) {
				let comments = document.getElementById('comments');
				comments.innerHTML += data.comments + "</br>";
				comments.scrollTop = comments.scrollHeight;
			}
		});
	}

    /* register to endOfGame and display it when received*/
    function displayEndOfGame(){
        socket.on('endOfGame', function(msg){
            document.getElementById('endOfGame').innerHTML = msg;
        });
    }
