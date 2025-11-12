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
            <Header />

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