class Notification:
    
    def __init__(self, bot):
        self.bot = bot
    
    def send_message(self, chat_id, message, reply_markup):
        self.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)