import { React, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { ItemBatchesDriver } from "../../services/ItemBatchesDriver";
import { setBatch } from "../reducers/itemsBatch";
import ItemsBatchLine from "./ItemsBatchLine";
import style from "../../style";
import {
  selectAllItems,
  selectItemsStatus,
  fetchItems,
} from "../reducers/itemsList";
import { store } from "../store";
import { doForecast } from "../../services/doForecast";
import { selectAuthData } from "../reducers/authData";
import { Outlet, useNavigate } from "react-router-dom";

const ForecastSelection = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const items = useSelector(selectAllItems);
  const itemsStatus = useSelector(selectItemsStatus);
  const token = useSelector(selectAuthData).token;
  var selectedItems = [];
  var unsubscribe = null;

  useEffect(() => {
    console.log("subscribing");
    if (unsubscribe === null) {
      unsubscribe = store.subscribe(() => {
        const batch = store
          .getState()
          .itemsBatch.data.find((batch) => batch.id == 2);
        console.log("ForecastSelection: batch: ", batch);
        if (batch) {
          selectedItems = batch.items;
        }
      });
    }

    if (itemsStatus === "idle") {
      dispatch(fetchItems());
    }

    return () => {
      if (unsubscribe !== null) {
        unsubscribe();
      }
    };
  }, [itemsStatus]);

  const onClick_ = async () => {
    console.log("Forecast on selected items: ", selectedItems);
    const response = await doForecast(selectedItems, token);
    navigate("result", {state: {
      forecast: response.data.forecast
    }});
  };

  dispatch(setBatch({ batchId: 1, items: items }));
  return (
    <div style={style.forecastSelectionMenu}>
      <div>
        <p>Selection panel</p>
        <ItemsBatchLine batchId={1} itemAction={ItemBatchesDriver(1, 2)} />
        <p>Selected items</p>
        <ItemsBatchLine batchId={2} itemAction={ItemBatchesDriver(2, 1)} />
      </div>
      <button
        onClick={onClick_}
        style={{ ...style.profileButton, ...style.centered }}
      >
        Send
      </button>
      <br />
      <Outlet />
    </div>
  );
};

export default ForecastSelection;
