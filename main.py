import asyncio
from itertools import zip_longest
import os
import argparse

from pyrogram import Client

from data import config
from utils.core import get_all_lines
from utils.starter import start
from utils.core.telegram import Accounts


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, help="Action to perform")

    action = parser.parse_args().action
    if not action:
        action = int(input("Select action:\n1. Start soft\n2. Create sessions\n\n> "))

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

    if action == 2:
        await Accounts().create_sessions()

    if action == 1:
        accounts = await Accounts().get_accounts()

        tasks = []

        if config.USE_PROXY_FROM_FILE:  # найс дублирование кода (впадлу фиксить пока)
            proxys = get_all_lines(filepath=config.PROXY_PATH)
            for account, proxy in zip_longest(accounts, proxys):
                if not account:
                    break
                session_name, _, proxy = account.values()
                client = Client(
                    name=session_name,
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    proxy=proxy,
                    workdir=config.WORKDIR
                )
                tasks.append(asyncio.create_task(start(tg_client=client, proxy=proxy)))
        else:
            for account in accounts:
                session_name, _, proxy = account.values()
                client = Client(
                    name=session_name,
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    proxy=proxy,
                    workdir=config.WORKDIR
                )
                tasks.append(asyncio.create_task(start(tg_client=client, proxy=proxy)))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

# # await Accounts().create_sessions()
# accounts = await Accounts().get_accounts()

# for account in accounts:
#     session_name, phone_number, _ = account.values()
#     client = Client(
#         name=session_name,
#         api_id=config.API_ID,
#         api_hash=config.API_HASH,
#         phone_number=phone_number,
#         workdir=config.WORKDIR
#     )
#     truecoin = TrueCoin(tg_client=client)
#     await truecoin.login()
#     await truecoin.get_wall_tasks()
#     await truecoin.logout()
