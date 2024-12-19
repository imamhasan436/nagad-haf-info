from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

TOKEN = "8190965782:AAHMDHEFBzg_F0wd4KPgKBMPm7vbIhWFtFk"  # আপনার বটের টোকেন এখানে বসান

async def check_group_only(update: Update) -> bool:
    if update.message.chat.type != "group" and update.message.chat.type != "supergroup":
        await update.message.reply_text("⚠️ এই বট শুধুমাত্র গ্রুপে কাজ করবে।")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_group_only(update):
        return
    await update.message.reply_text("Welcome! Use /nagad to input your phone number.")

async def nagad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_group_only(update):
        return
    await update.message.reply_text("📱SEND YOUR NAGAD NUMBER:")
    context.user_data['waiting_for_number'] = True

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_group_only(update):
        return
    if context.user_data.get('waiting_for_number'):
        number = update.message.text.strip()
        context.user_data['waiting_for_number'] = False

        url = "https://app2.mynagad.com:20002/api/user/check-user-status-for-log-in"
        headers = {
            'User-Agent': "okhttp/3.14.9",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'X-KM-UserId': "37235319",
            'X-KM-User-AspId': "100012345612345",
            'X-KM-User-Agent': "ANDROID/1164",
            'X-KM-DEVICE-FGP': "74D93CCB6CDF5B86D021AFF522BB4A4555CDEEE844E01F73FBF6B60B2EA09346",
            'X-KM-Accept-language': "bn",
            'X-KM-AUTH-TOKEN': "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIwMTk4MTAyNTY0NCIsInBob25lIjoiMDE5ODEwMjU2NDQiLCJhc3BJZCI6IjEwMDAxMjM0NTYxMjM0NSIsImNyZWF0ZWQiOjE3Mjg4MzYxNTYxMzQsInJhbmRvbVZhbHVlIjoiMTcyODgzNjE1NjEzNCIsInVzZXJUeXBlIjoiQ1UiLCJ0eXBlIjoiQUNDRVNTX1RPS0VOIiwiZXhwIjoxNzI4ODM2NDU2LCJ1c2VySWQiOiIzNzIzNTMxOSIsIm1wYUlkIjpudWxsLCJlbWFpbCI6bnVsbH0.Y681tEN45Qb77ZkVqTvBp6GS5__huvRAgzUH8Yi3krQ20qWOw9N92eoBilk04TwBpHmtxvPC--3ECeI40VrEWg",
            'X-KM-AppCode': "01"
        }
        params = {'msisdn': number}

        try:
            response = requests.get(url, params=params, headers=headers)
            if response.ok:
                data = response.json()
                response_text = "\n".join([f"*{key}*: {value}" for key, value in data.items()])
                await update.message.reply_text(f"*♻️INFO FOUND SUCCESS♻️*\n\n{response_text}", parse_mode="MarkdownV2")
            else:
                await update.message.reply_text(f"*Error:* {response.status_code}", parse_mode="MarkdownV2")
        except Exception as e:
            await update.message.reply_text(f"*Request Failed:* {str(e)}", parse_mode="MarkdownV2")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nagad", nagad))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
