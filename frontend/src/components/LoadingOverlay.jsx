export default function LoadingOverlay({ message = "Loading..." }) {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50">
      <div className="bg-white px-6 py-4 rounded-xl shadow-lg flex flex-col items-center gap-3">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-t-transparent border-blue-400"></div>
        <p className="font-semibold">{message}</p>
      </div>
    </div>
  );
}