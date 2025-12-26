import Header from "../components/Header";
import { correctAnswers, createReadingText } from "../api/readingApi";
import { useState } from "react";
import LoadingOverlay from "../components/LoadingOverlay";
import ActionButton from "../components/ActionButton";
import ReactMarkdown from "react-markdown";
import { useUser } from "../context/UserContext";
import { incrementPizzaCount } from "../api/pizzaApi";
import { useNavigate, useLocation } from "react-router-dom";


function ReadingPage() {
    const username = localStorage.getItem("username");
    const { updatePizzaCount, activeMultiplier, setActiveMultiplier } = useUser();
    const [userText, setUserText] = useState("");
    const [correctedText, setCorrectedText] = useState("");
    const [generatedText, setGeneratedText] = useState("");
    const [completed, setCompleted] = useState(false);
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();
    //
    const location = useLocation();
    const fromCity = location.state?.fromCity;
    const fromMode = location.state?.fromMode;

    //
    const handleBack = () => {
        if (fromMode === "free") {
            navigate("/free");
            return;
        }

        if (fromCity) {
            navigate(`/city/${fromCity}`);
            return;
        }

        navigate("/");
    };


    async function runAction(action, onSuccess, onError) {
        setLoading(true);
        try {
            const result = await action();
            onSuccess(result);
        } catch (error) {
            console.error("Errore durante l’esecuzione dell’azione:", error);
            onError("Qualcosa è andato storto, per favore riprova.");
        } finally {
            setLoading(false);
        }
    }

    const handleCorrect = async () => {
        if (completed) {
            setCorrectedText("Hai già completato questo esercizio! Generane uno nuovo.");
            return;
        }

        runAction(
            async () => {
                const result = await correctAnswers(userText, generatedText);

                setCorrectedText(result.corrected_answers);
                
                let reward = result.pizzas;
                if (activeMultiplier) {
                    reward = reward * activeMultiplier.value;
                    setActiveMultiplier(null);
                }
                const res = await incrementPizzaCount(reward);                
                updatePizzaCount(res.pizzaCount);

                setCompleted(true);

                return result;
            },
            (result) => setCorrectedText(result.corrected_answers),
            (msg) => setCorrectedText(msg)
        );
    };

    const handleReadingText = async () => {
        if (!username) return alert("Per favore, accedi per inviare le risposte.");
        setCompleted(false);
        runAction(
            () => createReadingText(),
            (result) => setGeneratedText(result),
            (msg) => setGeneratedText(msg)
        );
    };


    return (
        <div className="min-h-screen flex flex-col items-center text-black">
            {loading && <LoadingOverlay message="L’IA sta pensando…" />}

            {/* Header */}
            <Header onBack={handleBack} />

            <h1 className="text-3xl sm:text-4xl font-extrabold drop-shadow-md text-center mb-6">
                📚 Lettura
            </h1>

            {/* Main */}
            <div className="flex items-center justify-center flex-col mb-8 w-full">
                <h3 className="font-semibold mb-2">Esercizio</h3>

                <div className="
                    prose bg-white rounded-xl shadow-sm p-5 
                    w-full max-w-2xl 
                    h-60 sm:h-52 
                    overflow-y-auto leading-relaxed mb-3
                ">
                    <ReactMarkdown>{generatedText}</ReactMarkdown>
                </div>

                <ActionButton 
                    onClick={handleReadingText} 
                    className="bg-[#f8edd5] hover:bg-[#e7d9ba]"
                >
                    Genera
                </ActionButton>
            </div>

            <div className="
                flex flex-col lg:flex-row 
                gap-10 lg:gap-20 
                w-full max-w-5xl 
                items-center lg:items-start
            ">
                {/* User text */}
                <div className="flex items-center justify-center flex-col w-full max-w-md">
                    <h3 className="font-semibold">Il tuo testo</h3>
                    <textarea
                        value={userText}
                        onChange={(e) => setUserText(e.target.value)}
                        className="
                            mt-1 mb-3 resize-none rounded-xl shadow-sm p-3 
                            w-full h-56 
                            focus:outline-none focus:ring-2 focus:ring-blue-400
                        "
                    />
                    <ActionButton onClick={handleCorrect}className="bg-[#f8edd5] hover:bg-[#e7d9ba]">Correggi</ActionButton>
                </div>

                {/* AI correction */}
                <div className="flex flex-col items-center w-full max-w-md">
                    <h3 className="font-semibold">Corretto dall’IA</h3>

                    <div className="
                        prose bg-white rounded-xl shadow-sm p-3 mt-1
                        w-full h-56 overflow-y-auto leading-relaxed
                    ">
                        <ReactMarkdown>{correctedText}</ReactMarkdown>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ReadingPage;
