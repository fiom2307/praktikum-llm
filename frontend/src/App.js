import { ToastProvider } from "./context/ToastContext";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"; // Navigate
import LoginPage from "./pages/LoginPage";
import MainPage from "./pages/MainPage";
import ShopPage from "./pages/ShopPage"
import FlashcardsPage from "./pages/FlashcardsPage";
import ReadingPage from "./pages/ReadingPage";
import VocabularyPage from "./pages/VocabularyPage";
import TextProductionPage from "./pages/TextProductionPage";
import RegisterPage from "./pages/RegisterPage";
import CityMenuPage from "./pages/CityMenuPage";
import InventoryPage from "./pages/InventoryPage";
import StoryPage from "./pages/StoryPage";
import FreeModePage from "./pages/FreeModePage";
import FormFloatingGate from "./components/FormFloatingGate";
import AdminPage from "./pages/AdminPage";
import ChangePasswordPage from "./pages/ChangePasswordPage";

const isAdmin = () => {
  return localStorage.getItem("username") === "admin";
};

// check token
const getAuthToken = () => {

    return localStorage.getItem('authToken'); 
};


// protected route
function ProtectedRoute({ children }) {
    
    // check if the Token is valid
    const isAuthenticated = getAuthToken();

    if (!isAuthenticated) {
        // 
        return <Navigate to="/login" replace />; 
    }
    
    // 
    return children; 
}


function App() {

  return (
    <ToastProvider>
      <Router>
        <FormFloatingGate />

        <Routes>
          
          {/* login and register page */}
          <Route path="/login" element={<LoginPage />} />

          <Route path="/register" element={<RegisterPage />} />
          

          {/* protected route */}
          
          <Route path="/" element={
            <ProtectedRoute>
              <MainPage />
            </ProtectedRoute>
          } />

          <Route path="/story" element={
            <ProtectedRoute>
              <StoryPage />
            </ProtectedRoute>
          } />

          <Route path="/free" element={
            <ProtectedRoute>
              <FreeModePage />
            </ProtectedRoute>
          } />

          <Route path="/city/:cityName" element={
            <ProtectedRoute>
              <CityMenuPage />
            </ProtectedRoute>
          } />

          <Route path="/shop" element={
            <ProtectedRoute>
              <ShopPage />
            </ProtectedRoute>
          } />
          
          <Route path="/flashcards" element={
            <ProtectedRoute>
              <FlashcardsPage />
            </ProtectedRoute>
          } />
          
          <Route path="/reading" element={
            <ProtectedRoute>
              <ReadingPage />
            </ProtectedRoute>
          } />
          
          <Route path="/vocabulary" element={
            <ProtectedRoute>
              <VocabularyPage />
            </ProtectedRoute>
          } />
          
          <Route path="/textproduction" element={
            <ProtectedRoute>
              <TextProductionPage />
            </ProtectedRoute>
          } />

          <Route path="/inventory" element={
            <ProtectedRoute>
              <InventoryPage />
            </ProtectedRoute>
          } />

          <Route
            path="/admin"
            element={
              <ProtectedRoute>
                {isAdmin() ? <AdminPage /> : <Navigate to="/" />}
              </ProtectedRoute>
            }
          />

          <Route
            path="/change-password"
            element={
              <ProtectedRoute>
                <ChangePasswordPage />
              </ProtectedRoute>
            }
          />
          
        </Routes>
      </Router>
    </ToastProvider>
  );
}

export default App;