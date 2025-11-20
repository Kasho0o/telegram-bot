from telethon import TelegramClient, events
import asyncio
from datetime import datetime
import os

# ===== CONFIGURATION =====
API_ID = 34887085
API_HASH = '2b4cdfcc467872dea92c20f0306d301a'
TARGET_GROUP = -1003012743111  # Your Decita Previa group

SOURCE_BOTS = [
    'extranjerianotifyesp_bot',
    'avisocitaextranjeria'
]

# ===== BOT CODE =====
client = TelegramClient('session', API_ID, API_HASH)

message_count = 0

@client.on(events.NewMessage(chats=SOURCE_BOTS))
async def forward_handler(event):
    global message_count
    try:
        message = event.message
        message_text = message.text or ""
        
        # ✅ Send as YOUR message (NO "forwarded from" tag)
        if message_text:
            await client.send_message(TARGET_GROUP, message_text)
        
        # Send media if present
        if message.media:
            await client.send_file(
                TARGET_GROUP, 
                message.media,
                caption=message_text if message_text else ""
            )
        
        message_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{'='*60}")
        print(f"✅ Message #{message_count} forwarded")
        print(f"⏰ Time: {timestamp}")
        print(f"📤 From: @{event.chat.username}")
        print(f"📝 Text: {message_text[:100]}..." if len(message_text) > 100 else f"📝 Text: {message_text}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    print("\n" + "="*60)
    print("🤖 TELEGRAM NOTIFICATION FORWARDER")
    print("="*60)
    
    # Start client
    await client.start()
    
    # Get your info
    me = await client.get_me()
    print(f"\n✅ Logged in as: {me.first_name}")
    print(f"📱 Phone: +{me.phone}")
    print(f"📢 Target Group ID: {TARGET_GROUP}")
    print(f"\n📥 Monitoring these bots:")
    for bot in SOURCE_BOTS:
        print(f"   ✓ @{bot}")
    
    print("\n" + "="*60)
    print("✅ BOT IS RUNNING!")
    print("💡 Messages will appear as YOUR messages (no forward tag)")
    print("🔄 Waiting for notifications...")
    print("="*60 + "\n")
    
    # Keep running
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        # Auto-restart on error
        import time
        print("🔄 Restarting in 10 seconds...")
        time.sleep(10)
        asyncio.run(main())