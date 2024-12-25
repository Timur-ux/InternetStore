import React from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import style from "../../style";

const ItemOnItemsLine = ({id, title = "None", uri, description = "" , price = null, onClickAction = null}) => {
  const navigate = useNavigate();
  const dispatch = useDispatch()
  const onCLickButton = () => {
    if(onClickAction === null)
      navigate("/item", { state: {id, title, uri, price, description } });
    else {
      onClickAction({id, title, uri, price, description}, dispatch);
    }
  }

  return (
    <div style={style.itemOnItemsLine}>
      <button onClick={onCLickButton}>
        <p>Title: {title}</p>
        <p>Description: {description}</p>
        <p>Price: {price == null ? "" : price}</p>
      </button>
    </div>
  );
};

export default ItemOnItemsLine;
