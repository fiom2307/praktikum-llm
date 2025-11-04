import { useNavigate } from "react-router-dom";

function TextProductionPage() {
    const username = "CoolFrog74"
    const pizzaCount = 3;

    const navigate = useNavigate();
    
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
                📖 Text Production
            </h1>
            {/* Main */}
            
        </div>
    );
}

export default TextProductionPage;