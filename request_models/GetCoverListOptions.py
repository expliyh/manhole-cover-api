from pydantic import BaseModel


class SortOption:
    """
    排序选项
    """
    field: str
    order: str


class FilterOption:
    """
    过滤选项
    """
    field: str
    value: str
    match_mode: str
    operator: str


class GetCoverListOptions(BaseModel):
    """
    获取井盖列表时所需的参数
    """
    rows_per_page: int
    first: int
    filter_by: [FilterOption] = []
    sort_by: [SortOption] = []
