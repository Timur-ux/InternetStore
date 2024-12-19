import React from "react";
import ProfileMenu from "./ProfileMenu";
import Profile from "./Profile";
import style from "../../style.js"
import {baseMenuItems, userMenuItems, adminMenuItems} from "../../services/menuItems.js"
import { Routes, Route } from "react-router-dom";

const ProfileLine = () => {
  return (
    <div style={{...style.profileLine, ...style.baseBackground}}>
      <Routes>
        <Route path="profile">
          <Route path=":profileName" element={<ProfileMenu menuItems={baseMenuItems.concat(userMenuItems)}/>}/>
        </Route>
      </Routes>
      <Profile />
    </div>
  );
};

export default ProfileLine;
