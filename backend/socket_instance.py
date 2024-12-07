# socket_instance.py

from flask_socketio import SocketIO

# Initialize SocketIO here so it's accessible throughout your project
socketio = SocketIO(cors_allowed_origins="*")  # Allow cross-origin requests for frontend connection
