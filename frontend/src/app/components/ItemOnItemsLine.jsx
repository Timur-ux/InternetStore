import React from "react";
import { useNavigate } from "react-router-dom";
import style from "../../style";

const ItemOnItemsLine = ({ title = "None", uri, description = "" }) => {
  const navigate = useNavigate();
  const onCLickButton = () =>
    navigate("/item", { state: { title, uri, description } });

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
