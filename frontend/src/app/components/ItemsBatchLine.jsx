import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import style from "../../style";
import ItemOnItemsLine from "./ItemOnItemsLine";
import { store } from "../store";
import { selectItemsBatch } from "../reducers/itemsBatch";

const ItemsBatchLine = ({batchId, itemAction}) => {
  var items = useSelector(selectItemsBatch(batchId));
  if (items === undefined) {
    items = [];
  }
  else{
    items = items.items;
  }
  console.log("ItemsBatchLine", batchId, ": items:", items);

  useEffect(() => {
    const unsubscribe = store.subscribe(
      () => {
        console.log("H:", batchId);
        const batch = store.getState().itemsBatch.data.find((batch) => batch.id === batchId);
        if (batch) {
          items = batch.items;
          console.log("H:", batchId, "items: ", items);
        }
      }
    );

    return () => unsubscribe();

  }, []);

  const itemsElements = items.map((item) => {
    const props = {onClickAction: itemAction, ...item};
    return <ItemOnItemsLine {...props }/>;
  })


  return <div style={style.itemsLine}>{itemsElements}</div>;
};

export default ItemsBatchLine;

