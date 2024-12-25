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

    },
    addToBatch(state, action) {
      const {batchId, items} = action.payload;
      const existingBatch = state.data.find((batch) => batch.id === batchId);
      if (existingBatch) {
        for (let i = 0, len = items.length; i < len; i++) {
          existingBatch.items.push(items[i]);
        }
      }
      else {
        state.data.push({id: batchId, items: items});
      }
    },
    removeFromBatch(state, action) {
      const {batchId, itemId} = action.payload;
      const existingBatch = state.data.find((batch) => batch.id === batchId);
      if (existingBatch) {
        existingBatch.items = existingBatch.items.filter((value) => {
          return value.id != itemId;
        });
      }
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
