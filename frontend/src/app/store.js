import { configureStore } from "@reduxjs/toolkit";
import items from "./reducers/itemsList.js";
import item from "./reducers/itemInfo.js";
import authData from "./reducers/authData.js";
import itemsCart from "./reducers/itemsCart.js";
import menuItems from "./reducers/menuItems.js"
import itemsBatch from "./reducers/itemsBatch.js";

export const store = configureStore({
  reducer: {
    items,
    item,
    authData,
    itemsCart,
    menuItems,
    itemsBatch,
  },
});
