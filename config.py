import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 텔레그램 설정
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# ANTHROPIC 설정
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# 에러 메시지
ERROR_MESSAGES = {
    'server_error': '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
}

# Railway 환경 설정
IS_PRODUCTION = os.getenv('RAILWAY_ENVIRONMENT') == 'production'
PORT = int(os.getenv('PORT', 3000))
