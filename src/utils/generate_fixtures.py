import os
from random import choice

from src.db.session import async_session
from src.models.memes import Meme


async def generate_memes(base_dir):
    data = list()
    text = 'Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. '
    text_eng = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

    files = os.listdir(base_dir + "/media")

    for _ in range(100):
        data.append(Meme(text=text, text_eng=text_eng, image=choice(files)))
    async with async_session() as session:
        session.add_all(data)
        await session.commit()
