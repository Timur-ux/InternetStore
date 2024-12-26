from fastapi import APIRouter, HTTPException
from src.services.admin import (
    get_all_users,
    delete_user_by_id,
    get_sales_report,
    get_user_sales,
    # add_user,
)

router = APIRouter()

@router.get("/admin/users")
def list_users():
    """
    Получить список всех пользователей.
    """
    try:
        return get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/admin/users/{user_id}")
def delete_user(user_id: int):
    """
    Удалить пользователя по идентификатору.
    """
    try:
        delete_user_by_id(user_id)
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/sales")
def list_sales():
    """
    Получить отчет по продажам.
    """
    try:
        return get_sales_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/sales/{user_id}")
def user_sales(user_id: int):
    """
    Получить продажи по пользователю.
    """
    try:
        return get_user_sales(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.post("/admin/users")
# def create_new_user(login: str, password: str, access_level: int):
#     """
#     Создать нового пользователя.
#     """
#     try:
#         user = add_user(login, password, access_level)
#         return {"message": "User created successfully", "user_id": user.id}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
