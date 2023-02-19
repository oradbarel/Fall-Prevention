from fall_prevention_modes import CollectMode, PredMode, Position
from fall_prevention_patient import Patient
from fall_prevention_server import Server
from flask import Flask, render_template, request, flash, redirect, url_for
from turbo_flask import Turbo
from enum import Enum, auto
import threading
import json
import time

app = Flask(__name__, template_folder='fall_prevention_web/html', static_folder='fall_prevention_web')
turbo = Turbo(app)

NUM_CLIENTS = 1
PORT = 13380
IP = "192.168.196.232"
#IP = "192.168.0.100"
ADDR = (IP, PORT)

pred = PredMode()
server = Server(addr=ADDR, num_clients=NUM_CLIENTS, operator=pred)
patient1 = Patient.readPatientsJson("fall_prevention_web/assets/json/patient.json")[0]

last = 0
curr = 0

sex_dict = {}
with open("fall_prevention_web/assets/json/sex.json") as f:
    sex_dict = json.load(f)

doctor_dict = {}
with open("fall_prevention_web/assets/json/doctor.json") as f:
    doctor_dict = json.load(f)

nurse_dict = {}
with open("fall_prevention_web/assets/json/nurse.json") as f:
    nurse_dict = json.load(f)
    
Positions = ["Laying", "Left Side Alarm!", "Right Side Alarm!"]

AlarmPositions = [Position.LEFT_ALARM.value, Position.RIGHT_ALARM.value]

PositionsFiles = ["back", "left_alarm", "right_alarm"]



def isLive(server):
    if abs(server.last_recv - time.time()) > 3:
        return False
    return True


def update_datetime():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('datetime.html'), 'load_datetime'))

@app.context_processor
def get_datetime():
    curr_date = f"{time.strftime(f'%d/%m/%Y', time.gmtime())}"
    curr_time = f"{time.strftime(f'%H:%M:%S', time.gmtime())}"
    return {'curr_time': curr_time, 'curr_date': curr_date, 'live': isLive(server)}

def posToStr(pos):
    if not isPosValid(pos):
        return

    return Positions[pos]

def posToFile(pos):
    if not isPosValid(pos):
        return
    
    return PositionsFiles[pos]

def isPosAlarm(pos):
    return pos in AlarmPositions

def isPosValid(pos):
    return pos <= Position.RIGHT_ALARM.value and pos >= Position.LAYING.value

def update_position():
    global last, curr
    with app.app_context():
        while True:
            if last != curr:
                turbo.push(turbo.replace(render_template('position.html', patient=patient1), 'load_position'))
                last = curr

@app.context_processor
def get_position():
    global last, curr
    pos = pred.last_pred
    curr = pos
    position = posToStr(pos)
    position_image = posToFile(pos)
    position_alarm = ""
    if isPosAlarm(pos):
        position_alarm = "alarm"

    return {'position': position, 'position_image': position_image, 'alarm':position_alarm}

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_datetime).start()
    threading.Thread(target=update_position).start()

@app.route('/edit_patient')
def edit_patient():
    new_vals = {k:v for k,v in request.args.items()}
    try:
        patient1.update(new_vals)
    except (ValueError, TypeError) as e:
        print(f"Handled TypeError: {e}")
        flash(str(e))
    except KeyError as e:
        print(f"Un-handled KeyError: {e}")
    else:
        return redirect(url_for('patient'))

    return render_template('edit_patient.html', patient=patient1,
        sex_dict=sex_dict, doctor_dict=doctor_dict, nurse_dict=nurse_dict)

@app.route('/patient')
def patient():
    return render_template('patient.html', patient=patient1)

@app.route('/')
def home():
    return render_template('home.html', patient=patient1)
 
def startServer():
    server.init()
    server.start()

if __name__ == '__main__':
    threading.Thread(target=startServer).start()

    app.secret_key = 'very secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=56000)