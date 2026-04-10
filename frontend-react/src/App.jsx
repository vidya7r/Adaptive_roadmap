import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ExamProvider } from './context/ExamContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';
import { DashboardPage } from './pages/DashboardPage';
import { ExamSelectionPage } from './pages/ExamSelectionPage';
import { ModulesPage } from './pages/ModulesPage';
import { TopicsPage } from './pages/TopicsPage';
import { SubtopicDetailsPage } from './pages/SubtopicDetailsPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ExamProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />

            <Route
              path="/exam-selection"
              element={
                <ProtectedRoute>
                  <ExamSelectionPage />
                </ProtectedRoute>
              }
            />

            <Route
              path="/modules"
              element={
                <ProtectedRoute>
                  <ModulesPage />
                </ProtectedRoute>
              }
            />

            <Route
              path="/topics"
              element={
                <ProtectedRoute>
                  <TopicsPage />
                </ProtectedRoute>
              }
            />

            <Route
              path="/subtopic-details"
              element={
                <ProtectedRoute>
                  <SubtopicDetailsPage />
                </ProtectedRoute>
              }
            />

            <Route
              path="/analytics"
              element={
                <ProtectedRoute>
                  <AnalyticsPage />
                </ProtectedRoute>
              }
            />

            {/* Redirect to dashboard for authenticated users, login for others */}
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="*" element={<Navigate to="/dashboard" />} />
          </Routes>
        </ExamProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;


