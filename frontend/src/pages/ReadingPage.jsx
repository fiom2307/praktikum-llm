import { useNavigate } from "react-router-dom";
import { correctAnswers, createReadingText } from "../api/backendApi";
import { useState } from "react";

function ReadingPage() {
    const pizzaCount = localStorage.getItem("pizzaCount");
    const username = localStorage.getItem("username");

    const navigate = useNavigate();

    const [userText, setUserText] = useState("");
    const [correctedText, setCorrectedText] = useState("");
    const [generatedText, setGeneratedText] = useState("");

    const handleCorrect = async () => {
        const corrected = await correctAnswers(userText, generatedText);
        setCorrectedText(corrected);
    }

    const handleReadingText = async () => {
        const readingText = await createReadingText();
        setGeneratedText(readingText);
    }
    
    return (
        <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
            {/* Header */}
            <header className="w-full flex justify-between items-start p-6">
                
                {/* Back Button */}
                <button
                    onClick={() => navigate("/")}
                    className="bg-blue-400 hover:bg-blue-500 font-semibold px-3 py-1 rounded-xl shadow-md">
                        ← Back
                    </button>

                {/* Username + Pizza Count */}
                <div className="text-right flex flex-col items-end gap-1">
                <div className="flex items-center gap-2">
                    <h2 className="text-xl font-bold">{username}</h2>
                </div>
                    <p className="text-sm">
                    🍕 <span className="font-semibold">Pizza count:</span> {pizzaCount}
                    </p>
                </div>
            </header>

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                📚 Reading
            </h1>

            
            {/* Main */}
            <div>
                <div>
                    <h3>Aufgabe</h3>
                    <textarea
                        value={generatedText}
                        readOnly
                        rows={8}
                        cols={40}
                    />
                    <br />
                    <button onClick={handleReadingText} class="bg-white">Generate</button>
                </div>
                <div>
                    <h3>Your Text</h3>
                    <textarea
                        value={userText}
                        onChange={(e) => setUserText(e.target.value)}
                        rows={8}
                        cols={40}
                    />
                    <br />
                    <button onClick={handleCorrect} class="bg-white">Correct</button>
                </div>
                <div>
                    <h3>Corrected by AI</h3>
                    <textarea
                        value={correctedText}
                        readOnly
                        rows={8}
                        cols={40}
                    />
                </div>
            </div>
        </div>
    );
}

export default ReadingPage;