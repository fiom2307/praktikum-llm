import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import { Link } from 'react-router-dom';
import { getInventory } from '../api/shopApi';
import { useUser } from '../context/UserContext';
import Mascot from '../components/MascotOutfit';

function InventoryPage() {
    const { currentCostumeId, equipCostumeContext } = useUser();
    const [inventory, setInventory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const COSTUME_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];

    useEffect(() => {
        const fetchInventory = async () => {
        const currentUsername = localStorage.getItem("username");
        
        if (!currentUsername) {
            setError("Error: Username not found. Please log in.");
            setLoading(false);
            return;
        }

        try {

            const inventoryData = await getInventory(currentUsername);
            
            setInventory(inventoryData);
            setError(null); 
            
        } catch (err) {
            console.error("Error fetching inventory:", err);
            setError(err.message); 
            
        } finally {
            setLoading(false);
        }
        };

        fetchInventory();
    }, []);

    const handleEquip = async (itemId) => {
        try {
            await equipCostumeContext(itemId);
        } catch (err) {
            alert("equip failed: " + err.message);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center text-black">
            <Header />

            <h1 className="text-4xl font-extrabold mt-8 mb-8 drop-shadow-md text-center">
                🎒 Il mio zaino
            </h1>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
                    <p>{error}</p>
                    <Link to="/login" className="underline font-bold">Vai al login</Link>
                </div>
            )}

            {/* loading */}
            {loading ? (
                <p className="text-xl animate-pulse">Caricamento elementi in corso...</p>
            ) : (
                <div className="w-full max-w-5xl px-6 pb-12">
                    
                    {/* return to default */}
                    <div className="mb-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                        <div className={`bg-white rounded-2xl shadow-md p-6 flex flex-col gap-4 ${currentCostumeId === 0 ? 'border-2 border-green-500' : ''}`}>
                            <div className="flex items-center gap-5">
                                {/* show default image */}
                                <Mascot alt="Default" className="w-20 h-20 object-contain bg-gray-100 rounded-full p-2"></Mascot>
                                <div>
                                    <h3 className="text-xl font-bold text-gray-800">Aspetto predefinito</h3>
                                    <p className="text-xs text-gray-500 mt-1">Mascotte standard</p>
                                </div>
                            </div>
                            
                            <button 
                                onClick={() => handleEquip(0)} 
                                disabled={currentCostumeId === 0}
                                className={`w-full py-2 rounded-lg font-semibold transition-colors ${
                                    currentCostumeId === 0
                                    ? 'bg-green-100 text-green-700 cursor-default' 
                                    : 'bg-gray-500 text-white hover:bg-gray-600'
                                }`}
                            >
                                {currentCostumeId === 0 ? "Attuale" : "Rimuovi Costume"}
                            </button>
                        </div>
                    </div>

                    {/* item list */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {inventory.length === 0 && !error ? (
                            <div className="col-span-full text-center flex flex-col items-center">
                                <p className="text-xl text-gray-600 mb-4">Il tuo zaino è vuoto.</p>
                                <Link to="/shop" className="bg-blue-500 text-white px-6 py-2 rounded-full hover:bg-blue-600 transition">
                                    Vai al negozio 🛍️
                                </Link>
                            </div>
                        ) : (
                            inventory.filter(item => item.item_id < 100).map((item) => {
                                const isCostume = COSTUME_IDS.includes(item.item_id);
                                const isEquipped = currentCostumeId === item.item_id;
                                // 

                                return (
                                    <div 
                                        key={item.id} 
                                        className={`bg-white rounded-2xl shadow-md p-6 flex flex-col gap-4 hover:scale-105 transition-transform duration-200 ${isEquipped ? 'border-2 border-green-500' : ''}`}
                                    >
                                        <div className="flex items-center gap-5">
                                            
                                            {item.itemId !== null ? (
                                                <Mascot costumeId={item.item_id} alt={item.item_name} className="w-20 h-20 object-contain drop-shadow-md bg-gray-50 rounded-lg"></Mascot>
                                            ) : (
                                                <div className="text-5xl bg-gray-100 p-3 rounded-full">
                                                    {item.emoji || '📦'}
                                                </div>
                                            )}
                                            
                                            <div>
                                                <h3 className="text-xl font-bold text-gray-800">{item.item_name}</h3>
                                                <p className="text-xs text-gray-500 mt-1">
                                                    Acquistato: {new Date(item.purchased_at).toLocaleDateString()}
                                                </p>
                                            </div>
                                        </div>

                                        {isCostume && (
                                            <button 
                                                onClick={() => handleEquip(item.item_id)}
                                                disabled={isEquipped}
                                                className={`w-full py-2 rounded-lg font-semibold transition-colors ${
                                                    isEquipped 
                                                    ? 'bg-green-100 text-green-700 cursor-default' 
                                                    : 'bg-blue-500 text-white hover:bg-blue-600'
                                                }`}
                                            >
                                                {isEquipped ? "Indossato" : "Indossa"}
                                            </button>
                                        )}
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

export default InventoryPage;
