from services import add_cover
from .Yolo import yolo
from .test3 import filter_box, get_result


async def det(pid: int, file: bytes):
    output, or_img = yolo.inference(img_file=file)

    outbox = filter_box(output, 0.5, 0.5)  # 最终剩下的Anchors：0 1 2 3 4 5 分别是 x1 y1 x2 y2 score class

    result, or_img = get_result(outbox)

    await add_cover(pid, or_img, result[0][0])

