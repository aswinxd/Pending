import logging
import asyncio
from os import environ
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

logging.basicConfig(level=logging.INFO)

# Get API ID and API hash from environment variables
API_ID = int(environ.get("API_ID", 22710783))
API_HASH = environ.get("API_HASH", "616ea341acfed51f916506c20b8a0a44")
SESSION_NAME = "my_account"
if not API_ID or not API_HASH:
    raise ValueError("API_ID and API_HASH must be set")

# Create a new Client instance and save the session to a file
User = Client(name="AcceptUser", api_id=API_ID, api_hash=API_HASH)

async def approve_requests(client, chat_id):
    logging.info(f"Starting to approve join requests in chat {chat_id}")
    
    while True:
        try:
            await client.approve_all_chat_join_requests(chat_id)
            logging.info(f"Approved all join requests in chat {chat_id}")
            await asyncio.sleep(1)  # Small delay to avoid continuous loop with high CPU usage
        except FloodWait as e:
            logging.warning(f"FloodWait encountered: Sleeping for {e.value} seconds")
            await asyncio.sleep(e.value)
        except BadRequest as e:
            logging.error(f"BadRequest error: {str(e)}")
            if "HIDE_REQUESTER_MISSING" in str(e):
                logging.info("No pending join requests to approve. Continuing to check...")
                await asyncio.sleep(5)  # Wait for a few seconds before checking again
            else:
                break
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            break

@User.on_message(filters.command(["run", "approve"], [".", "/"]))                     
async def approve(client, message):
    chat_id = message.chat.id
    await message.delete()
    await client.send_message(chat_id, "Approval process started. Approving pending join requests...")

    # Start the approval task
    asyncio.create_task(approve_requests(client, chat_id))

if __name__ == "__main__":
    logging.info("Bot started...")
    User.run()
