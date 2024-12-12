import React, { useState, useEffect, useRef } from "react";
import "./SearchBar.css";
import { useSocket } from "../context/SocketContext.tsx";

const SearchBar: React.FC = () => {
    const socket = useSocket();
    const [searchTerm, setSearchTerm] = useState("");
    const [suggestions, setSuggestions] = useState<string[]>([]);
    const formRef = useRef<HTMLFormElement>(null);

    // Handle input change and emit 'get_suggestions' event
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setSearchTerm(value);

        if (value) {
            socket.emit("get_suggestions", { query: value });
        } else {
            setSuggestions([]);
        }
    };

    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        const relatedTarget = e.relatedTarget as HTMLElement | null;

        // Check if the focus is moving outside the entire form
        if (formRef.current && !formRef.current.contains(relatedTarget)) {
            setSuggestions([]);
        }
    };

    // Handle form submission
    const submitSearch = (e: React.FormEvent) => {
        e.preventDefault();
        console.log("Submitting Search Term:", searchTerm);
        socket.emit("submit_search", { searchTerm });
        setSearchTerm("");
        setSuggestions([]);
    };

    // Handle clicking a suggestion
    const handleSuggestionClick = (suggestion: string) => {
        socket.emit("submit_search", { searchTerm: suggestion });
        setSearchTerm("");
        setSuggestions([]);
    };

    // Listen for suggestions from the server
    useEffect(() => {
        if (!socket) return;

        socket.on("suggestions", (data: string[]) => {
            setSuggestions(data);
        });

        return () => {
            socket.off("suggestions");
        };
    }, [socket]);

    return (
        <form ref={formRef} className="search-bar-form" onSubmit={submitSearch}>
            <input
                type="text"
                placeholder="Search items..."
                value={searchTerm}
                onChange={handleInputChange}
                onBlur={handleBlur}
                className="search-bar"
            />
            <button type="submit" className="search-button">
                Search
            </button>

            {/* Suggestions dropdown */}
            {suggestions.length > 0 && (
                <ul className="suggestions-list">
                    {suggestions.map((suggestion, index) => (
                        <li key={index} className="suggestion-item">
                            <button
                                type="button"
                                className="suggestion-button"
                                onClick={() => handleSuggestionClick(suggestion)}
                            >
                                {suggestion}
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </form>
    );
};

export default SearchBar;

