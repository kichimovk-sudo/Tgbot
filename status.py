from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline, UserStatusOffline
import asyncio

API_ID = 38695797
API_HASH = "6549f09916a2711caef73f5d5002f78b"

client = TelegramClient(
    "my_account",
    API_ID,
    API_HASH
)


async def check_status():

    me = await client.get_me()

    print("\n============================")
    print("Telegram akkaunt holati")
    print("============================")

    print("Ism:", me.first_name)
    print("Username:", me.username)

    # Telegram statusini olish
    entity = await client.get_entity(me.id)

    status = entity.status

    if isinstance(status, UserStatusOnline):

        print("🟢 ONLINE")

    elif isinstance(status, UserStatusOffline):

        print("🔴 OFFLINE")

    else:

        print("⚪ STATUS ANIQLANMADI")

    print("============================")


async def main():

    await check_status()

    await client.disconnect()


with client:

    client.loop.run_until_complete(main())