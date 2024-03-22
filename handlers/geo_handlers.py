from fastapi import APIRouter

from geo_service import gaode

router = APIRouter()


@router.get("/api/geo/decode")
async def geo_decode(lon: float, lat: float):
    return await gaode.geo_decode(lon, lat)
