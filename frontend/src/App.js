import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import MainPage from "./pages/MainPage";
import ShopPage from "./pages/ShopPage"
import FlashcardsPage from "./pages/FlashcardsPage";
import ReadingPage from "./pages/ReadingPage";
import VocabularyPage from "./pages/VocabularyPage";
import TextProductionPage from "./pages/TextProductionPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/shop" element={<ShopPage />} />
        <Route path="/flashcards" element={<FlashcardsPage />} />
        <Route path="/reading" element={<ReadingPage />} />
        <Route path="/vocabulary" element={<VocabularyPage />} />
        <Route path="/textproduction" element={<TextProductionPage />} />
      </Routes>
    </Router>
  );
}

export default App;