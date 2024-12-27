import React from "react";
import ProfileMenu from "./ProfileMenu";
import Profile from "./Profile";
import style from "../../style.js"
import { Routes, Route } from "react-router-dom";

const ProfileLine = () => {
  return (
    <div style={{...style.profileLine, ...style.baseBackground}}>
      <ProfileMenu />
      <Profile />
    </div>
  );
};

export default ProfileLine;
