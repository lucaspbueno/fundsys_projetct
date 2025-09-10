import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import Home from "../pages/Home";
import Insights from "../pages/Insights";
import History from "../pages/History";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/insights" element={<Insights />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}
