from typing import List

from pydantic import BaseModel


class SortOption(BaseModel):
    """
    排序选项
    """
    field: str
    order: str


class FilterOption(BaseModel):
    """
    过滤选项
    """
    field: str
    value: str
    match_mode: str
    operator: str


class GetUserListOptions(BaseModel):
    """
    获取井盖列表时所需的参数
    """
    rows_per_page: int
    first: int
    filter_by: List[FilterOption] = []
    sort_by: List[SortOption] = []
