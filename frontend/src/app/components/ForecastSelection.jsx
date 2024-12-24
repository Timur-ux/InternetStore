import { React, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { ItemBatchesDriver } from "../../services/ItemBatchesDriver";
import { setBatch } from "../reducers/itemsBatch";
import ItemsBatchLine from "./ItemsBatchLine";
import style from "../../style";
import { selectAllItems, selectItemsStatus, fetchItems } from "../reducers/itemsList";
import { store } from "../store";
import { useSubmit } from "react-router-dom";

const ForecastSelection = () => {
  const dispatch = useDispatch();
  const items = useSelector(selectAllItems);
  const itemsStatus = useSelector(selectItemsStatus);
  var selectedItems = [];
  var unsubscribe = null;

  useEffect(() => {
    if (unsubscribe === null) {
     unsubscribe = store.subscribe(
        () => {
          const batch = store.getState().itemsBatch.data.find((batch) => batch.id == 2);
          if(batch) {
            selectedItems = batch.items;
          }
        }
      );
    }

    if (itemsStatus === "idle") {
      dispatch(fetchItems());
    }

    return () => {
      if (unsubscribe !== null) {
        unsubscribe();
      }
    }
  }, [itemsStatus, dispatch]);
  console.log("Forecast: items:", items);
  
  const onClick_ = () => {
    console.log("On realize i would send these items to forecast: ", selectedItems);
  }
  
  dispatch(setBatch({batchId: 1, items: items}));
  return (
    <div style={style.forecastSelectionMenu}>
      <div>
        <p>Selection panel</p>
        <ItemsBatchLine batchId={1} itemAction={ItemBatchesDriver(1, 2)}/>
        <p>Selected items</p>
        <ItemsBatchLine batchId={2} itemAction={ItemBatchesDriver(2, 1)}/>
      </div>
      <button onClick={onClick_} style={{...style.profileButton, ...style.centered}}>Send</button>
    </div>
  );
}

export default ForecastSelection;
