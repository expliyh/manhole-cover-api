import asyncio
from unittest import TestCase
from recognize import det


class Test(TestCase):
    def test_detect(self):
        with open('../covers/pic_1.png', 'rb') as f:
            # asyncio.run(detect(1, f.read()))
            asyncio.run(det(1, f.read()))
