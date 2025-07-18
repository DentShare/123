# dentshare_bot/models.py

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Boolean, Text, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from dentshare_bot.database import Base

class UserRole(str):
    DENTIST = "dentist"
    TECHNICIAN = "technician"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)
    fio = Column(String, nullable=False)
    phone_main = Column(String, nullable=False)
    phone_extra = Column(String)
    clinic_lab_name = Column(String)
    address = Column(String)
    tg_user_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    admin_key = Column(String, nullable=True)

    # Стоматолог — заказы как заказчик
    orders = relationship("Order", back_populates="dentist", foreign_keys="Order.dentist_id")

    # Техник — его лаборатории
    labs = relationship("Lab", back_populates="technician")

    # Техник — связь с UserLab (сотрудничества)
    user_labs = relationship("UserLab", back_populates="dentist", foreign_keys="UserLab.dentist_id")

class Lab(Base):
    __tablename__ = "lab"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    technician_id = Column(Integer, ForeignKey("user.id"))
    # связь с User (техник)
    technician = relationship("User", back_populates="labs")
    # заказы для этой лаборатории
    orders = relationship("Order", back_populates="lab")

class Clinic(Base):
    __tablename__ = "clinic"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    dentist_id = Column(Integer, ForeignKey("user.id"))

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    order_uid = Column(String, unique=True)
    dentist_id = Column(Integer, ForeignKey("user.id"))
    lab_id = Column(Integer, ForeignKey("lab.id"))
    status = Column(String, default="new")
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    dentist = relationship("User", foreign_keys=[dentist_id], back_populates="orders")
    lab = relationship("Lab", foreign_keys=[lab_id], back_populates="orders")
    positions = relationship("OrderPosition", back_populates="order")
    files = relationship("File", back_populates="order")

class OrderPosition(Base):
    __tablename__ = "order_position"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    construction_type = Column(String)
    place_type = Column(String)
    material = Column(String)
    color = Column(String)
    teeth_numbers = Column(JSON)
    order = relationship("Order", back_populates="positions")

class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    file_type = Column(String)
    file_path = Column(String)
    file_name = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    order = relationship("Order", back_populates="files")

class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    status = Column(String)
    changed_at = Column(DateTime, default=datetime.utcnow)
    changed_by_user_id = Column(Integer, ForeignKey("user.id"))

class OrderComment(Base):
    __tablename__ = "order_comment"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserLab(Base):
    __tablename__ = "user_lab"
    id = Column(Integer, primary_key=True)
    dentist_id = Column(Integer, ForeignKey("user.id"))
    lab_id = Column(Integer, ForeignKey("lab.id"))
    confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    dentist = relationship("User", back_populates="user_labs", foreign_keys=[dentist_id])
    lab = relationship("Lab")

class Cabinet(Base):
    __tablename__ = "cabinet"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    cabinet_type = Column(String)
    menu_function = Column(JSON)
