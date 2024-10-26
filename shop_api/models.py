from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class ItemInCart(BaseModel):
    item_id: int
    cart_id: int
    quantity: int
    available: bool = True

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True

class Cart(BaseModel):
    id: int
    items: List[ItemInCart] = Field(default_factory=list)
    price: float = 0.0

    class Config:
        from_attributes = True

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    price: float = 0.0
    deleted: bool = False

    class Config:
        from_attributes = True

class ItemPut(BaseModel):
    name: str
    price: float = 0.0
    deleted: bool = False
    
    class Config:
        from_attributes = True

class ItemPatch(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

    model_config = ConfigDict(extra='forbid')