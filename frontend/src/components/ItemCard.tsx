import React from "react";
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

const ItemCard: React.FC<ItemCardProps> = ({ item, isExpanded, toggleSeeMore, onDoubleClick }) => {
    const combinedText = item.higher_level
        ? `${item.desc}\n\n${item.higher_level}`
        : item.desc;

    return (
        <div className="item-card" onDoubleClick={onDoubleClick}>
            <div className="card-header">
                <span className="item-name">{item.name}</span>
                <span className="item-category">{item.category}</span>
            </div>

            <div className="item-description">
                {isExpanded ? (
                    <>
                        <TextWithLineBreaks text={combinedText} />
                        {combinedText && combinedText.length > MAX_LENGTH && (
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
                        {combinedText && combinedText.length > MAX_LENGTH && (
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
                {item.range ? <span className="pill">{"Range: " + item.range}</span> : null}
                {item.duration ? <span className="pill">{"Duration: " + item.duration}</span> : null}
                {item.requires_concentration && <span className="pill">Requires Concentration</span>}
                {item.casting_time ? <span className="pill">{"Casting time: " + item.casting_time}</span> : null}
                {item.level > 0 ? <span className="pill">{"Level: " + item.level}</span> : null}
                {item.type ? <span className="pill">{item.type}</span> : null}
                {item.rarity ? <span className="pill">{capitalizeFirstLetter(item.rarity)}</span> : null}
                {item.requires_attunement && <span className="pill">Requires Attunement</span>}
                {item.size ? <span className="pill">{item.size}</span> : null}
                {item.armor_class > 0 ? <span className="pill">{item.armor_class + " AC"}</span> : null}
                {item.is_melee && <span className="pill">Melee</span>}
                {item.damage_dice ? <span className="pill">{"DMG: " + item.damage_dice}</span> : null}
                {item.is_two_handed && <span className="pill">Two Handed</span>}
                {item.ac_display ? <span className="pill">{"Armor Class: " + item.ac_display}</span> : null}
                {item.grants_stealth_disadvantage && <span className="pill">Stealth Disadvantage</span>}
                {item.strength_score_required > 0 ? <span className="pill">{"Strength Required: " + item.strength_score_required}</span> : null}
            </div>
        </div>
    );
};

export default ItemCard;
