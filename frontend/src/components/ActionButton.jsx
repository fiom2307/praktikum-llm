export default function ActionButton({ onClick, children, className = "" }) {
    return (
        <button
        onClick={onClick}
        className={`font-bold px-6 py-2 rounded-xl shadow-md ${className}`}
        >
        {children}
        </button>
    );
}
