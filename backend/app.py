from time import sleep
from flask import Flask
from flask_socketio import SocketIO, emit
from transcription import WhisperTranscriber  # Import your transcriber class
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow cross-origin requests for frontend connection
transcriber = None  # To hold the transcriber instance

stop_flag = threading.Event()


@app.route("/")
def index():
    return "Real-time Transcription Service Running"


def send_transcriptions(transcriber):
    """
    Continuously process the transcription queue and emit updates via WebSocket.
    """
    while True:
        try:
            transcription = transcriber.get_transcription()
            if transcription:
                print(f"Sending to frontend: {transcription}")  # Debug log
                socketio.emit("transcription_update", {"transcription": transcription})  # Send updates to the frontend
        except Exception as e:
            print(f"[Error in send_transcriptions]: {e}")
        sleep(0.5)


@socketio.on("start_transcription")
def start_transcription(data):
    """
    Start the transcription process when the frontend sends a 'start_transcription' event.
    """
    global transcriber
    if not transcriber:
        transcriber = WhisperTranscriber(model=data.get("model", "medium"))
        transcriber.load_model()
        transcriber.start_transcription()
        # Run the transcription process in a separate thread to keep Flask responsive
        stop_flag.clear()
        thread = threading.Thread(target=send_transcriptions, args=(transcriber,))
        thread.daemon = True
        thread.start()
        emit("status", {"message": "Transcription started"})
    else:
        emit("status", {"message": "Transcription is already running"})


@socketio.on("stop_transcription")
def stop_transcription():
    """
    Stop the transcription process when the frontend sends a 'stop_transcription' event.
    """
    global transcriber
    if transcriber:
        stop_flag.set()
        transcriber = None
        emit("status", {"message": "Transcription stopped"})
    else:
        emit("status", {"message": "No transcription is running"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
