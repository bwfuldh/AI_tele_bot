from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """시작 명령어 처리"""
    await update.message.reply_text(
        "안녕하세요! 분석 봇입니다. 시작하려면 /start 를 입력해주세요."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """도움말 명령어 처리"""
    help_text = (
        "🚀 사용 가능한 명령어:\n\n"
        "/start - 시작하기\n"
        "/cancle - 분석 취소\n"
        "/help - 도움말 보기"
    )
    await update.message.reply_text(help_text)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """에러 처리"""
    print(f'Update {update} caused error {context.error}')
