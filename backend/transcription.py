import argparse
import threading
import numpy as np
import speech_recognition as sr
import whisper
import torch
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

from keywords import find_keywords
from socket_instance import socketio

stop_flag = threading.Event()

class WhisperTranscriber:
    def __init__(self, model="medium", non_english=False, energy_threshold=1000, record_timeout=2.0, phrase_timeout=1.0):
        """
        Initialize the transcriber with configurable parameters.
        """
        self.model_name = model
        self.non_english = non_english
        self.energy_threshold = energy_threshold
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.data_queue = Queue()
        self.transcript = ['']
        self.phrase_time = None
        self.audio_model = None
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = energy_threshold
        self.recorder.dynamic_energy_threshold = False
        self.source = None

    def load_model(self):
        """
        Load the Whisper model.
        """
        model = self.model_name
        if model != "large" and not self.non_english:
            model = model + ".en"
        self.audio_model = whisper.load_model(model)

    def start_transcription(self):
        """
        Start the transcription process.
        """
        global stop_flag
        if not self.audio_model:
            self.load_model()
        if not self.source:
            self.source = sr.Microphone(sample_rate=16000)

        # Adjust for ambient noise
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)

        def record_callback(_, audio: sr.AudioData) -> None:
            """
            Threaded callback function to receive audio data.
            """
            data = audio.get_raw_data()
            self.data_queue.put(data)

        # Start recording in a background thread
        self.recorder.listen_in_background(self.source, record_callback, phrase_time_limit=self.record_timeout)
        print("Recording started. Press Ctrl+C to stop.")

        try:
            stop_flag.clear()
            thread = threading.Thread(target=self._process_queue)
            thread.daemon = True
            thread.start()
        except KeyboardInterrupt:
            stop_flag.set()
            print("\nRecording stopped.")
        return self.get_transcription()

    def _process_queue(self):
        """
        Process audio chunks from the queue and transcribe them.
        """
        while not stop_flag.is_set():
            try:
                now = datetime.utcnow()
                if not self.data_queue.empty():
                    phrase_complete = False
                    if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                        phrase_complete = True

                    self.phrase_time = now
                    audio_data = b''.join(self.data_queue.queue)
                    self.data_queue.queue.clear()
                    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                    result = self.audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                    text = result['text'].strip()
                    if not text:
                        continue
                    print(f"[Transcribed Text]: {text}")
                    keywords = find_keywords(text)
                    print(f"[Keywords]: {keywords}")

                    if phrase_complete:
                        self.transcript.append(text)
                        self.send_transcript()
                    else:
                        self.transcript[-1] = text
                else:
                    sleep(0.25)
            except Exception as e:
                print(f"[Error in _process_queue]: {e}")

    def send_transcript(self):
        """
        Continuously process the transcription queue and emit updates via WebSocket.
        """
        try:
            if self.transcript:
                #print(f"Sending to frontend: {self.transcript}")  # Debug log
                socketio.emit("transcription_update", {"transcription": self.transcript})  # Send updates to the frontend
        except Exception as e:
            print(f"[Error in send_transcriptions]: {e}")

    def get_transcription(self):
        """
        Get the complete transcription as a list of strings.
        """
        return self.transcript
    
    def stop_transcription():
        stop_flag.set()


if __name__ == "__main__":
    # Command-line usage for standalone testing
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="medium", choices=["tiny", "base", "small", "medium", "large"], help="Whisper model size")
    parser.add_argument("--non_english", action='store_true', help="Use multilingual model.")
    parser.add_argument("--energy_threshold", default=1000, type=int, help="Energy level for mic to detect.")
    parser.add_argument("--record_timeout", default=2.0, type=float, help="Real-time recording timeout.")
    parser.add_argument("--phrase_timeout", default=3.0, type=float, help="Silence timeout to consider a phrase complete.")
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse', help="Default microphone name. Use 'list' to view available devices.")
    args = parser.parse_args()

    transcriber = WhisperTranscriber(
        model=args.model,
        non_english=args.non_english,
        energy_threshold=args.energy_threshold,
        record_timeout=args.record_timeout,
        phrase_timeout=args.phrase_timeout,
    )
    transcriber.start_transcription()
