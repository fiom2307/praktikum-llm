import { SiGoogleforms } from "react-icons/si";

export default function FloatingFormButton({ type }) {
    const isPre = type === "pre";

    const userId = localStorage.getItem("userId");

    const formUrl = isPre
        ? `https://docs.google.com/forms/d/e/1FAIpQLSet9c40nwjKGZ6XGJ2tPWj0hW_960yl0xfAYSaIRm8-pTfaIw/viewform?usp=pp_url&entry.1458977373=${userId}`
        : "https://google.com";

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