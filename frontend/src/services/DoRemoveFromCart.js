import { removeFromCart } from "../app/reducers/itemsCart"

export const DoRemoveFromCart = (dispatch, itemId) => {
  dispatch(removeFromCart({itemId}));
}
