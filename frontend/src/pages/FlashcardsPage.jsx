import Header from "../components/Header";
import { getFlashcards } from "../api/flashcardApi";
import { useEffect, useState } from "react";

function FlashcardsPage() {    
    const username = localStorage.getItem("username") || "";
    const [flashcards, setFlashcards] = useState([]);

    useEffect(() => {
        async function loadFlashcards() {
            const cards = await getFlashcards();
            setFlashcards(cards);
        }
        loadFlashcards();
    }, [username]);

    return (
        <div className="min-h-screen flex flex-col items-center text-black">
            {/* Header */}
            <Header />

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                Flashcard
            </h1>

            
            {/* Main */}
            <div className="grid grid-cols-3 gap-4 mt-4">
                {flashcards.map((card, index) => (
                    <div 
                        key={index}
                        className="bg-white shadow-md rounded-xl px-6 py-4 text-xl font-semibold text-center"
                    >
                        {card.word}
                    </div>
                ))}
            </div>
            
        </div>
    );
}

export default FlashcardsPage;