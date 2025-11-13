import { createContext, useContext, useState, useEffect } from "react";

const UserContext = createContext();

export function UserProvider({ children }) {
    const [username, setUsername] = useState("");
    const [pizzaCount, setPizzaCount] = useState(0);

    useEffect(() => {
        const storedUsername = localStorage.getItem("username") || "";
        const storedPizza = Number(localStorage.getItem("pizzaCount")) || 0;

        setUsername(storedUsername);
        setPizzaCount(storedPizza);
    }, []);

    const updatePizzaCount = (newCount) => {
        setPizzaCount(newCount);
        localStorage.setItem("pizzaCount", newCount);
    };

    return (
        <UserContext.Provider value={{ username, pizzaCount, updatePizzaCount }}>
            {children}
        </UserContext.Provider>
    );
}

export function useUser() {
    return useContext(UserContext);
}
