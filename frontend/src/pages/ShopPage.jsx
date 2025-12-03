import Header from "../components/Header";

function ShopPage() {
    const items = [
        { id: 1, emoji: "🍕", name: "Pizza Slice", cost: 0 },
        { id: 2, emoji: "☕", name: "Coffee Cup", cost: 2 },
        { id: 3, emoji: "🎁", name: "Sticker Pack", cost: 3 },
        { id: 4, emoji: "📚", name: "Grammar Book", cost: 4 },
        { id: 5, emoji: "🎧", name: "Music Pass", cost: 5 },
        { id: 6, emoji: "💡", name: "Hint Token", cost: 6 },
    ];
    
    return (
        <div className="min-h-screen flex flex-col items-center  text-black">
            {/* Header */}
            <Header />

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                🛍️ Shop
            </h1>

            {/* Item grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 px-6 pb-12">
                {items.map((item) => (
                <div
                key={item.id}
                className="bg-white rounded-2xl shadow-lg p-6 flex flex-col items-center justify-between transition-transform hover:scale-105">
                    <span className="text-6xl mb-4">{item.emoji}</span>
                    <h3 className="text-xl font-bold mb-6">{item.name}</h3>
                    <button className="bg-blue-400 hover:bg-blue-500 font-semibold px-6 py-2 rounded-xl shadow-md">
                        <span className="text-sm opacity-90">🍕 {item.cost}</span>
                    </button>
                </div>
                ))}
            </div>
            
        </div>
    );
}

export default ShopPage;