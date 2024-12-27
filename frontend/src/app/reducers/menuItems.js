import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  data: [
    {
      id: 1,
      name: "Go back",
      path: -1
    },
  ],
};

const menuItemsSlice = createSlice({
  name: "menuItems",
  initialState,
  reducers: {
    setMenuItems(state, action) {
      state.data = initialState.data.concat(action.payload);
    },
    addMenuItems(state, action) {
      state.data.push(...action.payload);
    }
  },
});

export const { setMenuItems, addMenuItems } = menuItemsSlice.actions;
export default menuItemsSlice.reducer;

export const selectMenuItemsData = (state) => state.menuItems.data;

