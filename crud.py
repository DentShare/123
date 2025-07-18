# app/crud.py
from sqlalchemy import select, update
from dentshare_bot.models import User, Order, Lab, UserLab
from dentshare_bot.database import async_session

async def get_user_by_tg_id(tg_user_id: str):
    async with async_session() as session:
        q = await session.execute(select(User).where(User.tg_user_id == tg_user_id))
        return q.scalar_one_or_none()

async def get_user_by_id(user_id: int):
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == user_id))
        return q.scalar_one_or_none()

async def create_order(order_dict):
    async with async_session() as session:
        order = Order(**order_dict)
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order

async def get_orders_by_dentist(dentist_id: int):
    async with async_session() as session:
        q = await session.execute(select(Order).where(Order.dentist_id == dentist_id))
        return q.scalars().all()

async def get_orders_by_technician(technician_id: int):
    async with async_session() as session:
        # lab_id — это лаборатория, где работает техник (или фильтруй по user_lab)
        q = await session.execute(select(Order).where(Order.lab_id == technician_id))
        return q.scalars().all()

async def get_lab_by_id(lab_id: int):
    async with async_session() as session:
        q = await session.execute(select(Lab).where(Lab.id == lab_id))
        return q.scalar_one_or_none()

async def add_lab(dentist_id: int, lab_id: int):
    async with async_session() as session:
        user_lab = UserLab(dentist_id=dentist_id, lab_id=lab_id)
        session.add(user_lab)
        await session.commit()
        await session.refresh(user_lab)
        return user_lab

async def confirm_lab_collaboration(user_lab_id: int):
    async with async_session() as session:
        await session.execute(update(UserLab).where(UserLab.id == user_lab_id).values(confirmed=True))
        await session.commit()
