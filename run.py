import eventlet
eventlet.monkey_patch()

from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app,debug=True)
    # socketio.run(app, host="0.0.0.0", port=5000, debug=True) # http://127.0.0.1:5000/

