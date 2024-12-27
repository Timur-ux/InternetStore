import { addToBatch, removeFromBatch } from "../app/reducers/itemsBatch"

export const ItemBatchesDriver = (batchIdFrom, batchIdTo) => (itemData, dispatch) => {
  dispatch(removeFromBatch({batchId: batchIdFrom, itemId: itemData.id}));
  dispatch(addToBatch({batchId: batchIdTo, items: [itemData]}));
}
