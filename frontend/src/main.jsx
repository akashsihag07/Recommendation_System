import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

// styles are split by area so each file is easy to find and skim
import "./styles/theme.css";
import "./styles/layout.css";
import "./styles/form.css";
import "./styles/cards.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
