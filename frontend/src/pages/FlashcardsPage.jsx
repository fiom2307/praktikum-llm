import Header from "../components/Header";

function FlashcardsPage() {    
    return (
        <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
            {/* Header */}
            <Header />

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                Flashcards
            </h1>

            
            {/* Main */}
            
        </div>
    );
}

export default FlashcardsPage;