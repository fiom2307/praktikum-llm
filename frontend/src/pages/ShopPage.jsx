import Header from "../components/Header";
import { useUser } from "../context/UserContext"; 
import { buyItem } from "../api/shopApi"; 
import { useState } from "react";


function ShopPage() {

    const { pizzaCount, updatePizzaCount } = useUser();
    const [boughtItems, setBoughtItems] = useState({});
    const [isBuying, setIsBuying] = useState(false);

    const items = [
        { id: 1, emoji: "🍕", name: "Pizza Slice", cost: 0 },
        { id: 2, emoji: "☕", name: "Coffee Cup", cost: 2 },
        { id: 3, emoji: "🎁", name: "Sticker Pack", cost: 3 },
        { id: 4, emoji: "📚", name: "Grammar Book", cost: 4 },
        { id: 5, emoji: "🎧", name: "Music Pass", cost: 5 },
        { id: 6, emoji: "💡", name: "Hint Token", cost: 6 },
    ];

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
        <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
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
                            <span className="text-6xl mb-4">{item.emoji}</span>
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