import React, { useState, useEffect } from "react";
import { useSocket } from "../context/SocketContext.tsx";
import ItemCard from "./ItemCard.tsx";
import "./ItemFeed.css";

interface Item {
  id: string;
  category: string;
  name: string;
  desc?: string;
  // Spells
  higher_level?: string;
  range?: string;
  duration?: string;
  requires_concentration?: boolean;
  casting_time?: string;
  level?: string;
  // Magic Items
  type?: string;
  rarity?: string;
  requires_attunement?: string;
  // Monsters
  size?: string;
  armor_class?: string,
  // Feats
  benefits?: string[],
  // Races
  traits?: string[],
  // Weapons
  is_melee?: boolean,
  damage_dice?: string,
  is_two_handed?: boolean
  // Armor
  ac_display?: string,
  grants_stealth_disadvantage?: boolean,
  strength_score_required?: number
}

interface ItemFeedProps {
    saveItem: (item: Item) => void;
}

const ItemFeed: React.FC<ItemFeedProps> = ({ saveItem }) => {
    const socket = useSocket();
    const [items, setItems] = useState<Item[]>([]);
    const [expandedItems, setExpandedItems] = useState<{ [key: string]: boolean }>({});

    useEffect(() => {
        if (!socket) return;

        socket.on("item_update", (data: { items: Item[] }) => {
            console.log("Received items:", data.items);
            setItems((prevItems) => [...data.items, ...prevItems]);
        });

        return () => {
            socket.off("item_update");
        };
    }, [socket]);

    const toggleSeeMore = (itemId: string) => {
        setExpandedItems((prev) => ({
            ...prev,
            [itemId]: !prev[itemId],
        }));
    };

    return (
        <div className="items-container">
            {items.length > 0 ? (
                items.map((item) => (
                    <ItemCard
                        key={item.id}
                        item={item}
                        isExpanded={!!expandedItems[item.id]}
                        toggleSeeMore={() => toggleSeeMore(item.id)}
                        onDoubleClick={() => saveItem(item)}
                    />
                ))
            ) : (
                <p>No items available.</p>
            )}
        </div>
    );
};

export default ItemFeed;
