from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread
from time import sleep
from random import random
from random import randint
import socket
import json


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000

app = Flask(__name__)
socketio = SocketIO(app)

DATA = [
              { "stock symbol": 'IBM', "price": 700 },
              { "stock symbol": 'MSFT', "price": 40 },
              { "stock symbol": 'AMD', "price": 200 },
              { "stock symbol": 'GOOGL', "price": 1000 }
     ]

def generate_changes():
    while True:
        index = randint(0, 3)
        DATA[index]["price"] = round(random() * 1000, 2)
        socketio.emit('broadcast_change', {'change': str(DATA[index]["price"]), 'index': str(index), 'field_name':'price'})
        sleep(0.3)

@app.route("/grid")
def grid():
  return app.send_static_file('grid.html')

@socketio.on('get_grid')
def handle_source(json_data):
    text = json_data['message'].encode('ascii', 'ignore')
    print text
    socketio.emit('grid', {'grid': json.dumps(DATA)})
    t1 = Thread(target=generate_changes)
    t1.start()

if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT)

