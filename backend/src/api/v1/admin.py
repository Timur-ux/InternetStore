from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from src.db.requests import get_user_actions, get_selled_items, get_recommendations
from src.dependencies import authenticate_user
from src.db.sessionManager import SessionManager

router = APIRouter()

@router.get("/history")
def history(time: str = None, user=Depends(authenticate_user)):
    if user["access_level"] < 2:
        raise HTTPException(status_code=403, detail="Permission denied")
    start_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S") if time else datetime.now() - timedelta(days=1)
    actions = get_user_actions(SessionManager, start_time)
    return {"actions": actions}

@router.get("/selled")
def selled(time: str = None, user=Depends(authenticate_user)):
    if user["access_level"] < 2:
        raise HTTPException(status_code=403, detail="Permission denied")
    start_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S") if time else datetime.now() - timedelta(days=1)
    selled_items = get_selled_items(SessionManager, start_time)
    return {"selled_items": selled_items}

@router.get("/recommendation")
def recommendation(n: int = Query(1, ge=1), user=Depends(authenticate_user)):
    recommendations = get_recommendations(SessionManager, user["user_id"], n)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return {"recommendations": recommendations}
