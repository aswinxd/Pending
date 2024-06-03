from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest

# Replace these with your own values
api_id = "22710783"
api_hash = "616ea341acfed51f916506c20b8a0a44"
bot_token = "7022599037:AAGOZdH0OTRakPAhkFmAHB1KuLr-jRCKHQo"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_chat_join_request()
async def approve_pending_requests(client: Client, chat_id: int):
    try:
        pending_requests = await client.get_chat_join_requests(chat_id)
        for request in pending_requests:
            await client.approve_chat_join_request(
                chat_id=chat_id,
                user_id=request.user.id
            )
            print(f"Approved pending join request from {request.user.first_name} in {request.chat.title}")
    except Exception as e:
        print(f"Failed to approve pending join requests: {e}")

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

@app.on_message(filters.command("approve_pending"))
async def approve_pending_command(client: Client, message):
    chat_id = message.chat.id
    await approve_pending_requests(client, chat_id)

if __name__ == "__main__":
    app.start()
    
    # Approve pending requests for specific chats (groups or channels)
    # Replace with your group/channel IDs
    group_ids = [-1002058711408]  # Example group/channel IDs
    
    for group_id in group_ids:
        app.loop.run_until_complete(approve_pending_requests(app, group_id))
    
    app.idle()
