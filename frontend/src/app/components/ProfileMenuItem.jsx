import React from "react";
import { useNavigate } from "react-router-dom";

const ProfileMenuItem = ({name, path}) => {
  const navigate = useNavigate();
  return (
    <button onClick={() => navigate(path)}>{name}</button>
  );
};


export default ProfileMenuItem;

