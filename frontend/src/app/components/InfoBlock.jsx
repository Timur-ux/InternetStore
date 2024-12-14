import React from "react";
import { Outlet } from "react-router-dom";
import style from "../../style";

const InfoBlock = () => {
  return (
    <div
      style={{ ...style.centeredText, ...style.infoBlock, ...style.baseBackground }}
    >
      Main info placed here
      <br />
      <Outlet/>
    </div>
  );
};

export default InfoBlock;
