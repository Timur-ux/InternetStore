import "./App.css";
import style from "./style.js";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Title from "./app/components/Title.jsx";
import ProfileLine from "./app/components/ProfileLine.jsx";
import InfoBlock from "./app/components/InfoBlock.jsx";
import Footer from "./app/components/Footer.jsx";

const App = () => {
  return (
    <div style={style.mainBlock}>
      <Title />
      <ProfileLine />
      <InfoBlock />
      <Footer />
    </div>
  );
};

export default App;
