import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Crossword from "./pages/Crossword";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/crossword" element={<Crossword />} />
      </Routes>
    </Router>
  );
}

export default App;