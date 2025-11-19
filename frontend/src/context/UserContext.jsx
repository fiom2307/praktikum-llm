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

    //
    const updateUsername = (newUsername) => {
        setUsername(newUsername);
        localStorage.setItem("username", newUsername);
    }
    
    //
    const loginUserContext = (userData) => {
        updateUsername(userData.username);
        updatePizzaCount(userData.pizzaCount);
    }

    return (
        <UserContext.Provider value={{ username, pizzaCount, updatePizzaCount, loginUserContext }}>
            {children}
        </UserContext.Provider>
    );
}

export function useUser() {
    return useContext(UserContext);
}
