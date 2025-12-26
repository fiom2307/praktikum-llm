import { useEffect, useState } from "react";
import { FiCheckCircle } from "react-icons/fi";

export default function Toast({ title, message, closing, onClose }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    requestAnimationFrame(() => {
      setVisible(true);
    });
  }, []);

  useEffect(() => {
    if (closing) {
      setVisible(false);
    }
  }, [closing]);

  return (
    <div
      role="alert"
      className={`
        fixed top-6 right-6 z-50 max-w-sm
        rounded-md border border-green-500 bg-green-50 p-4 shadow-sm
        transform transition-all duration-300 ease-out
        ${visible
          ? "opacity-100 translate-x-0"
          : "opacity-0 translate-x-8"}
      `}
      onTransitionEnd={() => {
        if (!visible) onClose();
      }}
    >
      <div className="flex items-start gap-4">
        <FiCheckCircle className="h-6 w-6 text-green-700 -mt-0.5" />

        <div className="flex-1">
          <strong className="block font-medium text-green-800">
            {title}
          </strong>
          <p className="mt-0.5 text-sm text-green-700">
            {message}
          </p>
        </div>
      </div>
    </div>
  );
}
