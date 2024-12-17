import React from "react";
import { useNavigate } from "react-router-dom";
import style from "../../style";

const ProfileMenu = () => {
  const navigate = useNavigate();
  return (
    <div style={style.profileMenu}>
      <button onClick={() => navigate(-1)}>Go back</button>
      <button onClick={() => navigate("/cart")}>Cart</button>
      <div>Profile Menu</div>
    </div>
  );
};

export default ProfileMenu;
