from telethon import TelegramClient, events
import asyncio
from datetime import datetime

API_ID = 34887085
API_HASH = '2b4cdfcc467872dea92c20f0306d301a'
TARGET_GROUP = -1003012743111

SOURCE_BOTS = ['extranjerianotifyesp_bot', 'avisocitaextranjeria']

client = TelegramClient('session', API_ID, API_HASH)
message_count = 0

@client.on(events.NewMessage(chats=SOURCE_BOTS))
async def forward_handler(event):
    global message_count
    try:
        message = event.message
        message_text = message.text or ""
        
        if message_text:
            await client.send_message(TARGET_GROUP, message_text)
        
        if message.media:
            await client.send_file(TARGET_GROUP, message.media, caption=message_text)
        
        message_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n✅ Message #{message_count} | {timestamp}")
        print(f"From: @{event.chat.username}")
        print(f"Text: {message_text[:80]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    print("🤖 Starting Telegram Forwarder...")
    await client.start()
    me = await client.get_me()
    print(f"✅ Logged in: {me.first_name} (+{me.phone})")
    print(f"📢 Monitoring: {', '.join(['@'+b for b in SOURCE_BOTS])}")
    print("✅ Bot running!\n")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
