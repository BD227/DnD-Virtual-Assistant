import React, { useEffect, useState } from 'react';
import { useSocket } from '../context/SocketContext.tsx';
import './Transcription.css';

const Transcription: React.FC = () => {
    const socket = useSocket();
    const [transcription, setTranscription] = useState<string[]>([]);
    const [isTranscribing, setIsTranscribing] = useState(false);  // New state to track transcription status

    const toggleTranscription = () => {
        if (isTranscribing) {
            // Stop transcription
            socket.emit("stop_transcription");
        } else {
            // Start transcription
            socket.emit("start_transcription", { model: "medium" });
        }
        setIsTranscribing(!isTranscribing);  // Toggle transcription state
    };

    useEffect(() => {
        if (!socket) return;

        // Listen for transcription updates
        socket.on('transcription_update', (data: { transcription: string[] }) => {
            console.log("Received Transcription!");
            if (data && data.transcription) {
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
    }, [transcription]);

    return (
        <div className="live-transcription-container">
            <h2>Live Transcription</h2>
            <div className="live-transcription">
                <div style={{ whiteSpace: 'pre-wrap' }}>
                    <p>{transcription.join(' ')}</p>
                </div>
            </div>

            {/* Single button to toggle transcription */}
            <button onClick={toggleTranscription} className="transcription-button">
                {isTranscribing ? 'Stop Transcription' : 'Start Transcription'}
            </button>
        </div>
    );
};

export default Transcription;
