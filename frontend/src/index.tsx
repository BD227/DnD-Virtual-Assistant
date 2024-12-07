import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { SocketProvider } from './context/SocketContext.tsx';

const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(
    <React.StrictMode>
        <SocketProvider>
            <App />
        </SocketProvider>
    </React.StrictMode>
);
