import React from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import style from "../../style";

const ItemOnItemsLine = ({id, title = "None", uri, description = "" , onClickAction = null}) => {
  const navigate = useNavigate();
  const dispatch = useDispatch()
  const onCLickButton = () => {
    if(onClickAction === null)
      navigate("/item", { state: {id, title, uri, description } });
    else {
      onClickAction({id, title, uri, description}, dispatch);
    }
  }

  return (
    <div style={style.itemOnItemsLine}>
      <button onClick={onCLickButton}>
        <p>{title}</p>
        <p>{description}</p>
      </button>
    </div>
  );
};

export const ItemOnItemsBatchLine = ({ title = "None", uri, description = "" , action}) => {
  const onCLickButton = () =>
    action({title, uri, description});

  return (
    <div style={style.itemOnItemsLine}>
      <button onClick={onCLickButton}>
        <p>{title}</p>
        <p>{description}</p>
      </button>
    </div>
  );
};

export default ItemOnItemsLine;
