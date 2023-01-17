        const canvas = document.getElementById('drawing');
        const context = canvas.getContext('2d');

        const roomName = JSON.parse(document.getElementById('room-name').textContent);
        const username = JSON.parse(document.getElementById('username').textContent);
        var moze_rysowac = false;
        var moze_rysowac_button = document.getElementById("dostep");


        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/kalambury/'
            + roomName
            + '/'
        );
        chatSocket.onopen = function() {
            chatSocket.send(JSON.stringify({
                'type':"hello",
                'username': username,
            }));
        };
        chatSocket.onmessage = function(e) {

            const data = JSON.parse(e.data);
            
            if(data.type == "chat_message"){
                document.querySelector('#chat-log').value += (data.message + '\n');
            }else if (data.type == "drawing"){
                
                var drawing_data = data.image;
                var image = new Image();
                image.src =drawing_data
//                console.log(image)

                    image.onload = function(){
                canvas.width = image.width;
                canvas.height = image.height;
                context.drawImage(image,0,0);
            }
                context.save()
            }else if (data.type == "odpowiedz"){
                    if(data.odpowiedz == "TAK"){
                        rysowanie();
                    }

            }else if (data.type == "slowo"){
             console.log(data.slowo);
             alert("Twoje słowo to: " +  data.slowo);

            }else if (data.type == "koniec"){
                koniec_rysowania();
                alert("Wygrywa gracz " + data.username)
                context.clearRect(0, 0, canvas.width, canvas.height);

            }else if (data.type == "hello"){

                document.querySelector('#chat-log').value += ("dołącza do nas " + data.username + '\n');
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
                'message': message,
                'username': username,
            }));
            messageInputDom.value = '';
        };


        

        
        let isDrawing = false;
        let lastX = 0;
        let lastY = 0;

        function rysowanie(){

                canvas.addEventListener('mousedown', ruch_2);

                canvas.addEventListener('mousemove', ruch_1);

                canvas.addEventListener('mouseup', ruch_3);
                canvas.addEventListener('mouseout', ruch_3);

       }
        moze_rysowac_button.addEventListener("click", zapytanie);

        function zapytanie(){
            chatSocket.send(JSON.stringify({
                        "type": "zapytanie",

                  }))
        }

        function ruch_1(e){
                  if (isDrawing === false) return;

                  context.strokeStyle = 'black';
                  context.lineWidth = 5;
                  context.beginPath();
                  context.moveTo(lastX, lastY);
                  context.lineTo(e.offsetX, e.offsetY);
                  context.stroke();
                  [lastX, lastY] = [e.offsetX, e.offsetY];
                  var drawingData = canvas.toDataURL();


              chatSocket.send(JSON.stringify({
                        "type": "drawing",
                        "image": drawingData,

                  }));


                }

        function ruch_2(e){
                  isDrawing = true;
                  [lastX, lastY] = [e.offsetX, e.offsetY];
                  var drawingData = canvas.toDataURL();
                  chatSocket.send(JSON.stringify({
                        "type": "drawing",
                        "image": drawingData,

                  }));
                }
        function ruch_3(){
            isDrawing = false;
            var drawingData = canvas.toDataURL();
                //   chatSocket.send(drawingData);
                // console.log(drawingData);

                chatSocket.send(JSON.stringify({
                        "type": "drawing",
                        "image": drawingData,

                  }));
        }

        function koniec_rysowania(){
        try{
            canvas.removeEventListener('mousedown', ruch_2);

                canvas.removeEventListener('mousemove', ruch_1);

                canvas.removeEventListener('mouseup', ruch_3);
                canvas.removeEventListener('mouseout', ruch_3);
            }catch (e){

            }


        }
