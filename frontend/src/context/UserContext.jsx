import { createContext, useContext, useState, useEffect } from "react";
import { equipCostume, markTutorialSeenApi } from '../api/userApi';

const UserContext = createContext();

export function UserProvider({ children }) {
    const [pizzaCount, setPizzaCount] = useState(0);
    const [username, setUsername] = useState(null);
    const [currentCostumeId, setCurrentCostumeId] = useState(0);
    const [tutorialProgress, setTutorialProgress] = useState(() => {
        const saved = localStorage.getItem("tutorialProgress");
        try {
            return saved ? JSON.parse(saved) : { reading: false, vocabulary: false, writing: false };
        } catch {
            return { reading: false, vocabulary: false, writing: false };
        }
    });

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
        
        if (user.tutorial_progress) {
            console.log("Saving Progress to Context:", user.tutorial_progress);
            setTutorialProgress(user.tutorial_progress);
            localStorage.setItem("tutorialProgress", JSON.stringify(user.tutorial_progress));
        }
    }

    const completeTutorialContext = async (taskType) => {
        const currentUsername = localStorage.getItem("username");
        if (!currentUsername) return;
        try {

            await markTutorialSeenApi(currentUsername, taskType);
            
            const newProgress = { ...tutorialProgress, [taskType]: true };
            setTutorialProgress(newProgress);
            localStorage.setItem("tutorialProgress", JSON.stringify(newProgress));
        } catch (err) {
            console.error("Failed to update tutorial status", err);
        }
    };

    const logoutUserContext = () => {
        setPizzaCount(0);
        setUsername(null);
        localStorage.removeItem("pizzaCount");
        localStorage.removeItem("username");
        localStorage.removeItem("currentCostumeId");
        setTutorialProgress({ reading: false, vocabulary: false, writing: false });
        localStorage.removeItem("tutorialProgress");
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
            equipCostumeContext, 
            tutorialProgress, 
            completeTutorialContext
            }}>
            {children}
        </UserContext.Provider>
    );
}

export function useUser() {
    return useContext(UserContext);
}
