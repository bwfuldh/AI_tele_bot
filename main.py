import os
import logging
from telegram import Update
from telegram.ext import Application
from dotenv import load_dotenv
from bot.conversations import analysis_conversation

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """봇 실행"""
    # 토큰 확인
    token = os.getenv('TELEGRAM_TOKEN')
    print(f"\n현재 사용 중인 토큰: {token}\n")
    
    # 봇 생성
    application = Application.builder().token(token).build()
    
    # 대화 핸들러 등록
    application.add_handler(analysis_conversation)
    
    # 봇 실행
    print("봇이 시작되었습니다. Ctrl+C를 눌러 종료할 수 있습니다.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
