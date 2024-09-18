import asyncio
import os

from pyrogram import Client

from data import config
from utils.truecoin import TrueCoin
from utils.core.telegram import Accounts


async def main():
    """TODO: Надо ща создать сессию и вызвать TrueCoin.get_tg_web_data и посмотреть, что приходит в урлы (ЕСЛИ ТАМ ЕСТЬ AUTH-KEY - ПОБЕДА)"""
    if not os.path.exists('sessions'):
        os.mkdir('sessions')

    if config.USE_PROXY_FROM_FILE:
        if not os.path.exists(config.PROXY_PATH):
            with open(config.PROXY_PATH, 'w') as f:
                f.write("")
    else:
        if not os.path.exists('sessions/accounts.json'):
            with open("sessions/accounts.json", 'w') as f:
                f.write("[]")

    # await Accounts().create_sessions()
    accounts = await Accounts().get_accounts()

    for account in accounts:
        session_name, phone_number, proxy = account.values()
        client = Client(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            phone_number=phone_number,
            workdir=config.WORKDIR
        )
        truecoin = TrueCoin(tg_client=client)
        await truecoin.get_tg_web_data()


if __name__ == "__main__":
    asyncio.run(main())
