import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { initTheme } from "./utils/theme";
import "./styles/tailwind.css";
import App from './App.jsx'
initTheme();

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
