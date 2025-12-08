import { createContext, useContext, useState, useEffect } from "react";

const UserContext = createContext();

export function UserProvider({ children }) {
    const [pizzaCount, setPizzaCount] = useState(0);
    const [username, setUsername] = useState(null);

    useEffect(() => {
        const storedPizza = Number(localStorage.getItem("pizzaCount")) || 0;

        setPizzaCount(storedPizza);

        const storedUsername = localStorage.getItem("username") || null;

        setUsername(storedUsername);

    }, []);

    const updatePizzaCount = (newCount) => {
        setPizzaCount(newCount);
        localStorage.setItem("pizzaCount", newCount);
    };    

    const loginUserContext = (userData) => {
        const user = userData.user;
        updatePizzaCount(userData.pizza_count);
        setUsername(user.username);
        localStorage.setItem("username", user.username);
    }

    const logoutUserContext = () => {
        setPizzaCount(0);
        setUsername(null);
        localStorage.removeItem("pizzaCount");
        localStorage.removeItem("username");
    };

    return (
        <UserContext.Provider value={{ pizzaCount, updatePizzaCount, loginUserContext, username, loginUserContext, logoutUserContext }}>
            {children}
        </UserContext.Provider>
    );
}

export function useUser() {
    return useContext(UserContext);
}
