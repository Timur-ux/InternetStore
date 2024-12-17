import React from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import style from "../../style";
import { selectItemsCart } from "../reducers/itemsCart";

const CartInfo = () => {
  const navigate = useNavigate();
  const items = useSelector(selectItemsCart);
  console.log("Cart Info: items:", items);

  const navigateTo = item => () => {
    console.log("Cart Info: navigateTo: item:", item);
    navigate("/item", {state: item});
  }
  const itemsElement = items.map((item) => (
    <li>
      <a onClick={navigateTo(item)}>{item.title}</a>
    </li>
  ));

  const onBuyClicked = () => {
    // TODO buy processing
    console.log("Buy processing, really... no");
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
