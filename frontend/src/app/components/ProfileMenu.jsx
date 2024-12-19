import React from "react";
import { useNavigate } from "react-router-dom";
import style from "../../style";
import ProfileMenuItem from "./ProfileMenuItem.jsx"

const ProfileMenu = ({menuItems}) => {
  const navigate = useNavigate();
  const buttons = menuItems.map((item) => 
    <ProfileMenuItem name={item.name} path={item.path} />
  );
  return (
    <div style={style.profileMenu}>
      {buttons}
    </div>
  );
};


export default ProfileMenu;
