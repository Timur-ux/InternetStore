import { configureStore } from "@reduxjs/toolkit";
import items from "./reducers/itemsList.js";
import item from "./reducers/itemInfo.js";
import authData from "./reducers/authData.js";

export const store = configureStore({
  reducer: {
    items,
    item,
    authData,
  },
});
