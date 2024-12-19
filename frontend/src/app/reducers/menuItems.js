import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  data: [],
};

const menuItemsSlice = createSlice({
  name: "menuItems",
  initialState,
  reducers: {
    setMenuItems(state, action) {
      state.data = action.payload;
    },
  },
});

export const { setMenuItems} = menuItemsSlice.actions;
export default menuItemsSlice.reducer;

export const selectMenuItemsData = (state) => state.menuItems.data;

