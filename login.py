from telethon import TelegramClient

# O'ZINGIZNIKI
API_ID = 38695797
API_HASH = "6549f09916a2711caef73f5d5002f78b"

client = TelegramClient(
    "my_account",
    API_ID,
    API_HASH
)

async def main():
    me = await client.get_me()

    print("\n==========================")
    print("AKKAUNT MUVAFFAQIYATLI ULANDI")
    print("==========================")
    print("Ism:", me.first_name)
    print("Username:", me.username)
    print("ID:", me.id)
    print("==========================")

with client:
    client.loop.run_until_complete(main())