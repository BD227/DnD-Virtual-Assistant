import React, { useEffect, useState } from 'react';
import { useSocket } from '../context/SocketContext.tsx';
import './Transcription.css';

const Transcription: React.FC = () => {
    const socket = useSocket();
    const [transcription, setTranscription] = useState<string[]>([]);

    const startTranscription = () => {
        // Emit the 'start_transcription' event to the backend
        socket.emit("start_transcription", { model: "medium" });
      };
    
      const stopTranscription = () => {
        // Emit the 'stop_transcription' event to the backend
        socket.emit("stop_transcription");
      };

    useEffect(() => {
        if (!socket) return;

        // Listen for transcription updates
        socket.on('transcription_update', (data: { transcription: string[]}) => {
            console.log("Received Transcription!");
            if(data && data.transcription){
                setTranscription(data.transcription);
            }
        });

        // Cleanup on unmount
        return () => {
            socket.off('transcription_update');
        };
    }, [socket]);

    useEffect(() => {
        const transcriptionContainer = document.querySelector(".live-transcription");
        if (transcriptionContainer) {
          transcriptionContainer.scrollTop = transcriptionContainer.scrollHeight;
        }
      }, [transcription]); // Runs whenever transcription updates
      

    return (
        <div className="live-transcription-container">
            <h2>Live Transcription</h2>
            <div className="live-transcription">
                <div style={{ whiteSpace: 'pre-wrap' }}>
                    <p>{transcription.join(' ')}</p>
                </div>
            </div>
            <button onClick={startTranscription}>Start Transcription</button>
            <button onClick={stopTranscription}>Stop Transcription</button>
        </div>
    );
};

export default Transcription;
