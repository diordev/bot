from aiogram.types import InputFile


async def user_photo(photo: str):
    if photo.startswith("users/"):
        photo = InputFile(path_or_bytesio=f"waiter_admin/{photo}")
    return photo


async def product_photo(photo: str):
    if photo.startswith("products/"):
        photo = InputFile(path_or_bytesio=f"waiter_admin/{photo}")
    return photo