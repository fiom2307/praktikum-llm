import Header from "../components/Header";
import { useUser } from "../context/UserContext"; 
import { buyItem, getInventory } from "../api/shopApi"; 
import { useState, useEffect } from "react";
import MascotOutfit from "../components/MascotOutfit";
import multiplier2x from '../assets/multipliers/2x.png';
import multiplier3x from '../assets/multipliers/3x.png';
import multiplier10x from '../assets/multipliers/10x.png';

//all images
// import outfits from "../assets/outfits;"



function ShopPage() {

    const { pizzaCount, updatePizzaCount, activeMultiplier, setActiveMultiplier  } = useUser();
    const [boughtItems, setBoughtItems] = useState({});
    const [isBuying, setIsBuying] = useState(false);


    const items = [
        { id: 1, emoji: "⚫️", name: "Darth Vader", cost: 30, isCostume: true },
        { id: 2, emoji: "🛡️", name: "Gladiatore", cost: 25, isCostume: true },
        { id: 3, emoji: "👨‍🍳", name: "Pizzaiolo", cost: 25, isCostume: true },
        { id: 4, emoji: "🌹", name: "Il Padrino", cost: 25, isCostume: true },
        { id: 5, emoji: "⚽", name: "Maradona", cost: 30, isCostume: true },
        { id: 6, emoji: "🏎️", name: "Pilota Ferrari", cost: 25, isCostume: true },
        // more further items
        { id: 7, emoji: "☕", name: "Barista", cost: 25, isCostume: true },
        { id: 8, emoji: "🎭", name: "Maschera Veneziana", cost: 25, isCostume: true },
        { id: 9, emoji: "🍄", name: "Super Idraulico", cost: 30, isCostume: true },
        { id: 10, emoji: "🎨", name: "L'artista", cost: 30, isCostume: true },
        { id: 11, emoji: "🛵", name: "Motociclista Vespa", cost: 25, isCostume: true },
        { id: 12, emoji: "👑", name: "L'Imperatore", cost: 30, isCostume: true },
        { id: 13, emoji: "⛵️", name: "Il Capitano", cost: 30, isCostume: true },
        { id: 14, emoji: "🥊", name: "Pugile", cost: 25, isCostume: true },
    ];

    const multipliers = [
        { id: 101, name: "Punti doppi", cost: 10, image: multiplier2x, value: 2 },
        { id: 102, name: "Punti tripli ", cost: 15, image: multiplier3x, value: 3 },
        { id: 103, name: "Dieci punti o niente", cost: 25, image: multiplier10x, value: 10  }
    ]

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
        setIsBuying(true);

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
                
                if (item.isCostume) {
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

    const handleBuyMultiplier = async (item) => {
        if (activeMultiplier) return;

        setIsBuying(true);

        const currentUsername = localStorage.getItem("username");

        setIsBuying(true);

        try {
            const result = await buyItem(currentUsername, item.id, item.cost);
            updatePizzaCount(result.new_pizza_count);

            // activar multiplicador
            setActiveMultiplier({
                id: item.id,
                value: item.value 
            });

        } catch (err) {
            alert("Purchase failed");
        } finally {
            setIsBuying(false);
        }
    };



    
    return (
    <div className="min-h-screen flex flex-col items-center text-black">
        {/* Header */}
        <Header />

        <h1 className="text-4xl font-extrabold mt-0 mb-10 drop-shadow-md text-center">
            🛍️ Shop
        </h1>

        <section className="w-full  max-w-6xl px-6 pb-12">
            <h2 className="text-3xl font-bold mb-2 text-center">
                ✖️ Moltiplicatori
            </h2>
            <p className="text-sm font-semibold text-gray-700 leading-relaxed mb-4 items-center text-center">
                Un moltiplicatore di punti ti permette di guadagnare più pizze.
                Una volta acquistato, si attiva automaticamente per la partita successiva.
                <br />
                Il moltiplicatore <strong> 10X </strong> funziona solo se produci almeno <strong> 7 </strong> pizze nella modalità
                <strong> Produzione scritta </strong> o <strong> 4 </strong> pizze nella modalità
                <strong> Lettura </strong>.
                Se ne produci meno, non si attiva e lo perdi.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                {multipliers.map(item => {
                    const canAfford = item.cost <= pizzaCount;
                    return (
                        <div
                            key={item.id}
                            className="bg-white min-h-[220px] rounded-2xl shadow-lg p-6 flex flex-col items-center gap-4"
                            >
                            <img
                                src={item.image}
                                alt={item.name}
                                className="h-20 w-auto drop-shadow-md"
                            />

                            <h3 className="text-xl font-bold items-center justify-center">
                                {item.name}
                            </h3>

                            <button
                                onClick={() => handleBuyMultiplier(item)}
                                disabled={!canAfford || isBuying || activeMultiplier}
                                className={`px-6 py-2 rounded-xl ${
                                    activeMultiplier
                                        ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
                                        : canAfford
                                            ? 'bg-blue-400 hover:bg-blue-500 text-white'
                                            : 'bg-gray-400 cursor-not-allowed'
                                }`}>
                                {activeMultiplier
                                    ? `Attivo ${activeMultiplier.value}X`
                                    : `🍕 ${item.cost}`
                                }
                            </button>

                            </div>

                    );
                })}
            </div>
        </section>


        {/* ===================== COSTUMI ===================== */}
        <section className="w-full max-w-6xl px-6 mb-16">
            <h2 className="text-3xl font-bold mb-8 text-center">
                🎭 Costumi
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                {items
                    .filter(item => item.isCostume)
                    .map(item => {
                        const isBought = boughtItems[item.id];
                        const canAfford = item.cost <= pizzaCount;

                        return (
                            <div
                                key={item.id}
                                className={`bg-white rounded-2xl shadow-lg p-6 flex flex-col items-center justify-between transition-transform hover:scale-105 ${
                                    isBought ? 'opacity-70 border-2 border-green-500' : ''
                                }`}
                            >
                                <div className="h-24 w-auto mb-4 flex items-center justify-center">
                                    <MascotOutfit
                                        costumeId={item.id}
                                        className="h-full object-contain drop-shadow-md"
                                    />
                                </div>

                                <h3 className="text-xl font-bold mb-6 items-center justify-center">
                                    {item.name}
                                </h3>

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
        </section>
    </div>
);

}

export default ShopPage;