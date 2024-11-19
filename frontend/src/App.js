import React from 'react';
import './App.css';  // Optional: If you have a global CSS file for your app
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { LoginForm } from './Login/LoginForm';  // Import LoginForm component
import { SignupForm } from './Signup/SignupForm';  // Import SignupForm component

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LoginForm />} />
          <Route path="/signup" element={<SignupForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
