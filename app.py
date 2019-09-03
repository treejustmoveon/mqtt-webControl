from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
import json
import eventlet
import psycopg2
import psycopg2.extras

eventlet.monkey_patch()

app = Flask(__name__)

# app configure for mqtt,socket
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '192.168.1.102'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 600
app.config['MQTT_TLS_ENABLED'] = False

# connect to postgres
conn = psycopg2.connect(database="xiaocheshuju", user="postgres",
                        password="980115", host="192.168.1.102", port="5432")
# create cursor
cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

# initialise
socketio = SocketIO(app)
mqtt = Mqtt(app)


@app.route("/car")
def index():
    return render_template('car.html')


@app.route("/")
def carData():
    cur.execute('''
    select * from carcondition order by log desc limit 20;''')
    cars = cur.fetchall()
    # cars = []
    return render_template('index.html', cars=cars)


@app.route('/data')
def handle():
    return render_template('socket.html')


@socketio.on('my event')
def handle_my_custom_namespace_event(json):
    print('received json: ' + str(json))


@socketio.on('publish')
def handle_publish(json_str):
    data = json_str
    mqtt.publish(data['topic'], data['message'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


@socketio.on('positionQuery')
def handlePositionQuery(message):
    cur.execute(
        ''' select locationx,locationy from carcondition order by log desc limit 5;''')
    data = cur.fetchall()
    # print(data)
    # print(message)
    socketio.emit('returnPosition', data)


@socketio.on('speedQuery')
def handleSpeedQuery(message):
    cur.execute(
        ''' select speed from carspeed order by id desc limit 1;''')
    data = cur.fetchall()
    socketio.emit('returnSpeed', data)


@socketio.on('carsQuery')
def handleCarsQuery(message):
    cur.execute('''
    select * from carcondition order by log desc limit 20;''')
    cars = cur.fetchall()
    socketio.emit('returnCars', cars)


if __name__ == "__main__":
    socketio.run(app, debug=True)
