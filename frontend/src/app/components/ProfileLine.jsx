import React from "react";
import ProfileMenu from "./ProfileMenu";
import Profile from "./Profile";
import style from "../../style.js"

const ProfileLine = () => {
  return (
    <div style={{...style.profileLine, ...style.baseBackground}}>
      <ProfileMenu />
      <Profile />
    </div>
  );
};

export default ProfileLine;
