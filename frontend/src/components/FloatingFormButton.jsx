import { SiGoogleforms } from "react-icons/si";

export default function FloatingFormButton({ baseUrl }) {
    const userId = localStorage.getItem("userId");

    const formUrl = `${baseUrl}${userId}`;

    return (
        <a
            href={formUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={`fixed bottom-6 right-6 z-50
                p-5 rounded-full shadow-xl
                bg-purple-600 hover:bg-purple-700
                text-white`}
        >
            <SiGoogleforms size={22} />
        </a>
    );
}