import asyncio
import requests
import time

from telethon import TelegramClient, events


# ============================================================
# TELEGRAM USER API
# ============================================================

API_ID = 38695797
API_HASH = "6549f09916a2711caef73f5d5002f78b"

# Oldingi login.py yaratgan session
SESSION = "my_account"


# ============================================================
# BOTFATHER BOT
# ============================================================

BOT_TOKEN = "8824074647:AAH_nSyADinBDL-FxXrFSettqgi4uwGq404"

BOT_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ============================================================
# INACTIVITY SOZLAMASI
# ============================================================

# TEST:
# 60 = 1 daqiqa
#
# REAL ISHLATISH UCHUN:
# 300 = 5 daqiqa

INACTIVE_AFTER = 60

# Timer har necha sekundda tekshiriladi
CHECK_EVERY = 2


# ============================================================
# AVTO JAVOB LUG'ATI
# ============================================================

JAVOBLAR = {

    "salom":
        "Va alaykum assalom. Hozircha offline bo'lganim uchun avtomatik javob berdim.",

    "assalomu alaykum":
        "Va alaykum assalom. Hozircha offline bo'lganim uchun avtomatik javob berdim.",

    "narx":
        "Narx haqida ma'lumotni keyinroq yuboraman.",

    "qancha":
        "Narx haqida ma'lumotni keyinroq yuboraman.",

    "manzil":
        "Manzilni keyinroq yuboraman.",

    "telefon":
        "Telefon raqamimni keyinroq yuboraman.",

    "rahmat":
        "Arzimaydi.",

    "yordam":
        "Hozircha offline bo'lganim uchun avtomatik javob berayapman."
}


# ============================================================
# TELETHON CLIENT
# ============================================================

client = TelegramClient(
    SESSION,
    API_ID,
    API_HASH
)


# ============================================================
# GLOBAL HOLATLAR
# ============================================================

# Oxirgi haqiqiy foydalanuvchi faoliyati
last_activity = time.monotonic()

# Hozir user faolmi?
is_active = True

# Bot hozir javob yuboryaptimi?
# Botning o'z xabari activity hisoblanmasligi uchun kerak.
bot_sending = False


# ============================================================
# USER ACTIVITY
# ============================================================

def mark_active():

    global last_activity

    last_activity = time.monotonic()


# ============================================================
# USER YUBORGAN XABAR
# ============================================================

@client.on(events.NewMessage(outgoing=True))
async def user_sent_message(event):

    global bot_sending

    # -----------------------------------------
    # Bot javob yuborayotgan bo'lsa
    # -----------------------------------------

    if bot_sending:

        print(
            "🤖 Bot yuborgan xabar "
            "→ activity hisoblanmadi"
        )

        return


    # -----------------------------------------
    # Telegram bot orqali yuborilgan xabar
    # -----------------------------------------

    if getattr(
        event.message,
        "via_bot",
        False
    ):

        print(
            "🤖 via_bot xabar "
            "→ activity hisoblanmadi"
        )

        return


    # -----------------------------------------
    # Haqiqiy outgoing xabar
    # -----------------------------------------

    mark_active()

    print(
        "\n📤 Siz xabar yubordingiz"
    )

    print(
        "🟢 ACTIVE"
    )


# ============================================================
# STATUS MONITOR
# ============================================================

async def status_monitor():

    global is_active

    previous_status = None

    while True:

        elapsed = (
            time.monotonic()
            - last_activity
        )

        # -----------------------------------------
        # ACTIVE / INACTIVE
        # -----------------------------------------

        current_status = (
            elapsed < INACTIVE_AFTER
        )


        # -----------------------------------------
        # STATUS O'ZGARGANDA CHIQARISH
        # -----------------------------------------

        if current_status != previous_status:

            previous_status = current_status

            if current_status:

                print()
                print(
                    "🟢 USER ACTIVE"
                )

                print(
                    "⏱️ Oxirgi faoliyat:",
                    round(elapsed, 1),
                    "sekund oldin"
                )

                print(
                    "🤖 Avtojavob: OFF"
                )

            else:

                print()
                print(
                    "🔴 USER INACTIVE"
                )

                print(
                    "⏱️ Faoliyatsiz:",
                    round(elapsed, 1),
                    "sekund"
                )

                print(
                    "🤖 Avtojavob: ON"
                )


        # Global qiymatni yangilash
        is_active = current_status


        await asyncio.sleep(
            CHECK_EVERY
        )


# ============================================================
# TELEGRAM BOT API — GET UPDATES
# ============================================================

def get_updates(offset=None):

    params = {

        "timeout": 25,

        "allowed_updates": [
            "business_message"
        ]
    }


    if offset is not None:

        params[
            "offset"
        ] = offset


    try:

        response = requests.get(

            BOT_API + "/getUpdates",

            params=params,

            timeout=35
        )

        return response.json()


    except Exception as e:

        print()
        print(
            "❌ Bot API xatosi:",
            e
        )

        return None


# ============================================================
# TELEGRAM BOT API — SEND MESSAGE
# ============================================================

async def send_answer(
    chat_id,
    business_connection_id,
    text
):

    global bot_sending

    # -----------------------------------------
    # Bot yuboryapti
    # -----------------------------------------

    bot_sending = True


    try:

        data = {

            "chat_id":
                chat_id,

            "text":
                text,

            "business_connection_id":
                business_connection_id
        }


        response = await asyncio.to_thread(

            requests.post,

            BOT_API + "/sendMessage",

            data=data,

            timeout=20
        )


        result = response.json()


        if result.get("ok"):

            print()
            print(
                "🤖 AVTOJAVOB YUBORILDI:"
            )

            print(
                text
            )

        else:

            print()
            print(
                "❌ Telegram javob xatosi:"
            )

            print(
                result
            )


    except Exception as e:

        print()
        print(
            "❌ Javob yuborish xatosi:",
            e
        )


    finally:

        # -----------------------------------------
        # Telethon event kelib qolsa ham
        # bot xabarini activity hisoblamaslik
        # -----------------------------------------

        await asyncio.sleep(3)

        bot_sending = False


# ============================================================
# BUSINESS BOT LOOP
# ============================================================

async def bot_loop():

    offset = None


    print()
    print(
        "=============================="
    )

    print(
        "🤖 SECRETARY AUTO REPLY"
    )

    print(
        "=============================="
    )

    print(
        "Inactivity:",
        INACTIVE_AFTER,
        "sekund"
    )

    print(
        "Tekshirish:",
        CHECK_EVERY,
        "sekund"
    )

    print(
        "=============================="
    )


    while True:

        updates = await asyncio.to_thread(

            get_updates,

            offset
        )


        # -----------------------------------------
        # UPDATE YO'Q
        # -----------------------------------------

        if not updates:

            await asyncio.sleep(2)

            continue


        # -----------------------------------------
        # TELEGRAM API ERROR
        # -----------------------------------------

        if not updates.get("ok"):

            print()
            print(
                "❌ Telegram Bot API xatosi:"
            )

            print(
                updates
            )

            await asyncio.sleep(5)

            continue


        # -----------------------------------------
        # UPDATE'LAR
        # -----------------------------------------

        for update in updates.get(
            "result",
            []
        ):


            offset = (
                update[
                    "update_id"
                ] + 1
            )


            # =====================================
            # BUSINESS MESSAGE
            # =====================================

            message = update.get(
                "business_message"
            )


            if not message:

                continue


            # =====================================
            # MATN
            # =====================================

            text = message.get(
                "text"
            )


            if not text:

                continue


            print()
            print(
                "------------------------------"
            )

            print(
                "📩 Yangi xabar:",
                text
            )


            # =====================================
            # USER ACTIVE BO'LSA
            # =====================================

            if is_active:

                print(
                    "🟢 USER ACTIVE"
                )

                print(
                    "🚫 Avtojavob yuborilmadi."
                )

                continue


            # =====================================
            # USER INACTIVE
            # =====================================

            print(
                "🔴 USER INACTIVE"
            )

            print(
                "🤖 Avtojavob tekshirilmoqda..."
            )


            # =====================================
            # KALIT SO'Z
            # =====================================

            text_lower = (
                text
                .lower()
                .strip()
            )


            answer = None


            for keyword, response in JAVOBLAR.items():

                if keyword in text_lower:

                    answer = response

                    break


            # =====================================
            # JAVOB TOPILMADI
            # =====================================

            if not answer:

                print(
                    "ℹ️ Kalit so'z topilmadi."
                )

                continue


            # =====================================
            # CHAT ID
            # =====================================

            chat = message.get(
                "chat",
                {}
            )


            chat_id = chat.get(
                "id"
            )


            # =====================================
            # BUSINESS CONNECTION ID
            # =====================================

            business_connection_id = (
                message.get(
                    "business_connection_id"
                )
            )


            if not business_connection_id:

                print()
                print(
                    "❌ business_connection_id "
                    "topilmadi."
                )

                continue


            # =====================================
            # JAVOB
            # =====================================

            await send_answer(

                chat_id,

                business_connection_id,

                answer
            )


# ============================================================
# MAIN
# ============================================================

async def main():

    print()
    print(
        "=============================="
    )

    print(
        "🚀 TELEGRAM SECRETARY SYSTEM"
    )

    print(
        "=============================="
    )


    # -----------------------------------------
    # Telethon login
    # -----------------------------------------

    await client.start()


    # -----------------------------------------
    # Akkaunt ma'lumotlari
    # -----------------------------------------

    me = await client.get_me()


    print()
    print(
        "👤 AKKAUNT:"
    )

    print(
        "Ism:",
        me.first_name
    )

    print(
        "Username:",
        me.username
    )

    print(
        "ID:",
        me.id
    )


    print()
    print(
        "⏱️ INACTIVE chegarasi:",
        INACTIVE_AFTER,
        "sekund"
    )


    print()
    print(
        "🟢 Tizim ishga tushdi."
    )

    print(
        "=============================="
    )


    # -----------------------------------------
    # Ikkala jarayon bir vaqtda ishlaydi
    # -----------------------------------------

    await asyncio.gather(

        status_monitor(),

        bot_loop()
    )


# ============================================================
# START
# ============================================================

with client:

    client.loop.run_until_complete(
        main()
    )