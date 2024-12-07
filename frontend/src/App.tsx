import React from 'react';
import Transcription from './components/Transcription.tsx';
import ItemList from './components/items.tsx';

const App: React.FC = () => {
    return (
        <div>
            <Transcription />
            <ItemList />
        </div>
    );
};

export default App;
