import React, { useState, useEffect } from "react";
import { useSocket } from '../context/SocketContext.tsx';

interface Item {
    category: string;
    name: string;
    desc?: string;
}

interface Items {
    spells?: Item[];
    monsters?: Item[];
    magicitems?: Item[];
}

const ItemList = () => {
    const socket = useSocket();
    const [items, setItems] = useState([]);
  
    // Listen for item updates from the server
    useEffect(() => {
        if (!socket) return;

        socket.on('item_update', (data: { items: Item[]}) => {
            console.log("Received items!");
            if(data && data.items){
                console.log("Received items:", data.items);
                setItems(prevItems => [...prevItems, ...data.items])
            }
        });
  
        return () => {
            socket.off("item_update");
        };
    }, [socket]);
  
    return (
        <div>
        <h2>D&D Items</h2>
  
        {items.length > 0 ? (
          items.map((item, index) => (
            <div key={index}>
              <strong>{item.name}</strong>
              <p>{item.desc || "No description available."}</p>
            </div>
          ))
        ) : (
          <p>No items available.</p>
        )}
      </div>
    );
  };
  
  export default ItemList;
