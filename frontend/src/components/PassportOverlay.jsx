import { useEffect } from "react";

export default function PassportOverlay({
  open,
  onClose,
  cityTitle,
  badgeSrc,
  infoLines = []
}) {
  useEffect(() => {
    if (!open) return;

    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const onKeyDown = (e) => {
      if (e.key === "Escape") onClose?.();
    };

    window.addEventListener("keydown", onKeyDown);

    return () => {
      document.body.style.overflow = prev;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[9999]">
      <div className="absolute inset-0 bg-black/45" onClick={onClose} />

      <div className="absolute inset-0 flex items-center justify-center p-4">
        <div className="w-full max-w-5xl max-h-[85vh] overflow-auto rounded-2xl shadow-2xl bg-[#f7f0d9] border border-black/10">
          <div className="flex items-center justify-between px-6 py-4 bg-[#e6d3a6] border-b border-black/10">
            <h2 className="text-lg font-extrabold">Passaporto di viaggio</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-0">
            <div className="p-6 bg-[#fbf4de] border-b md:border-b-0 md:border-r border-black/10">
              <h3 className="text-2xl font-extrabold mb-3">📍 {cityTitle}</h3>

              <ul className="space-y-3 text-base text-black/80">
                {infoLines.map((line, idx) => (
                  <li key={idx} className="flex gap-2">
                    <span className="mt-[2px]">•</span>
                    <span>{line}</span>
                  </li>
                ))}
              </ul>

              <div className="mt-6 pt-4 border-t border-black/10 text-sm text-black/70">
                Per ottenere il badge, completa la città.
              </div>
            </div>

            <div className="p-6 bg-[#fff7e6] flex flex-col items-center justify-center">
              <div className="text-lg font-extrabold mb-4">Badge della città</div>

              {badgeSrc ? (
                <img
                  src={badgeSrc}
                  alt={`${cityTitle} badge`}
                  className="w-[240px] max-w-[70%] h-auto drop-shadow-lg"
                />
              ) : (
                <div className="text-sm text-black/60">
                  Nessun badge disponibile per questa città.
                </div>
              )}
            </div>
          </div>

          <div className="px-6 py-4 flex justify-end bg-[#f7f0d9] border-t border-black/10">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-black text-white font-semibold hover:bg-black/90"
            >
              Chiudi
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}