from pyrogram import Client, filters
from pyrogram.types import (Message,
                            InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle,InputTextMessageContent)
from pyromod import listen

api_id = "1272537"
api_hash = "7cf7e855971ec61a606cc4ff5eaa3d1b"

admin_user_id = 886415476

app = Client("pm", config_file="config.ini")

@app.on_message(filters.private)
async def main(_:app, m:Message):
    msg = m.text
    u_id = m.from_user.id

    if msg == "/start":
        if u_id == admin_user_id:
            await m.reply("Hello, Welcome :0")
        else:
            await m.reply("Hello, Send the message : ")
    
    else:
        if u_id != admin_user_id:
            await app.send_message(admin_user_id, f"**New Message from** [{u_id}](tg://user?id={u_id}) 👇")
            await m.copy(admin_user_id, reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=f"response", callback_data=f"r-{u_id}")
                    ],
                ]
                )
            )

            await m.reply("Message sent successfully.")


@app.on_callback_query()
async def callbacks(_:app, query):
    await app.answer_callback_query(query.id, text=None, show_alert=False)
    d = str(query.data)
    if "r-" in d:
        u_id = d.split("-")[1]
        r = await app.ask(admin_user_id, "Send the response : ")
        await app.copy_message(u_id, admin_user_id, r.message_id)
        await app.send_message(admin_user_id, "Response sended!")
        try:
            await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=f"responsed ✓", callback_data=f"{query.data}")
                    ],
                ]
                )
            )
        except:pass

app.run()