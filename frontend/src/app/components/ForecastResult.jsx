import React from "react";
import { useSelector } from "react-redux";
import { useLocation } from "react-router-dom";
import { selectAllItems } from "../reducers/itemsList";

const ForecastResult = () => {
  const state = useLocation().state;
  const items = useSelector(selectAllItems);

  const curItems = state.forecast.forecast;
  console.log("ForecastResult: curItems:", curItems);
  const listItems = curItems.map((item) => {
    return (
      <tr>
        <td>{items.find((item_) => item_.uri === item.uri).title}</td>
        <td>{item.forecast}</td>
      </tr>
    );
  });

  return (
    <div>
      Результат:
      <br />
      <table
        style={{
          width: "100%",
          border: "1px solid black",
          textAlign: "center",
        }}
      >
        <tr style={{border: "1px solid black"}}>
          <td>Name</td>
          <td>Forecast</td>
        </tr>
        {listItems}
      </table>
    </div>
  );
};

export default ForecastResult;
