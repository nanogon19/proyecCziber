import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home.tsx"; // Ensure that ./pages/Home.tsx exists, or update the path if necessary

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}