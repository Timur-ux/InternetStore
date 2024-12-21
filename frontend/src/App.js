import "./App.css";
import style from "./style.js";
import { Routes, Route } from "react-router-dom";

import Title from "./app/components/Title.jsx";
import ProfileLine from "./app/components/ProfileLine.jsx";
import InfoBlock from "./app/components/InfoBlock.jsx";
import Footer from "./app/components/Footer.jsx";
import ItemsLine from "./app/components/ItemsLine";
import ItemInfo from "./app/components/ItemInfo";
import Auth from "./app/components/Auth";
import Register from "./app/components/Register";
import CartInfo from "./app/components/CartInfo";

const App = () => {
  return (
    <div style={style.mainBlock}>
      <Title />
      <ProfileLine />
      <Routes>
        <Route path="/" element={<InfoBlock />}>
          <Route path="/" element={<ItemsLine />} />
          <Route path="item" element={<ItemInfo />} />
        </Route>
        <Route path="/auth" element={<Auth />}></Route>
        <Route path="/register" element={<Register />}></Route>
        <Route path="/cart" element={<CartInfo />}></Route>
      </Routes>
      <Footer />
    </div>
  );
};

export default App;
