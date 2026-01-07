import React, { useState } from 'react';
import MascotOutfit from './MascotOutfit';
import { FaQuestionCircle, FaTimes } from 'react-icons/fa';

export default function HelpModal({ costumeId }) {
    const [isOpen, setIsOpen] = useState(false);
    const [answer, setAnswer] = useState("Ciao! Hai qualche domanda sulle attività?");

    const qaList = [
        { 
            q: "Lettura (Reading)", 
            a: "Clicca 'Genera', leggi il testo e rispondi a 5 domande nel riquadro. 5 risposte corrette = 5 Pizze!" 
        },
        { 
            q: "Vocabolario (Vocabulary)", 
            a: "Clicca 'Genera' e indovina la parola usando i 3 indizi. Ogni parola indovinata = 1 Pizza!" 
        },
        { 
            q: "Scrittura (Writing)", 
            a: "Scrivi 50-150 parole sul tema scelto. Clicca 'Correggi' per i miei suggerimenti. Testo eccellente = 10 Pizze!" 
        }
    ];

    return (
        <>
            {/* button */}

            <button 
                onClick={() => setIsOpen(true)}
                className="fixed right-5 top-[92px] z-40 bg-white/90 hover:bg-white text-black rounded-2xl shadow-lg border border-black/10 px-3 py-2 flex items-center gap-2 transition-all"
            >
                <FaQuestionCircle className="text-xl text-blue-500" />
                <span className="text-sm font-semibold">Aiuto</span>
            </button>
            
            {/* Q&A format */}
            {isOpen && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
                    <div className="bg-white rounded-3xl p-6 max-w-md w-full shadow-2xl relative animate-in fade-in zoom-in duration-200">
                        {/* closing button */}
                        <button 
                            onClick={() => setIsOpen(false)}
                            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
                        >
                            <FaTimes size={24} />
                        </button>

                        <div className="flex flex-col items-center">
                            {/* mascot */}
                            <div className="w-32 h-32 mb-4 bg-blue-50 rounded-full p-2 border-4 border-white shadow-inner">
                                <MascotOutfit costumeId={costumeId} className="w-full h-full object-contain" />
                            </div>

                            {/* dialogue */}
                            <div className="relative bg-blue-500 text-white p-4 rounded-2xl mb-6 text-center shadow-lg">
                                <p className="text-sm font-medium leading-relaxed italic">
                                    "{answer}"
                                </p>
                                {/* pointer */}
                                <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-0 h-0 border-l-[8px] border-l-transparent border-r-[8px] border-r-transparent border-b-[8px] border-b-blue-500"></div>
                            </div>

                            {/* question list */}
                            <div className="flex flex-col gap-2 w-full">
                                {qaList.map((item, idx) => (
                                    <button 
                                        key={idx}
                                        onClick={() => setAnswer(item.a)}
                                        className="w-full py-3 px-4 bg-gray-50 hover:bg-blue-100 rounded-xl text-left text-sm font-bold text-gray-700 transition-colors border border-gray-100"
                                    >
                                        ❓ {item.q}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}