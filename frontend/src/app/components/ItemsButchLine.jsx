import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import style from "../../style";
import ItemOnItemsLine from "./ItemOnItemsLine";
import { store } from "../store";

const ItemsButchLine = ({batchId}) => {
  var items = [];

  useEffect(() => {
    const unsubscribe = store.subscribe(
      () => {
        const butch = store.getState().itemsBatch.data.find((batch) => batch.id === batchId);
        if (butch) {
          items = butch.items;
        }
      }
    );

    return () => unsubscribe();

  }, []);

  const itemsElements = items.map( (item) => <ItemOnItemsLine {...item}/>)

  // return <div style={style}>{items.length == 0 ? itemsStatus : itemsElements}</div>;
  return <div style={style.itemsLine}>{itemsElements}</div>;
};

export default ItemsButchLine;

