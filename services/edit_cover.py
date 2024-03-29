from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from defines import AuditStatus
from models import engine, Cover

from request_models.EditCoverRequest import EditCoverRequest


async def edit_cover(option: EditCoverRequest):
    async with engine.new_session() as session:
        cover: Cover | None = await session.get(Cover, option.cid)
        if cover is None:
            raise HTTPException(status_code=404, detail="Cover not found")
        cover.editCount += 1

        if option.auditStatus == AuditStatus.NOT_VIEWED and Cover.auditStatus != AuditStatus.NOT_VIEWED:
            raise HTTPException(status_code=400, detail='此纪录已审核，不能设置为未审核状态')

        if cover.auditStatus == AuditStatus.NOT_VIEWED and option.correctedResult is not None:
            if option.auditStatus in (None, AuditStatus.NOT_VIEWED):
                raise HTTPException(status_code=400, detail="此记录未经审核")

        if (a_stat := option.auditStatus) is not None:
            cover.auditStatus = a_stat
        if (c_result := option.correctedResult) is not None:
            cover.correctedResult = c_result

        await session.commit()
