import os
from dotenv import load_dotenv
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-pro")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    first_name = update.effective_user.first_name.lower()

    if any(name in first_name for name in ["anh", "nam", "minh", "hoàng", "quang", "thắng"]):
        xung_ho = "anh"
    elif any(name in first_name for name in ["linh", "trang", "hằng", "ngọc", "phương", "nhi"]):
        xung_ho = "chị"
    else:
        xung_ho = "anh/chị"

    try:
        response = model.generate_content(
    f"""
    Bạn là nhân viên chăm sóc khách hàng của công ty.
    Trong mọi câu trả lời, bạn phải xưng là 'em' và gọi khách là '{xung_ho}'.
    Ví dụ: 'Dạ em chào {xung_ho}', 'Dạ {xung_ho} vui lòng cung cấp thêm thông tin', v.v.
    Tuyệt đối không dùng từ 'tôi' hoặc 'quý khách'.
    Chỉ trả lời các câu hỏi liên quan đến chính sách, bảo hành, đổi trả, sản phẩm, đơn hàng.
    Nếu câu hỏi không liên quan, hãy lịch sự từ chối.

    Câu hỏi từ {xung_ho}: {user_input}
    """
)
        await update.message.reply_text(response.text)
    except Exception as e:
        print("[LỖI]:", e)
        await update.message.reply_text("Hệ thống gặp lỗi. Thử lại sau.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 BOT Gemini 1.5 CSKH đang chạy... chờ tin nhắn từ Telegram")
    app.run_polling()
