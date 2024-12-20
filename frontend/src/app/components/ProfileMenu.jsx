import React from "react";
import { useParams } from "react-router-dom";
import { baseMenuItems, profileMenuItems } from "../../services/menuItems";
import style from "../../style";
import ProfileMenuItem from "./ProfileMenuItem.jsx"

const ProfileMenu = ({useProfile}) => {
  const params = useParams();

  var items = baseMenuItems;
  if(useProfile) {
    const {profileName} = params;
    items = items.concat(profileMenuItems[profileName]);
  }

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
