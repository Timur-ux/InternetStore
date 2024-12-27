import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import client, { doRequest, RequestType } from "../../services/client";

export const fetchItemData = createAsyncThunk(
  "item/fetchItemData",
  async (item_id) => {
    const response = await doRequest({type: RequestType.get, uri: "/item", params: { item_id: item_id },});
    return response.data;
  },
  {
    condition(arg, thunkApi) {
      const itemStatus = selectItemStatus(thunkApi.getState());
      if (itemStatus !== "idle") {
        return false;
      }
    },
  },
);

const initialState = {
  data: { title: "", uri: "", content: {} },
  status: "idle",
  error: null,
};

const itemSlice = createSlice({
  name: "item",
  initialState,
  reducers: {
    itemSet(state, action) {
      state.title = action.payload.title;
      state.uri = action.payload.uri;
      state.content = action.payload.content;
    },
  },
  extraReducers: (builder) =>
    builder
      .addCase(fetchItemData.pending, (state, action) => {
        state.status = "pending";
      })
      .addCase(fetchItemData.fulfilled, (state, action) => {
        state.status = "succeeded";
      })
      .addCase(fetchItemData.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message ?? "Unknown Error";
      }),
});

export const { itemSet } = itemSlice.actions;
export default itemSlice.reducer;

export const selectItem = (state) => state.item.data;

export const selectItemStatus = (state) => state.item.status;
export const selectItemError = (state) => state.item.error;
