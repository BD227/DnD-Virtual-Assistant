import React, {useState} from 'react';
import './App.css';
import Transcription from './components/Transcription.tsx';
import ItemFeed from './components/ItemFeed.tsx';
import SearchBar from './components/SearchBar.tsx';
import References from './components/References.tsx';
import NameGenerator from './components/NameGenerator.tsx';

const App: React.FC = () => {

    const [savedItems, setSavedItems] = useState([]);

    const saveItem = (item) => {
      if (!savedItems.some((savedItem) => savedItem.id === item.id)) {
        setSavedItems((prevItems) => [item, ...prevItems]);
      }
    };

    const removeItem = (id) => {
      setSavedItems((prevItems) => prevItems.filter((item) => item.id !== id));
    };

    return (
        <div className="app-layout">
          <div className="left-panel">
            <h1>D&D Virtual Assistant</h1>
            <References savedItems={savedItems} removeItem={removeItem}/>
          </div>
          <div className="middle-panel">
            <SearchBar />
            <ItemFeed saveItem={saveItem}/>
          </div>
          <div className="right-panel">
            <Transcription />
            <NameGenerator />
          </div>
        </div>
    );
};

export default App;
