import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"; // <-- 【修复点 1】: 确保这里导入了 Navigate
import LoginPage from "./pages/LoginPage";
import MainPage from "./pages/MainPage";
import ShopPage from "./pages/ShopPage"
import FlashcardsPage from "./pages/FlashcardsPage";
import ReadingPage from "./pages/ReadingPage";
import VocabularyPage from "./pages/VocabularyPage";
import TextProductionPage from "./pages/TextProductionPage";


// 辅助函数：检查认证令牌
const getAuthToken = () => {
    // 从本地存储获取令牌，用于 ProtectedRoute 检查
    return localStorage.getItem('authToken'); 
};


// 辅助组件：受保护的路由
function ProtectedRoute({ children }) {
    
    // 检查用户是否有有效的 Token
    const isAuthenticated = getAuthToken();

    if (!isAuthenticated) {
        // 如果未登录，则重定向到登录页
        return <Navigate to="/login" replace />; 
    }
    
    // 如果已登录，则渲染子组件
    return children; 
}


function App() {
  
  return (
    <Router>
      <Routes>
        
        {/* 1. 登录页: 所有人都可以访问 */}
        <Route path="/login" element={<LoginPage />} />
        

        {/* 2. 受保护的路由: 需要登录才能访问 */}
        
        <Route path="/" element={
          <ProtectedRoute>
            <MainPage />
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
        
      </Routes>
    </Router>
  );
}

export default App;