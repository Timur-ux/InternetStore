import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import client, { doRequest, RequestType } from "../../services/client";

// TODO: clear list due to user logout via extraReducers

export const fetchItems = createAsyncThunk(
  "items/fetchItems",
  async () => {
    const response = await doRequest({type: RequestType.get, uri: "/items"});
    return response.data;
  },
  {
    condition(arg, thunkApi) {
      const itemsStatus = selectItemsStatus(thunkApi.getState());
      if (itemsStatus !== "idle") {
        return false;
      }
    },
  },
);

const initialState = {
  // data: [] // Default
  data: [{id: 1, title: "item1", uri: "/item/1", description: "Some description about item 1", price: "261$"}, {id: 2, title: "item2", uri: "/item/2", description: "Some description about item 2", price: "100$"}], // for tests purposes
  status: "idle",
  error: null,
};

const itemsSlice = createSlice({
  name: "items",
  initialState,
  reducers: {
    itemAdded(state, action) {
      state.data.push(action.payload);
    },
    itemUpdated(state, action) {
      const { id, title, uri, description } = action.payload;
      const existingItem = state.data.find((item) => item.id === id);
      if (existingItem) {
        existingItem.title = title;
        existingItem.uri = uri;
        existingItem.description = description;
      }
    },
    itemRemoved(state, action) {
      const { id } = action.payload;
      state.data = state.data.filter((item) => item.id !== id);
    },
  },
  extraReducers: (builder) =>
    builder
      .addCase(fetchItems.pending, (state, action) => {
        state.status = "pending";
      })
      .addCase(fetchItems.fulfilled, (state, action) => {
        state.status = "succeeded";
        console.log("ItemsSlice: recieved items: ", action.payload);
        state.data.push(...action.payload.items);
      })
      .addCase(fetchItems.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message ?? "Unknown Error";
      }),
});

export const { itemAdded, itemUpdated, itemRemoved } = itemsSlice.actions;
export default itemsSlice.reducer;

export const selectState = (state) => state;
export const selectAllItems = (state) => state.items.data;
export const selectItemById = (state, id) =>
  state.items.data.find((item) => item.id === id);

export const selectItemsState = (state) => state;
export const selectItemsStatus = (state) => state.items.status;
export const selectItemsError = (state) => state.items.error;
