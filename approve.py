from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest

# Replace these with your own values
api_id = "22710783"
api_hash = "616ea341acfed51f916506c20b8a0a44"
bot_token = "7022599037:AAGOZdH0OTRakPAhkFmAHB1KuLr-jRCKHQo"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_chat_join_request()
async def approve_join_request(client: Client, chat_join_request: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(
            chat_id=chat_join_request.chat.id,
            user_id=chat_join_request.from_user.id
        )
        print(f"Approved join request from {chat_join_request.from_user.first_name} in {chat_join_request.chat.title}")
    except Exception as e:
        print(f"Failed to approve join request: {e}")

if __name__ == "__main__":
    app.run()
