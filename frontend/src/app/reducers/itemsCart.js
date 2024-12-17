import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  data: [],
};

const itemsCartSlice = createSlice({
  name: "itemsCart",
  initialState,
  reducers: {
    setCart(state, action) {
      state.data = action.payload;
      console.log("Items Cart: set:", action.payload);
    },
    addToCart(state, action) {
      state.data.push(action.payload);
      console.log("Items Cart: add:", action.payload);
    },
    removeFromCart(state, action) {
      console.log("Items Cart: remove:", action.payload);
      state.data.filter((value) => {
        return value.uri != action.payload.uri;
      });
    },
  },
});

export const { setCart, addToCart, removeFromCart } = itemsCartSlice.actions;
export default itemsCartSlice.reducer;

export const selectItemsCart = (state) => state.itemsCart.data;
