import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import App from "./App.tsx";
import TradeCalculator from "./pages/TradeCalculator.tsx";
import LeagueImport from "./pages/LeagueImport.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/trade" element={<TradeCalculator />} />
        <Route path="/league" element={<LeagueImport />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);