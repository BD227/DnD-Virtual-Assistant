import React, {useState} from "react";
import ItemCard from "./ItemCard.tsx";
import "./References.css";

interface Item {
    id: string;
    category: string;
    name: string;
    desc?: string;
    higher_level?: string;
    range?: string;
    duration?: string;
    requires_concentration?: boolean;
    casting_time?: string;
    level?: string;
    type?: string;
    rarity?: string;
    requires_attunement?: string;
}

interface ReferencesProps {
    savedItems: Item[];
    removeItem: (itemId: string) => void;
}

const References: React.FC<ReferencesProps> = ({ savedItems, removeItem }) => {

    const [expandedItems, setExpandedItems] = useState<{ [key: string]: boolean }>({});

    const toggleSeeMore = (itemId: string) => {
        setExpandedItems((prev) => ({
            ...prev,
            [itemId]: !prev[itemId],
        }));
    };
    
    return (
        <div className="references-container">
            {savedItems.length > 0 ? (
                savedItems.map((item) => (
                    <ItemCard
                        key={item.id}
                        item={item}
                        isExpanded={!!expandedItems[item.id]} // Always expanded in references
                        toggleSeeMore={() => toggleSeeMore(item.id)}
                        onDoubleClick={() => removeItem(item.id)}
                    />
                ))
            ) : (
                <p>No references saved.</p>
            )}
        </div>
    );
};

export default References;
