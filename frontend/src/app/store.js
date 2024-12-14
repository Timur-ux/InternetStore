import { applyMiddleware, configureStore } from "@reduxjs/toolkit";
import { thunk } from "redux-thunk";

export const store = configureStore({
  reducer: {},
}, applyMiddleware(thunk));
