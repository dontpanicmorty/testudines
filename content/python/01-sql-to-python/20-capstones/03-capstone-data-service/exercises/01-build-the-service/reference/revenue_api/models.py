"""Response and request models: the public contract."""
from datetime import date

from pydantic import BaseModel, Field


class DailyRevenue(BaseModel):
    day: date
    region: str
    orders: int
    revenue: float


class RegionRevenue(BaseModel):
    region: str
    orders: int
    revenue: float


class DayDetail(BaseModel):
    day: date
    orders: int
    revenue: float
    regions: list[RegionRevenue]


class Customer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    region: str
    plan: str
    signup_date: date


class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int
    has_next: bool


class RevenuePage(PageMeta):
    items: list[DailyRevenue]


class CustomerPage(PageMeta):
    items: list[Customer]


class NewCustomer(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+$")
    region: str = Field(min_length=1)
    plan: str = Field(pattern=r"^(free|pro|enterprise)$")
