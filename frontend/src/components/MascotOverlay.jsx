import { useState } from "react";
import defaultMascotImg from "../assets/hello.png";


/**
 * @param {Array} dialogues - DialogueArray ["Ciao!", "...", "..."]
 * @param {Function} onComplete - DialogueEndFunction
 */

function MascotOverlay({ dialogues, onComplete , currentImage}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isExiting, setIsExiting] = useState(false);

  const handleNext = () => {
    if (currentIndex < dialogues.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setIsExiting(true);
      
      setTimeout(onComplete, 500);
    }
  };

  
  if (!dialogues || dialogues.length === 0) return null;

  return (
    
    <div 
      className={`fixed inset-0 z-50 flex items-end justify-center pb-10 transition-opacity duration-500
      ${isExiting ? "opacity-0 pointer-events-none" : "opacity-100 backdrop-blur-md bg-black/20"}`}
    >
      
      <div className={`relative flex items-end w-full max-w-5xl px-4 transition-transform duration-500 ${isExiting ? "translate-y-full" : "translate-y-0"}`}>
        
        {/* mascot image */}
        <img 
          src={currentImage || defaultMascotImg} 
          alt="Mascot" 
          className="w-1/3 md:w-1/4 object-contain drop-shadow-2xl animate-bounce-slow"
          style={{ maxHeight: "60vh" }} 
        />
        
        {/* Dialogue Box */}
        <div className="relative bg-white border-4 border-blue-500 rounded-3xl p-6 mb-20 ml-[-20px] shadow-xl w-full max-w-lg min-h-[150px] flex flex-col justify-between animate-fade-in-up">
          
          <div className="absolute left-[-16px] bottom-10 w-0 h-0 border-t-[15px] border-t-transparent border-r-[20px] border-r-blue-500 border-b-[15px] border-b-transparent"></div>
          <div className="absolute left-[-10px] bottom-10 w-0 h-0 border-t-[15px] border-t-transparent border-r-[20px] border-r-white border-b-[15px] border-b-transparent"></div>

          <p className="text-xl font-medium text-gray-800 leading-relaxed">
            {dialogues[currentIndex]}
          </p>

          {/* next step*/}
          <button 
            onClick={handleNext}
            className="self-end mt-2 text-blue-500 hover:text-blue-700 hover:scale-110 transition-transform animate-pulse cursor-pointer p-2"
          >
            {/* icon */}
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 21l-12-18h24z" />
            </svg>
          </button>
        </div>

      </div>
    </div>
  );
}

export default MascotOverlay;