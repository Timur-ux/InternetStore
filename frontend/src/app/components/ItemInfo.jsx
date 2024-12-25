import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useLocation, useParams } from "react-router-dom";
import style from "../../style";
import { addToCart } from "../reducers/itemsCart";

const ItemInfo = () => {
  const dispatch = useDispatch();
  console.log("Item Info: state:", useLocation().state);

  const data = useLocation().state;
  const {id, title, uri, description, price } = data;

  const onClickButton = () => {
    dispatch(addToCart(data));
  };

  return (
    <div style={style.itemInfo}>
      <p>Title: {title}</p>
      <p>Description: {description}</p>
      <p> Price: {price} </p>
      <button onClick={onClickButton}>Add to cart</button>
    </div>
  );
};

export default ItemInfo;
