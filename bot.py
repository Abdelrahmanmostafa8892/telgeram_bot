import telebot
from pydub import AudioSegment
from io import BytesIO

API_TOKEN = '7477344988:AAF1iZrTPjzuCREQXJnh0lZJn2-pUKDbByA'  # أضف التوكن هنا مباشرة
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    audio = AudioSegment.from_file(BytesIO(downloaded_file))
    
    bot.reply_to(message, "أرسل لي الأجزاء التي تريد قصها بتنسيق from 0:00:00 to 0:10:45 في كل سطر.")

    @bot.message_handler(func=lambda msg: True)
    def handle_text(message):
        try:
            parts = message.text.split('\n')
            for part in parts:
                start_str, end_str = part.split(' to ')
                start_time = convert_to_milliseconds(start_str.split(' ')[1])
                end_time = convert_to_milliseconds(end_str)
                
                segment = audio[start_time:end_time]
                output = BytesIO()
                segment.export(output, format="mp3")
                output.seek(0)
                
                bot.send_audio(message.chat.id, output, caption=f'جزء من {start_str} إلى {end_str}')
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ: {str(e)}")

def convert_to_milliseconds(time_str):
    h, m, s = map(float, time_str.split(':'))
    return int((h * 3600 + m * 60 + s) * 1000)

bot.polling()
