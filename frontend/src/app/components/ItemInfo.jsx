import React, { useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import style from "../../style";

const ItemInfo = ({data = null}) => {
  const state = useLocation().state;
  var title = ""
  if(data === null) {
    title = state !== null ? (state.title !== null ? state.title : "None") : "None" 
  } else {
    title = data !== null ? (data.title === null ? title : data.title) : "None";
  }
  return (<div style={style.itemInfo}>item info(title = {title}) </div>);
}

export default ItemInfo;
