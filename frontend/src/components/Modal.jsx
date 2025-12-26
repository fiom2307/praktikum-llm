import { FiX } from "react-icons/fi";

export default function Modal({
    title = "Attenzione",
    message,
    onClose,
}) {
    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
            role="dialog"
            aria-modal="true"
            aria-labelledby="modalTitle"
            onClick={onClose}
        >
        {/* Modal box */}
        <div
            className="w-full max-w-md rounded-2xl bg-white p-6 shadow-lg"
            onClick={(e) => e.stopPropagation()}
        >
            {/* Header */}
            <div className="flex items-start justify-between">
            <h2
                id="modalTitle"
                className="text-xl font-bold text-gray-900 sm:text-2xl"
            >
                {title}
            </h2>

            <button
                type="button"
                onClick={onClose}
                className="-me-3 -mt-3 rounded-full p-2 text-gray-400 transition hover:bg-gray-100 hover:text-gray-600 focus:outline-none"
                aria-label="Close"
            >
                <FiX className="h-5 w-5" />
            </button>
            </div>

            {/* Body */}
            <div className="mt-4">
            <p className="text-gray-700">{message}</p>
            </div>
        </div>
        </div>
    );
}