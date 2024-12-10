import React, {useState} from "react";
import "./SearchBar.css";
import { useSocket } from '../context/SocketContext.tsx';

const SearchBar: React.FC = () => {

    const socket = useSocket();
    const [searchTerm, setSearchTerm] = useState("");
    
    const handleInputChange = (e) => {
        setSearchTerm(e.target.value);
    };

    const submit_search = (e: React.FormEvent) => {
        e.preventDefault(); // Prevent the default form submission behavior
        socket.emit("submit_search", { searchTerm });
        setSearchTerm(""); // Clear the search bar
    };

    return (
        <form className="search-bar-form" onSubmit={submit_search}>
            <input
                type="text"
                placeholder="Search items..."
                value={searchTerm}
                onChange={handleInputChange}
                className="search-bar"
            />
            <button type="submit" className="search-button">
                Search
            </button>
        </form>
    );
};

export default SearchBar;

