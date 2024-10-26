from typing import List, Optional
from sqlalchemy.orm import Session
from .db import Cart, Item, ItemInCart
from .models import Cart as CartSchema, Item as ItemSchema, ItemInCart as ItemInCartSchema, ItemPut


def get_item(db: Session, item_id: int) -> Optional[ItemSchema]:
    item = db.query(Item).filter(Item.id == item_id, Item.deleted == False).first()
    return ItemSchema.from_orm(item) if item else None


def get_items(db: Session, offset: int, limit: int, min_price: Optional[float], max_price: Optional[float], show_deleted: bool) -> List[ItemSchema]:
    query = db.query(Item)
    if not show_deleted:
        query = query.filter(Item.deleted == False)
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    items = query.offset(offset).limit(limit).all()
    return [ItemSchema.from_orm(item) for item in items]


def add_item(db: Session, item_data: dict) -> ItemSchema:
    item = Item(**item_data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return ItemSchema.from_orm(item)


def change_item(db: Session, item_id: int, new_data: ItemPut) -> ItemSchema:
    item = db.query(Item).filter(Item.id == item_id, Item.deleted == False).first()
    if not item:
        raise ValueError(f"Item {item_id} not found.")
    item.name = new_data.name
    item.price = new_data.price
    item.deleted = new_data.deleted
    db.commit()
    db.refresh(item)
    return ItemSchema.from_orm(item)


def modify_item(db: Session, item_id: int, new_name: Optional[str] = None, new_price: Optional[float] = None) -> ItemSchema:
    item = db.query(Item).filter(Item.id == item_id, Item.deleted == False).first()
    if not item:
        raise ValueError(f"Item {item_id} not found.")
    if new_name:
        item.name = new_name
    if new_price:
        item.price = new_price
    db.commit()
    db.refresh(item)
    return ItemSchema.from_orm(item)


def delete_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        item.deleted = True
        db.commit()


def get_cart(db: Session, cart_id: int) -> Optional[CartSchema]:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        return None
    return CartSchema(
        id=cart.id,
        items=[ItemInCartSchema.from_orm(item) for item in cart.items],
        price=cart.total_price
    )


def get_carts(db: Session, offset: int, limit: int, min_price: Optional[float], max_price: Optional[float], min_quantity: Optional[int], max_quantity: Optional[int]) -> List[CartSchema]:
    query = db.query(Cart)
    if min_price is not None:
        query = query.filter(Cart.total_price >= min_price)
    if max_price is not None:
        query = query.filter(Cart.total_price <= max_price)
    carts = query.offset(offset).limit(limit).all()
    return [
        CartSchema(
            id=cart.id,
            items=[ItemInCartSchema.from_orm(item) for item in cart.items],
            price=cart.total_price
        )
        for cart in carts
    ]


def create_cart(db: Session) -> CartSchema:
    cart = Cart(total_price=0.0)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return CartSchema(
        id=cart.id,
        items=[ItemInCartSchema.from_orm(item) for item in cart.items],
        price=cart.total_price
    )


def add_item_in_cart(db: Session, cart_id: int, item_id: int) -> CartSchema:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    item = db.query(Item).filter(Item.id == item_id, Item.deleted == False).first()
    if not cart:
        raise ValueError(f"Cart with id {cart_id} not found.")
    if not item:
        raise ValueError(f"Item with id {item_id} not found.")
    
    item_in_cart = db.query(ItemInCart).filter_by(cart_id=cart_id, item_id=item_id).first()
    if item_in_cart:
        item_in_cart.quantity += 1
    else:
        item_in_cart = ItemInCart(cart_id=cart_id, item_id=item_id, quantity=1)
        db.add(item_in_cart)
    
    cart.total_price += item.price
    db.commit()
    db.refresh(cart)

    return CartSchema(
        id=cart.id,
        items=[ItemInCartSchema.from_orm(item) for item in cart.items],
        price=cart.total_price
    )