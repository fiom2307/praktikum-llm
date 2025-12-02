import { createContext, useContext, useState, useEffect } from "react";

const UserContext = createContext();

export function UserProvider({ children }) {
    const [pizzaCount, setPizzaCount] = useState(0);

    useEffect(() => {
        const storedPizza = Number(localStorage.getItem("pizzaCount")) || 0;

        setPizzaCount(storedPizza);
    }, []);

    const updatePizzaCount = (newCount) => {
        setPizzaCount(newCount);
        localStorage.setItem("pizzaCount", newCount);
    };    

    const loginUserContext = (userData) => {
        updatePizzaCount(userData.pizza_count);
    }

    return (
        <UserContext.Provider value={{ pizzaCount, updatePizzaCount, loginUserContext }}>
            {children}
        </UserContext.Provider>
    );
}

export function useUser() {
    return useContext(UserContext);
}
