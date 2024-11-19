import React from 'react';
import './App.css';  // Optional: If you have a global CSS file for your app
import { LoginForm } from './Login/LoginForm';  // Import LoginForm component

function App() {
  return (
    <div className="App">
      <LoginForm />  {/* Render the LoginForm component */}
    </div>
  );
}

export default App;