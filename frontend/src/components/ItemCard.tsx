import React from "react";
import "./ItemFeed.css";

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

interface ItemCardProps {
    item: Item;
    isExpanded: boolean;
    toggleSeeMore: () => void;
    onClick: () => void;
}

const MAX_LENGTH = 150;

const truncateText = (text: string, length: number) => {
    return text && text.length > length ? `${text.substring(0, length)}...` : text;
};

const getTruncatedDescription = (item: Item, length = MAX_LENGTH) => {
    let combinedText = "";
    if (item.desc) combinedText += item.desc;
    if (item.higher_level) combinedText += "\n\n" + item.higher_level;
    return truncateText(combinedText, length);
};

const capitalizeFirstLetter = (str: string) => str.charAt(0).toUpperCase() + str.slice(1);

const TextWithLineBreaks: React.FC<{ text: string }> = ({ text }) => (
    <div>
        {text.split("\n").map((line, index) => (
            <React.Fragment key={index}>
                {line}
                <br />
            </React.Fragment>
        ))}
    </div>
);

const ItemCard: React.FC<ItemCardProps> = ({ item, isExpanded, toggleSeeMore, onClick }) => {
    const combinedText = item.higher_level
        ? `${item.desc}\n\n${item.higher_level}`
        : item.desc;

    return (
        <div className="item-card" onClick={onClick}>
            <div className="card-header">
                <span className="item-name">{item.name}</span>
                <span className="item-category">{item.category}</span>
            </div>

            <div className="item-description">
                {isExpanded ? (
                    <>
                        <TextWithLineBreaks text={combinedText} />
                        {combinedText.length > MAX_LENGTH && (
                            <a
                                href="#"
                                className="see-more-link"
                                onClick={(e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    toggleSeeMore();
                                } }
                            >
                                Show Less
                            </a>
                            
                        )}
                    </>
                ) : (
                    <>
                        <TextWithLineBreaks text={getTruncatedDescription(item)} />
                        {combinedText.length > MAX_LENGTH && (
                            <a
                                href="#"
                                className="see-more-link"
                                onClick={(e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    toggleSeeMore();
                                } }
                            >
                                Show More
                            </a>
                            
                        )}
                    </>
                )}
            </div>

            <div className="item-details">
                {item.range && <span className="pill">{"Range: " + item.range}</span>}
                {item.duration && <span className="pill">{"Duration: " + item.duration}</span>}
                {item.requires_concentration && <span className="pill">Requires Concentration</span>}
                {item.casting_time && <span className="pill">{"Casting time: " + item.casting_time}</span>}
                {item.level && <span className="pill">{item.level}</span>}
                {item.type && <span className="pill">{item.type}</span>}
                {item.rarity && <span className="pill">{capitalizeFirstLetter(item.rarity)}</span>}
                {item.requires_attunement && <span className="pill">Requires Attunement</span>}
            </div>
        </div>
    );
};

export default ItemCard;
