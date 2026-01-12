import Header from "../components/Header";
import { getFlashcards } from "../api/flashcardApi";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

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

            <h1 className="text-4xl font-extrabold mb-8 drop-shadow-md text-center">
                Flashcard
            </h1>

            
            {/* Main */}
            <div className="grid grid-cols-2 gap-4 mt-4 max-w-4xl">
                {flashcards.map((card, index) => (
                    <div
                    key={index}
                    className="
                        group
                        bg-white shadow-md rounded-xl px-6 py-4
                        text-xl font-semibold text-center
                        transition-all duration-300
                        hover:scale-105
                    "
                    >
                    {/* WORD */}
                    <div className="text-2xl">
                        <ReactMarkdown>{card.word}</ReactMarkdown>
                    </div>

                    {/* DEFINITION (hidden until hover) */}
                    <div
                        className="
                        mt-4
                        text-base font-normal text-gray-700
                        opacity-0 max-h-0 overflow-hidden
                        transition-all duration-300
                        group-hover:opacity-100 group-hover:max-h-40
                        "
                    >
                        <ReactMarkdown>{card.definition}</ReactMarkdown>
                    </div>
                    </div>
                ))}
                </div>

            
        </div>
    );
}

export default FlashcardsPage;