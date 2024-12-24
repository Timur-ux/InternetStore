import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  data: [],
};

const itemsBatchSlice = createSlice({
  name: "itemsBatch",
  initialState,
  reducers: {
    setBatch(state, action) {
      const {batchId, items} = action.payload;
      const existingBatch = state.data.find((batch) => batch.id === batchId);
      if (existingBatch) {
        existingBatch.items = items;
      } else {
        state.data.push({id: batchId, items: items});
      }

      console.log("Items Batch:", batchId, ": set:", action.payload);
    },
    addToBatch(state, action) {
      const {batchId, items} = action.payload;
      const existingBatch = state.data.find((batch) => batch.id === batchId);
      if (existingBatch) {
        console.log("Items batch: add: found");
        for (let i = 0, len = items.length; i < len; i++) {
          existingBatch.items.push(items[i]);
        }
      }
      else {
        console.log("Items batch: add: not found, creating:", {batchId, items});
        state.data.push({id: batchId, items: items});
      }
      console.log("Items Batch:", batchId, ": add:", action.payload);
    },
    removeFromBatch(state, action) {
      const {batchId, itemId} = action.payload;
      const existingBatch = state.data.find((batch) => batch.id === batchId);
      if (existingBatch) {
        existingBatch.items = existingBatch.items.filter((value) => {
          return value.id != itemId;
        });
      }
      console.log("Items Batch:", batchId, ": remove:", action.payload);
    },
  }
});

export const { setBatch, addToBatch, removeFromBatch } = itemsBatchSlice.actions;
export default itemsBatchSlice.reducer;

export const selectItemsBatch = (batchId) => (state) => state.itemsBatch.data.find((batch) => batch.id === batchId);

export const selectItemFromBatch = (batchId, itemId) => (state) => {
  const existingBatch = state.itemsBatch.find((batch) => batch.id == batchId);
  if(existingBatch)
    return existingBatch.find((item) => item.id == itemId);
  return null;
}
