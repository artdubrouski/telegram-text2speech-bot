from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):
    '''Bot can be used only by users with specified access_id.'''
    def __init__(self, access_id: int):
        self.access_id = access_id
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if self.access_id == 0:
            return

        if int(message.from_user.id) != int(self.access_id):
            await message.answer("Access Denied")
            raise CancelHandler()
