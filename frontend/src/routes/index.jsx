import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import Home from "../pages/Home";
import Insights from "../pages/Insights";
import History from "../pages/History";
import TestHistory from "../pages/TestHistory";
import SimpleHistory from "../pages/SimpleHistory";
import Test from "../pages/Test";
import SimpleTest from "../pages/SimpleTest";
import MinimalTest from "../pages/MinimalTest";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/insights" element={<Insights />} />
          <Route path="/history" element={<History />} />
          <Route path="/test-history" element={<TestHistory />} />
          <Route path="/simple-history" element={<SimpleHistory />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}
