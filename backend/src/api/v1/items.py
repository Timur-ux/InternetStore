from fastapi import APIRouter, Depends, HTTPException, Query
from src.db.requests import get_items, get_item_by_id, get_items_by_uris, add_purchase, log_user_action
from src.models import BuyRequest
from src.dependencies import authenticate_user
from src.db.sessionManager import SessionManager

router = APIRouter()

@router.get("/items", dependencies=[Depends(authenticate_user)])
def list_items():
    return {"items": get_items(SessionManager)}

@router.get("/item")
def get_item(id: int = Query(...), user=Depends(authenticate_user)):
    item = get_item_by_id(SessionManager, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"data": item}

@router.post("/buy")
def buy(item_uris: BuyRequest, user=Depends(authenticate_user)):
    user_id = user["user_id"]
    items = get_items_by_uris(SessionManager, item_uris.item_uris)
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")
    total_price = sum(item["price"] * item_uris.item_uris.count(str(item["id"])) for item in items)
    for item in items:
        add_purchase(SessionManager, user_id, item["id"], item["price"], item_uris.item_uris.count(str(item["id"])))
    log_user_action(SessionManager, user_id, f"Purchased items: {item_uris.item_uris}")
    return {"message": "Purchase successful", "total_price": total_price}
