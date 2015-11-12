(function() {
	var IMAGE_HEIGHT = 2780,
	IMAGE_WIDTH = 4380,
	teamA = new Array(11),
	teamB = new Array(11),
	referee,
	ball,
	prevTime,
	canvasHeight = window.innerHeight,
	canvasWidth = canvasHeight * IMAGE_WIDTH / IMAGE_HEIGHT,
	toggleA = true,
	toggleB = true,
	canvas = this.__canvas = new fabric.StaticCanvas('c', {
		renderOnAddRemove: false,
  	selection: false,
  	width: canvasWidth,
  	height: canvasHeight,
	});
	
	canvas.setBackgroundImage('../topProjectionImg/TopView.png', canvas.renderAll.bind(canvas), {
		scaleY: canvasHeight/IMAGE_HEIGHT,
	  scaleX: canvasHeight/IMAGE_HEIGHT,
	});

	loadActors();

	function loadActors () {
		referee = new fabric.Circle({ left: 300, top: 300, radius: 5,fill: 'yellow' });
		ball = new fabric.Circle({ left: 500, top: 500, radius: 3, fill: 'white' });
		canvas.add(referee, ball);
		
		for(var i = 0; i < 11; i++) {
			var teamAPlayer = new fabric.Circle({ originX: 'center', originY: 'center', radius: 15, fill: 'red' });
			var teamBPlayer = new fabric.Circle({ originX: 'center', originY: 'center', radius: 15, fill: 'blue' });			
			
			var text = new fabric.Text(i.toString(), { fontSize: 10, originX: 'center', originY: 'center', fontWeight: 'bold', fill: 'rgb(255,255,255)'  });

			var groupA = new fabric.Group([ teamAPlayer, text ], {
				left: Math.random() * canvasWidth,
				top: Math.random() * canvasHeight
			});

			var groupB = new fabric.Group([ teamBPlayer, text ], {
			  left: Math.random() * canvasWidth,
				top: Math.random() * canvasHeight
			});

			teamA[i] = groupA;
			teamB[i] = groupB;
			
			canvas.add(groupA, groupB);
		}

		prevTime = Date.now();
		animate();
	}

	function animate () {
		var time = Date.now();
		if ( time > prevTime + 500 ) {
			// Animating players from Team A
			for (var i = 0; i < teamA.length ; i++) {
				var player = teamA[i];
				if(toggleA) {
					player.left += 15;
					player.top += 15;
					toggleA = false;
				} else {
					player.left -= 15;
					player.top -= 15;
					toggleA = true;
				}
			}

			// Animating players from Team B
			for (var i = 0; i < teamB.length ; i++) {
				var player = teamB[i];
				if(toggleB) {
					player.left += 15;
					player.top += 15;
					toggleB = false;
				} else {
					player.left -= 15;
					player.top -= 15;
					toggleB = true;
				}
			}
      
      prevTime = time;
    }

    fabric.util.requestAnimFrame(animate, canvas.getElement());
		canvas.renderAll();
	}

})();