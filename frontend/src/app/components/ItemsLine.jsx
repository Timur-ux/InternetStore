import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import style from "../../style";
import {
  fetchItems,
  selectAllItems,
  selectItemsStatus,
  selectState,
} from "../reducers/itemsList";
import ItemInfo from "./ItemInfo";

const ItemsLine = () => {
  const dispatch = useDispatch();
  const items = useSelector(selectAllItems);
  const itemsStatus = useSelector(selectItemsStatus);

  useEffect(() => {
    if (itemsStatus === "idle") {
      dispatch(fetchItems());
    }
  }, [itemsStatus, dispatch]);

  const itemsElements = items.map( (item) => <ItemInfo data={item}/>)

  // return <div style={style}>{items.length == 0 ? itemsStatus : itemsElements}</div>;
  return <div style={style}>{itemsElements}</div>;
};

export default ItemsLine;
