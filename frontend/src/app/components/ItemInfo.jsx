import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useLocation, useParams } from "react-router-dom";
import style from "../../style";
import { addToCart } from "../reducers/itemsCart";

const ItemInfo = () => {
  const dispatch = useDispatch();
  console.log("Item Info: state:", useLocation().state);

  const { title, uri, description } = useLocation().state;

  const onClickButton = () => {
    dispatch(addToCart({ title, uri, description }));
  };

  return (
    <div style={style.itemInfo}>
      <p>{title}</p>
      <p>{description}</p>
      <button onClick={onClickButton}>Add to cart</button>
    </div>
  );
};

export default ItemInfo;
