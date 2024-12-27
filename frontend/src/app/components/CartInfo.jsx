import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { BuyProcess } from "../../services/BuyProcess";
import { DoRemoveFromCart } from "../../services/DoRemoveFromCart";
import style from "../../style";
import { selectAuthData } from "../reducers/authData";
import { removeFromCart, selectItemsCart } from "../reducers/itemsCart";
import { store } from "../store";

const CartInfo = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  var items = useSelector(selectItemsCart);
  const token = useSelector(selectAuthData).token;

  useEffect(() => {
    const unsubscribe = store.subscribe(() => {
      items = store.getState().itemsCart.data;
    });

    return () => unsubscribe();
  }, [])

  const navigateTo = item => () => {
    navigate("/item", {state: item});
  }
  const itemsElement = items.map((item) => (
    <li style={{width: "100%"}}>
    <div style={style.cartItemStyle}>
      <a style={{marginRight: "100%"}}onClick={navigateTo(item)}>{item.title}</a>
      <button style={{marginLeft: "100%"}} onClick={() => DoRemoveFromCart(dispatch, item.id)}>Remove</button>
    </div>
    </li>
  ));

  const onBuyClicked = async () => {
    console.log("Processing buying next items: ", items);
    await BuyProcess(items, token, dispatch);
  }

  return (<div style={style.cartInfo}>
    <ul>
    {itemsElement}
    </ul>
    <button onClick={onBuyClicked}>
      Buy
    </button>
  </div>)
};

export default CartInfo;
