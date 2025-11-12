export default function ActionButton({ onClick, children, className = "" }) {
    return (
        <button
        onClick={onClick}
        className={`bg-blue-400 hover:bg-blue-500 font-semibold px-3 py-1 rounded-xl shadow-md ${className}`}
        >
        {children}
        </button>
    );
}
