import React from "react";
import { useSelector } from "react-redux";
import style from "../../style";
import { selectMenuItemsData } from "../reducers/menuItems";
import ProfileMenuItem from "./ProfileMenuItem.jsx"

const ProfileMenu = () => {
  const items = useSelector(selectMenuItemsData);
  console.log(items);

  const buttons = items.map((item) =>
    <ProfileMenuItem name={item.name} path={item.path} />
  );

  return (
    <div style={style.profileMenu}>
      {buttons}
    </div>
  );
};


export default ProfileMenu;
