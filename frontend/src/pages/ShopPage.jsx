import Header from "../components/Header";
import { useUser } from "../context/UserContext"; 
import { buyItem, getInventory } from "../api/shopApi"; 
import { useState, useEffect } from "react";
import MascotOutfit from "../components/MascotOutfit";

//all images
// import outfits from "../assets/outfits"


function ShopPage() {

    const { pizzaCount, updatePizzaCount } = useUser();
    const [boughtItems, setBoughtItems] = useState({});
    const [isBuying, setIsBuying] = useState(false);

    const items = [
        { id: 1, emoji: "⚫️", name: "Darth Vader", cost: 1, isCostume: true },
        { id: 2, emoji: "🛡️", name: "Gladiator", cost: 1, isCostume: true },
        { id: 3, emoji: "👨‍🍳", name: "Pizza Chef", cost: 1, isCostume: true },
        { id: 4, emoji: "🌹", name: "The Godfather", cost: 1, isCostume: true },
        { id: 5, emoji: "⚽", name: "Maradona", cost: 2, isCostume: true },
        { id: 6, emoji: "🏎️", name: "Ferrari Man", cost: 1, isCostume: true },
        // more further items
        { id: 7, emoji: "☕", name: "Barista", cost: 1, isCostume: true },
        { id: 8, emoji: "🎭", name: "Venetian Mask", cost: 1, isCostume: true },
        { id: 9, emoji: "🍄", name: "Super Plumber", cost: 3, isCostume: true },
        { id: 10, emoji: "🎨", name: "The Artist", cost: 2, isCostume: true },
        { id: 11, emoji: "🛵", name: "Vespa Rider", cost: 2, isCostume: true },
        { id: 12, emoji: "👑", name: "The Emperor", cost: 4, isCostume: true },
        { id: 13, emoji: "⛵️", name: "The Captain", cost: 2, isCostume: true },
        { id: 14, emoji: "🥊", name: "Boxer", cost: 1, isCostume: true },
        
    ];

    useEffect(() => {
        const fetchOwnedItems = async () => {
            const currentUsername = localStorage.getItem("username");
            if (!currentUsername) return;

            try {
                const inventory = await getInventory(currentUsername);
                
                const ownedMap = {};
                inventory.forEach(item => {
                    ownedMap[item.item_id] = true;
                });
                
                setBoughtItems(ownedMap);
                
            } catch (err) {
                console.error("Failed to load inventory in shop:", err);
            }
        };

        fetchOwnedItems();
    }, []);

    const handleBuy = async (item, cost) => {

        const currentUsername = localStorage.getItem("username");

        if (!currentUsername) {
            alert("Please log in first (No username found).");
            return;
        }

        if (cost > pizzaCount) {
            alert(`Non hai abbastanza pizze per comprare ${item.name}! Ti servono ${cost} pizze.`);
            return;
        }

        try {

            const result = await buyItem(currentUsername, item.id, item.cost);
            
            if (result.new_pizza_count !== undefined) {
                updatePizzaCount(result.new_pizza_count);
                
                if (!item.consumable) {
                        setBoughtItems(prev => ({ ...prev, [item.id]: true }));
                }
                
                console.log(`Bought ${item.name}`);
            }
        } catch (error) {
            alert(`Acquisto fallito: ${error.message}`);
        } finally {
            setIsBuying(false);
        }
        
    };


    
    return (
        <div className="min-h-screen flex flex-col items-center  text-black">
            {/* Header */}
            <Header />

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                🛍️ Shop 
            </h1>

            {/* Item grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 px-6 pb-12">
                {items.map((item) => {
                    const isBought = !item.consumable && boughtItems[item.id];
                    const canAfford = item.cost <= pizzaCount;

                    return (
                        <div
                            key={item.id}
                            className={`bg-white rounded-2xl shadow-lg p-6 flex flex-col items-center justify-between transition-transform hover:scale-105 ${
                                isBought ? 'opacity-70 border-2 border-green-500' : ''
                            }`}
                        >

                            {item.isCostume ? (
                                <div className="h-24 w-auto mb-4 flex items-center justify-center">
                                     <MascotOutfit 
                                        costumeId={item.id} //
                                        className="h-full object-contain drop-shadow-md" 
                                     />
                                </div>
                            ) : (
                                // 
                                <span className="text-6xl mb-4">{item.emoji}</span>
                            )}

                            <h3 className="text-xl font-bold mb-6">{item.name}</h3>
                            
                            <button 
                                onClick={() => handleBuy(item, item.cost)} 
                                className={`font-semibold px-6 py-2 rounded-xl shadow-md transition-colors ${
                                    isBought 
                                    ? 'bg-green-500 cursor-default text-white'
                                    : canAfford 
                                        ? 'bg-blue-400 hover:bg-blue-500' 
                                        : 'bg-gray-400 cursor-not-allowed text-gray-700'
                                }`}
                                disabled={isBought || !canAfford || isBuying}
                            >
                                <span className="text-sm opacity-90">
                                    {isBought ? 'Comprato!' : `🍕 ${item.cost}`}
                                </span>
                            </button>
                        </div>
                    );
                })}
            </div>
            
        </div>
    );
}

export default ShopPage;