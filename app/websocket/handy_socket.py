from flask_socketio import Namespace, emit

class PiHandyChannel(Namespace):

    def on_connect(self):
        print('Someone connected to the websocket.')

    def on_disconnect(self):
        print('Someone disconnected to the websoket.')

    def on_frame(self, frame):
        emit('frame', frame, broadcast=True)

    def on_result(self, result):
        emit('result', result, broadcast=True)

    def on_reset(self):
        emit('reset', broadcast=True)