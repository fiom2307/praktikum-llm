import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import { Link } from 'react-router-dom';
import { getInventory } from '../api/shopApi';

function InventoryPage() {
    const [inventory, setInventory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

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

    return (
        <div className="min-h-screen flex flex-col items-center bg-blue-100 text-black">
            <Header />

            <h1 className="text-4xl font-extrabold mt-8 mb-8 drop-shadow-md text-center">
                🎒 My Backpack
            </h1>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
                    <p>{error}</p>
                    <Link to="/login" className="underline font-bold">Go to Login</Link>
                </div>
            )}

            {/* loading */}
            {loading ? (
                <p className="text-xl animate-pulse">Loading items...</p>
            ) : (
                /* item list table */
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 px-6 pb-12 w-full max-w-5xl">
                    {inventory.length === 0 && !error ? (
                        <div className="col-span-full text-center flex flex-col items-center">
                            <p className="text-xl text-gray-600 mb-4">Your backpack is empty.</p>
                            <Link to="/shop" className="bg-blue-500 text-white px-6 py-2 rounded-full hover:bg-blue-600 transition">
                                Go to Shop 🛍️
                            </Link>
                        </div>
                    ) : (
                        inventory.map((item) => (
                            <div 
                                key={item.id} 
                                className="bg-white rounded-2xl shadow-md p-6 flex items-center gap-5 hover:scale-105 transition-transform duration-200"
                            >
                                {/* show emoji */}
                                <div className="text-5xl bg-gray-100 p-3 rounded-full">
                                    {item.emoji || '📦'}
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-gray-800">{item.item_name}</h3>
                                    <p className="text-xs text-gray-500 mt-1">
                                        Bought: {new Date(item.purchased_at).toLocaleDateString()}
                                    </p>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            )}
        </div>
    );
}

export default InventoryPage;