from flask import Flask, request
from flask import render_template, jsonify
from flask_socketio import SocketIO

from app import uber_reminder

app = Flask(__name__)
socketio = SocketIO(app)

clients = []


@app.route('/')
def main_index():
    index_main = render_template('index.html')
    return index_main


@app.route('/schedule', methods=['POST'])
def schedule_operation():
    print "inside schedule"
    request_dict = request.form.to_dict()
    response = {}
    try:
        for result in uber_reminder.set_uber_reminder(request_dict, socketio):
            response = result
    except Exception as e:
        response.update({"valid": False, "errors": e})
    return jsonify(response)


if __name__ == '__main__':
    socketio.run(app, debug=True)
