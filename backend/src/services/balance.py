from yookassa import Configuration, Payment
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User

# Настройка SDK ЮKassa
Configuration.account_id = "<your_account_id>"
Configuration.secret_key = "<your_secret_key>"

async def get_user_balance(session: AsyncSession, user_id: int) -> float:
    user = await session.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    return user.balance

async def top_up_balance(user_id: int, amount: float) -> str:
    """
    Создание платежа в ЮKassa и возврат ссылки для оплаты.
    """
    payment = Payment.create({
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://localhost:8000/payment/success"
        },
        "description": f"Пополнение баланса пользователя {user_id}"
    })
    return payment.confirmation.confirmation_url
