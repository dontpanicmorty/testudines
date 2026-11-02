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
    """Public customer shape. Note: no email."""

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
    """Request body for POST /customers.

    TODO: add constraints so invalid bodies fail validation (see the prompt):
    names non-empty, email shaped like x@y, plan in free/pro/enterprise, region non-empty.
    """

    first_name: str
    last_name: str
    email: str
    region: str
    plan: str
