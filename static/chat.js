        const canvas = document.getElementById('drawing');
        const context = canvas.getContext('2d');
        
        const roomName = JSON.parse(document.getElementById('room-name').textContent);
        var moze_rysowac = false;
        var moze_rysowac_button = document.getElementById("dostep");


        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/kalambury/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {

            const data = JSON.parse(e.data);
            
            if(data.type == "chat_message"){
                document.querySelector('#chat-log').value += (data.message + '\n');
            }else if (data.type == "drawing"){
                
                var drawing_data = data.image;
                var image = new Image();
                image.src =drawing_data
                console.log(image)

                context.drawImage(image,0,0)
                context.save()
            }else if (data.type == "odpowiedz"){
                    if(data.odpowiedz == "TAK"){
                        rysowanie();
                    }

            }else if (data.type == "slowo"){
             console.log(data.slowo);

            }


        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'type':"message",
                'message': message
            }));
            messageInputDom.value = '';
        };


        

        
        let isDrawing = false;
        let lastX = 0;
        let lastY = 0;

        function rysowanie(){

                canvas.addEventListener('mousedown', e => {
                  isDrawing = true;
                  [lastX, lastY] = [e.offsetX, e.offsetY];
                  var drawingData = canvas.toDataURL();
                  chatSocket.send(JSON.stringify({
                        "type": "drawing",
                        "image": drawingData,

                  }));
                });

                canvas.addEventListener('mousemove', e => {
                  if (isDrawing === false) return;

                  context.strokeStyle = 'black';
                  context.lineWidth = 5;
                  context.beginPath();
                  context.moveTo(lastX, lastY);
                  context.lineTo(e.offsetX, e.offsetY);
                  context.stroke();
                  [lastX, lastY] = [e.offsetX, e.offsetY];
                  var drawingData = canvas.toDataURL();
                //   chatSocket.send(drawingData);
                // console.log(drawingData);
                });

                canvas.addEventListener('mouseup', () => isDrawing = false);
                canvas.addEventListener('mouseout', () => isDrawing = false);

       }
        moze_rysowac_button.addEventListener("click", zapytanie);

        function zapytanie(){
            chatSocket.send(JSON.stringify({
                        "type": "zapytanie",

                  }))
        }
        function koniec_rysowania(){
            const events = ["mousedown", "mousemove", "mouseup"]

        }

