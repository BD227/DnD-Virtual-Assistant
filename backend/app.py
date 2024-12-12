from flask import Flask
from names import query_names, try_create_name_url
from dnd_lookup import query_open5e_for_keywords
from keywords import find_keywords, get_keywords
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
    global transcriber, transcription_running

    if not transcriber:
        transcriber = WhisperTranscriber(model=data.get("model", "base"))
        transcriber.load_model()
        transcriber.start_transcription()

        transcription_running = True  # Set transcription status
        socketio.emit("status", {"message": "Transcription started"})
    else:
        socketio.emit("status", {"message": "Transcription is already running"})


@socketio.on("stop_transcription")
def stop_transcription():
    global transcriber, transcription_running

    if transcriber:
        transcriber.stop_transcription()
        transcriber = None
        transcription_running = False  # Update transcription status
        socketio.emit("status", {"message": "Transcription stopped"})
    else:
        socketio.emit("status", {"message": "No transcription is running"})

@socketio.on('get_suggestions')
def handle_get_suggestions(data):
    query = data.get('query', '').lower()
    matches = []
    max_suggestions = 5  # Define the maximum number of suggestions
    keywords = get_keywords()  # Dictionary with string keys and list values

    # Iterate over the dictionary values (lists of keywords)
    for category in keywords.values():
        for keyword in category:
            # Ensure 'keyword' contains a 'name' key and it matches the query
            if keyword.get("name") and keyword.get("name").lower().startswith(query):
                matches.append(keyword.get("name"))
                print("Matched on " + keyword.get("name"))

                # Check if we have reached the limit of suggestions
                if len(matches) >= max_suggestions:
                    break
        if len(matches) >= max_suggestions:
            break

    # Emit the matches back to the client
    socketio.emit('suggestions', matches)

@socketio.on("submit_search")
def submit_search(text):
    """
    Submit a keyword
    """
    keywords = find_keywords(text.get("searchTerm"))
    print(f"[Keywords]: {keywords}")
    item_list = query_open5e_for_keywords(keywords)
    if item_list:
        print(f"Emitting items: {item_list}")  # Debugging output
        socketio.emit("item_update", {"items": item_list})

@socketio.on("generate_names")
def submit_search(request):
    """
    Submit a keyword
    """
    category = request.get("category")
    print(f"Category Received: {category}")
    url, race, type = try_create_name_url(category)
    print(url)
    data = query_names(url)
    name_list = data.get("names")
    if name_list:
        print(f"Emitting items: {name_list}")  # Debugging output
        socketio.emit("name_update", {"category": "", "names": name_list})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
