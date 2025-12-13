import { createContext, useContext, useState, useEffect } from "react";
import { equipCostume } from '../api/userApi';

const UserContext = createContext();

export function UserProvider({ children }) {
    const [pizzaCount, setPizzaCount] = useState(0);
    const [username, setUsername] = useState(null);
    const [currentCostumeId, setCurrentCostumeId] = useState(0);

    useEffect(() => {
        const storedPizza = Number(localStorage.getItem("pizzaCount")) || 0;

        setPizzaCount(storedPizza);

        const storedUsername = localStorage.getItem("username") || null;

        setUsername(storedUsername);

        const storedCostumeId = Number(localStorage.getItem("currentCostumeId")) || 0;

        setCurrentCostumeId(storedCostumeId);

    }, []);

    const updatePizzaCount = (newCount) => {
        setPizzaCount(newCount);
        localStorage.setItem("pizzaCount", newCount);
    };    

    const updateCostumeId = (newId) => {
        setCurrentCostumeId(newId);
        localStorage.setItem("currentCostumeId", newId);
    };

    const loginUserContext = (userData) => {
        if (!userData || !userData.user) {
            console.error("Login data is missing or malformed.");
            return; 
        }
        const user = userData.user;
        updatePizzaCount(user.pizza_count);
        updateCostumeId(user.current_costume_id || 0);
        setUsername(user.username);
        localStorage.setItem("username", user.username);
    }

    const logoutUserContext = () => {
        setPizzaCount(0);
        setUsername(null);
        localStorage.removeItem("pizzaCount");
        localStorage.removeItem("username");
        localStorage.removeItem("currentCostumeId");
    };

    const equipCostumeContext = async (itemId) => {
        const currentUsername = localStorage.getItem("username");

        if (!currentUsername) throw new Error("User data missing. Please log in again.");
        
        const result = await equipCostume(currentUsername, itemId);
        
        updateCostumeId(result.current_costume_id);
    };

    return (
        <UserContext.Provider value={
            { pizzaCount, 
            updatePizzaCount, 
            loginUserContext, 
            username, 
            logoutUserContext, 
            currentCostumeId,
            equipCostumeContext
            }}>
            {children}
        </UserContext.Provider>
    );
}

export function useUser() {
    return useContext(UserContext);
}
