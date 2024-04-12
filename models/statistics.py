import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .engine import engine

from .Cover import Cover

from defines import AuditStatus


async def get_statistics():
    async with engine.new_session() as session:
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=1)

        statement_all_cover = select(func.count()).select_from(Cover).filter(Cover.uploadTime >= start_time).filter(
            Cover.uploadTime <= end_time)

        statement_cover_broken = statement_all_cover.filter(Cover.recognizeResult != 'good')

        statement_cover_audited = statement_all_cover.filter(Cover.auditStatus != AuditStatus.NOT_VIEWED)

        statement_cover_fixed = statement_all_cover.filter(Cover.auditStatus == AuditStatus.VIEWED).filter(
            Cover.recognizeResult != 'good')

        result_all_cover = await session.execute(statement_all_cover)
        result_cover_broken = await session.execute(statement_cover_broken)
        result_cover_audited = await session.execute(statement_cover_audited)
        result_cover_fixed = await session.execute(statement_cover_fixed)

        return {
            'cover': {
                'all': result_all_cover.scalar_one(),
                'broken': result_cover_broken.scalar_one(),
                'audited': result_cover_audited.scalar_one(),
                'fixed': result_cover_fixed.scalar_one()
            }
        }
