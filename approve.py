import logging
import asyncio
from os import environ
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, BadRequest

logging.basicConfig(level=logging.INFO)

API_ID = int(environ.get("API_ID", 22710783))
API_HASH = environ.get("API_HASH", "616ea341acfed51f916506c20b8a0a44")
SESSION_NAME = "my_account"
if not API_ID or not API_HASH:
    raise ValueError("API_ID and API_HASH must be set")

User = Client(name="AcceptUser", api_id=API_ID, api_hash=API_HASH)

BATCH_SIZE = 100  

async def approve_requests(client, chat_id):
    logging.info(f"Starting approval in chat {chat_id}")
    
    while True:
        try:
          
            async for request in client.get_chat_join_requests(chat_id, limit=BATCH_SIZE):
                if request is None:
                    logging.info("No more pending join requests.")
                    await client.send_message(chat_id, "All pending join requests have been approved.")
                    break

                try:
                
                    await client.approve_chat_join_request(chat_id, request.user.id)
                  #  logging.info(f"Approved user: {request.user.id}")
                except BadRequest as e:
                    if "USER_CHANNELS_TOO_MUCH" in str(e):
                        logging.warning(f"Cannot approve user {request.user.id}: User has joined too many channels.")
                       
                        continue
                    else:
                        raise e

               #  await asyncio.sleep(1)  

                try:
                     await client.approve_chat_join_request(chat_id, request.user.id)
                 except BadRequest as e:
                     if "400 INPUT_USER_DEACTIVATED" in str(e):
                        logging.warning(f"Cannot approve user {request.user.id}: User is deleted ac")
                        continue
                    else:
                        raise e

                 await asyncio.sleep(1)  

                   
    

             

        except FloodWait as e:
            logging.warning(f"FloodWait: Sleeping for {e.value} seconds.")
            await asyncio.sleep(e.value)  
        except BadRequest as e:
            logging.error(f"BadRequest error: {str(e)}")
            if "HIDE_REQUESTER_MISSING" in str(e):
                logging.info("HIDE_REQUESTER_MISSING, stopping.")
                break
            else:
                break
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            break

@User.on_message(filters.command(["run", "approve"], [".", "/"]))
async def approve(client, message):
    chat_id = message.chat.id
    await message.delete()
   # await client.send_message(chat_id, "Approval process started. Approving pending join requests...")
    asyncio.create_task(approve_requests(client, chat_id))

if __name__ == "__main__":
    logging.info("Bot started...")
    User.run()
