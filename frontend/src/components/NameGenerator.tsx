import React, { useState, useEffect } from 'react';
import './NameGenerator.css';
import { useSocket } from '../context/SocketContext.tsx';

// Example categories
const categories = [
    'Dragonborn, Male', 'Dragonborn, Female', 'Dragonborn, Family', 'Dragonborn, Region', 
    'Dragonborn, Town', 'Dwarf, Male', 'Dwarf, Female', 
    'Dwarf, Family', 'Dwarf, Region', 'Dwarf, Town', 'Elf, Male', 
    'Elf, Female', 'Elf, Family', 'Elf, Region', 'Elf, Town', 
    'Gnome, Male', 'Gnome, Female', 'Gnome, Family', 'Gnome, Region', 'Gnome, Town', 
    'Goblin, Male', 'Goblin, Female', 'Goblin, Family', 
    'Goblin, Region', 'Goblin, Town', 'Halfling, Male', 
    'Halfling, Female', 'Halfling, Family', 'Halfling, Region', 'Halfling, Town', 
    'Human, Male', 'Human, Female', 'Human, Family', 
    'Human, Region', 'Human, Town', 'Orc, Male', 'Orc, Female', 
    'Orc, Family', 'Orc, Region', 'Orc, Town', 'Tavern', 'Tiefling, Male', 
    'Tiefling, Female', 'Tiefling, Family', 'Tiefling, Region', 'Tiefling, Town', 
    'Troll, Male', 'Troll, Female', 'Troll, Family', 
    'Troll, Region', 'Troll, Town'
   ]

const NameGenerator: React.FC = () => {
    const socket = useSocket();
    const [selectedCategory, setSelectedCategory] = useState('Tavern');
    const [names, setNames] = useState<string[]>([]);

    const fetchNames = async (category: string) => {
        if (!socket) return
        socket.emit("generate_names", { category });
    };

    useEffect(() => {
        if (!socket) return;

        fetchNames(selectedCategory);

        socket.on("name_update", (data: { category: string, names: string[] }) => {
            console.log("Received items:", data.names);
            console.log("Received category: ", data.category)
            setNames(data.names);
            if(data.category){
                categories.forEach(element => {
                    if(element.toLowerCase() == data.category.toLowerCase()){
                        setSelectedCategory(element)
                    }
                });
            }
        });

        return () => {
            socket.off("item_update");
        };
    }, [socket]);

    useEffect(() => {
        fetchNames(selectedCategory)
    }, [selectedCategory]);

    return (
        <div className="name-generator">
            <div className="category-selector-container">
                <select
                id="category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="category-selector"
                >
                {categories.map((category) => (
                    <option key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                    </option>
                ))}
                </select>
            </div>

            {/* Grid container for displaying names */}
            <div className="name-grid">
                {names.map((name, index) => (
                <div key={index} className="name-card">
                    {name}
                </div>
                ))}
            </div>
            <button className="generate-button" onClick={() => fetchNames(selectedCategory)}>
                Generate Names
            </button>
        </div>
    );
    };

export default NameGenerator;
