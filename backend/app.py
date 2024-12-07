from flask import Flask
from socket_instance import socketio
from transcription import WhisperTranscriber  # Import your transcriber class
import threading

app = Flask(__name__)
socketio.init_app(app)
transcriber = None  # To hold the transcriber instance

stop_flag = threading.Event()


@app.route("/")
def index():
    return "Real-time Transcription Service Running"

@socketio.on("start_transcription")
def start_transcription(data):
    """
    Start the transcription process when the frontend sends a 'start_transcription' event.
    """
    global transcriber
    if not transcriber:
        transcriber = WhisperTranscriber(model=data.get("model", "base"))
        transcriber.load_model()
        transcriber.start_transcription()
        # Run the transcription process in a separate thread to keep Flask responsive
        socketio.emit("status", {"message": "Transcription started"})
    else:
        socketio.emit("status", {"message": "Transcription is already running"})


@socketio.on("stop_transcription")
def stop_transcription():
    """
    Stop the transcription process when the frontend sends a 'stop_transcription' event.
    """
    global transcriber
    if transcriber:
        transcriber.stop_transcription()
        transcriber = None
        socketio.emit("status", {"message": "Transcription stopped"})
    else:
        socketio.emit("status", {"message": "No transcription is running"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
