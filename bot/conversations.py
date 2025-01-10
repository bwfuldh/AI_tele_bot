"""
대화 흐름 관리 모듈

이 모듈은 텔레그램 봇의 대화 흐름을 관리합니다.
사용자와의 상호작용을 단계별로 처리하고, 각 단계에서 적절한 응답을 제공합니다.

주요 기능:
1. 대화 상태 관리
2. 사용자 입력 처리
3. 키보드 메뉴 제공
4. AI 분석 결과 전달

사용자 정의:
- 대화 흐름 수정
- 키보드 메뉴 구성
- 응답 메시지 형식
"""

import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)
from bot.messages import ElonStyleMessageFormatter as Elon
from services.langchain_service import LangChainService
from database import init_db, save_analysis

# 데이터베이스 초기화
init_db()

# AI 분석 서비스 인스턴스
langchain_service = LangChainService()

# 대화 상태 정의 - 각 상태는 하나의 질문/응답 단계를 나타냅니다
(WAITING_START, 
 IDEA,           # 아이디어 설명 (자유 입력)
 CATEGORY,       # 서비스 분야 선택
 APPROACH,       # 접근 방식 선택
 TARGET,         # 타겟 고객 선택
 PROBLEM,        # 해결할 문제 선택
 SOLUTION,       # 해결 방안 선택
 IMPLEMENTATION, # 구현 기술 선택
 GOALS,          # 목표 선택
 NEEDS,          # 필요 사항 선택
 ANALYZING,      # AI 분석 중
 HELP_MENU) = range(12)

# 키보드 메뉴 정의 - 각 단계별로 사용자에게 제공할 선택지를 구성합니다
# 필요에 따라 옵션을 수정하거나 새로운 키보드를 추가할 수 있습니다

# 서비스 분야 선택 옵션
CATEGORY_KEYBOARD = [
    ['🚀 서비스/앱', '💡 콘텐츠/미디어'],
    ['🤖 AI/데이터', '🎮 게임/엔터'],
    ['🏥 건강/의료', '🎓 교육/이러닝'],
    ['💰 금융/핀테크', '🛍️ 커머스/유통'],
    ['✨ 직접 입력']
]

# 서비스 형태 선택 옵션
APPROACH_KEYBOARD = [
    ['💫 B2C 서비스', '🎯 B2B 서비스'],
    ['🤝 B2B2C 서비스', '💡 하드웨어'],
    ['📊 플랫폼', '🌱 콘텐츠'],
    ['✨ 직접 입력']
]

# 타겟 고객 선택 옵션
TARGET_KEYBOARD = [
    ['👥 일반 소비자', '👨‍👩‍👧‍👦 가족/육아'],
    ['👨‍💼 직장인', '🎓 학생'],
    ['💼 소상공인', '🏢 기업'],
    ['✨ 직접 입력']
]

# 문제 유형 선택 옵션
PROBLEM_KEYBOARD = [
    ['⏰ 시간/비용 절약', '📈 생산성 향상'],
    ['😊 편의성/접근성', '🤝 소통/협업'],
    ['💡 정보/지식 습득', '🎯 목표 달성'],
    ['✨ 직접 입력']
]

# 해결 방식 선택 옵션
SOLUTION_KEYBOARD = [
    ['📱 모바일 앱', '💻 웹 서비스'],
    ['🤖 AI 솔루션', '🎮 게임/콘텐츠'],
    ['🛠️ 자동화 도구', '🤝 플랫폼'],
    ['✨ 직접 입력']
]

# 구현 기술 선택 옵션
IMPLEMENTATION_KEYBOARD = [
    ['📱 iOS/Android', '💻 웹/크로스플랫폼'],
    ['☁️ 클라우드/서버', '🤖 AI/ML'],
    ['🎮 게임엔진', '🔒 블록체인'],
    ['✨ 직접 입력']
]

# 목표 선택 옵션
GOALS_KEYBOARD = [
    ['📈 매출/성장', '👥 유저 확보'],
    ['🌟 브랜드 인지도', '🤝 파트너십'],
    ['💰 투자 유치', '🌍 해외 진출'],
    ['✨ 직접 입력']
]

# 필요 사항 선택 옵션
NEEDS_KEYBOARD = [
    ['👨‍💻 개발 인력', '🎨 기획/디자인'],
    ['💰 초기 투자금', '📊 시장 검증'],
    ['🤝 파트너/멘토', '📢 마케팅'],
    ['✨ 직접 입력']
]

# 도움말 메뉴 옵션
HELP_KEYBOARD = [
    ['📚 도움말 1'],
    ['💡 도움말 2'],
    ['🤝 도움말 3'],
    ['📊 도움말 4'],
    ['❓ 도움말 5']
]

# 시작 메뉴 옵션
START_KEYBOARD = [
    ['✨ 시작하기'],
    ['📚 가이드']
]

async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    대화 시작 핸들러
    
    사용자가 /start 명령어를 입력했을 때 실행됩니다.
    웰컴 메시지와 시작 버튼을 표시합니다.
    """
    try:
        # 이미지와 웰컴 메시지 전송
        await update.message.reply_photo(
            photo=Elon.WELCOME_IMG_URL,
            caption=Elon.WELCOME_MESSAGE,
            reply_markup=ReplyKeyboardMarkup(START_KEYBOARD, resize_keyboard=True)
        )
    except Exception as e:
        print(f"이미지 전송 실패: {e}")
        await update.message.reply_text(
            Elon.WELCOME_MESSAGE,
            reply_markup=ReplyKeyboardMarkup(START_KEYBOARD, resize_keyboard=True)
        )
    return WAITING_START

async def handle_start_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    시작 응답 처리 핸들러
    
    사용자가 시작 버튼을 클릭했을 때의 응답을 처리합니다.
    분석 프로세스를 시작하거나 가이드를 제공합니다.
    """
    text = update.message.text
    
    if text == '✨ 시작하기':
        await update.message.reply_text(Elon.QUESTIONS['idea'])
        return IDEA
    elif text == '📚 외부 채널 연결':
        keyboard = [[
            InlineKeyboardButton(
                "✨✨✨✨✨✨✨✨✨\n✨✨연결 버튼✨✨",
                url="http://starlenz.notion.site"
            )
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✨✨연결 버튼✨✨",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("안내 메세지 👀")
        return WAITING_START

async def handle_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    아이디어 입력 처리 핸들러
    
    사용자가 입력한 아이디어 설명을 저장하고
    다음 단계(서비스 분야 선택)로 진행합니다.
    """
    context.user_data['idea'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(CATEGORY_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['category'],
        reply_markup=reply_markup
    )
    return CATEGORY

async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    서비스 분야 선택 처리 핸들러
    
    사용자가 선택한 서비스 분야를 저장하고
    다음 단계(서비스 형태 선택)로 진행합니다.
    """
    context.user_data['category'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(APPROACH_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['approach'],
        reply_markup=reply_markup
    )
    return APPROACH

async def handle_approach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    서비스 형태 선택 처리 핸들러
    
    사용자가 선택한 서비스 형태를 저장하고
    다음 단계(타겟 고객 선택)로 진행합니다.
    """
    context.user_data['approach'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(TARGET_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['target'],
        reply_markup=reply_markup
    )
    return TARGET

async def handle_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    타겟 고객 선택 처리 핸들러
    
    사용자가 선택한 타겟 고객을 저장하고
    다음 단계(문제 유형 선택)로 진행합니다.
    """
    context.user_data['target'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(PROBLEM_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['problem'],
        reply_markup=reply_markup
    )
    return PROBLEM

async def handle_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    문제 유형 선택 처리 핸들러
    
    사용자가 선택한 문제 유형을 저장하고
    다음 단계(해결 방식 선택)로 진행합니다.
    """
    context.user_data['problem'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(SOLUTION_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['solution'],
        reply_markup=reply_markup
    )
    return SOLUTION

async def handle_solution(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    해결 방식 선택 처리 핸들러
    
    사용자가 선택한 해결 방식을 저장하고
    다음 단계(구현 기술 선택)로 진행합니다.
    """
    context.user_data['solution'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(IMPLEMENTATION_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['implementation'],
        reply_markup=reply_markup
    )
    return IMPLEMENTATION

async def handle_implementation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    구현 기술 선택 처리 핸들러
    
    사용자가 선택한 구현 기술을 저장하고
    다음 단계(목표 선택)로 진행합니다.
    """
    context.user_data['implementation'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(GOALS_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['goals'],
        reply_markup=reply_markup
    )
    return GOALS

async def handle_goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    목표 선택 처리 핸들러
    
    사용자가 선택한 목표를 저장하고
    다음 단계(필요 사항 선택)로 진행합니다.
    """
    context.user_data['goals'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(NEEDS_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['needs'],
        reply_markup=reply_markup
    )
    return NEEDS

async def handle_needs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    필요 사항 선택 처리 핸들러
    
    사용자가 선택한 필요 사항을 저장하고
    AI 분석을 시작합니다.
    """
    context.user_data['needs'] = update.message.text
    
    try:
        # 분석 시작 메시지 전송
        await update.message.reply_text(
            Elon.ANALYSIS_START,
            reply_markup=ReplyKeyboardRemove()
        )
        
        # AI 분석 수행 및 결과 대기
        analysis_result = await langchain_service.analyze_startup(context.user_data)
        
        if not analysis_result:
            await update.message.reply_text(
                "⚠️ 분석 중 오류가 발생했습니다. 다시 시도해주세요."
            )
            return ConversationHandler.END
            
        # 분석 결과 저장 (실패해도 분석은 계속 진행)
        try:
            save_analysis(
                telegram_id=update.effective_user.id,
                input_data=context.user_data,
                result=analysis_result
            )
        except Exception as e:
            print(f"데이터베이스 저장 오류: {e}")
            await update.message.reply_text(
                "⚠️ 분석 중 오류가 발생했습니다. 다시 시도해주세요."
            )
            return ConversationHandler.END
        
        # 분석 결과 구조 보존
        formatted_result = {
            'summary': analysis_result.get('summary', ''),
            'case_studies': analysis_result.get('case_studies', []),
            'feasibility': analysis_result.get('feasibility', []),
            'development_plan': analysis_result.get('development_plan', []),
            'improvements': analysis_result.get('improvements', [])
        }
        
        # 디버깅 로그
        print("\n=== Analysis Result Structure ===")
        for key, value in formatted_result.items():
            print(f"\n{key}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  {item}")
            else:
                print(f"  {value}")
        
        context.user_data['analysis_result'] = formatted_result
        
        # 분석 결과 메시지 전송
        formatted_message = Elon.format_analysis_result(formatted_result)
        await update.message.reply_text(formatted_message)
        
        # 분석 완료 후 인라인 키보드 생성
        keyboard = [
            [
                InlineKeyboardButton("외부 링크 연결", url="http://starlenz.notion.site")
            ],
            [
                InlineKeyboardButton("공유하기", url="https://t.me/share/url?url=https://t.me/starlenz_bot&text=✨아이디어 분석 도우미✨"),
                InlineKeyboardButton("관리자 문의", url="tg://resolve?domain=starlenz_inc")
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "분석이 완료되었습니다!",
            reply_markup=reply_markup
        )
        
        return ConversationHandler.END
        
    except Exception as e:
        print(f"분석 중 오류 발생: {e}")
        await update.message.reply_text(
            "⚠️ 시스템 오류가 발생했습니다. 다시 시도해주세요."
        )
        return ConversationHandler.END

async def handle_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    분석 결과 처리 핸들러
    
    AI 분석 결과를 사용자에게 표시합니다.
    분석 결과가 없는 경우 오류 메시지를 표시합니다.
    """
    if 'analysis_result' not in context.user_data:
        await update.message.reply_text(
            "❌ 분석 결과를 찾을 수 없습니다. 다시 시작해주세요."
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        Elon.format_analysis_result(context.user_data['analysis_result'])
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    도움말 명령어 핸들러
    
    사용자가 /help 명령어를 입력했을 때 실행됩니다.
    도움말 메뉴를 표시합니다.
    """
    help_text = (
        "가이드:\n\n"
        "/start | 새로운 분석 시작\n"
        "/help | 도움말\n\n"
        "@starlenz_inc | 관리자 연결"
    )
    
    # 기존의 HELP_KEYBOARD만 사용해서 키보드를 정의합니다.
    reply_markup = ReplyKeyboardMarkup(HELP_KEYBOARD, resize_keyboard=True)
    
    # 텍스트와 기존 키보드를 함께 전송
    await update.message.reply_text(help_text, reply_markup=reply_markup)
    return HELP_MENU

async def handle_help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    도움말 메뉴 처리 핸들러
    
    도움말 메뉴에서 사용자가 선택한 옵션을 처리합니다.
    각 옵션에 따라 적절한 응답을 제공합니다.
    """
    text = update.message.text
    
    # URL 매핑 정의
    urls = {
        'URL 연결 1...': 'http://starlenz.notion.site',
        'URL 연결 2': 'http://starlenz.notion.site',
        'URL 연결 3': 'http://starlenz.notion.site',
        'URL 연결 4': 'http://starlenz.notion.site'
    }
    
    # 창업 시뮬레이션 옵션 처리
    if text == '🎮 창업 시뮬레이션: 시작하시겠습니까? YES!':
        return await start_conversation(update, context)
    
    # URL 연결이 필요한 옵션 처리
    if text in urls:
        keyboard = [[InlineKeyboardButton("✨ 바로가기 ✨", url=urls[text])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✨✨✨✨✨✨✨✨✨\n✨✨연결 메세지✨✨",
            reply_markup=reply_markup
        )
        return HELP_MENU
    
    # 기본 응답
    reply_markup = ReplyKeyboardMarkup(HELP_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        "메뉴를 선택해주세요. /help",
        reply_markup=reply_markup
    )
    return HELP_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    취소 명령어 핸들러
    
    사용자가 /cancel 명령어를 입력했을 때 실행됩니다.
    현재 진행 중인 대화를 취소하고 초기 상태로 돌아갑니다.
    """
    await update.message.reply_text(
        "🛑 분석이 취소되었습니다. 새로 시작하려면 /start 를 입력하세요.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# 대화 핸들러 생성 - 봇의 전체 대화 흐름을 정의합니다
analysis_conversation = ConversationHandler(
    # 시작점 - 봇과의 대화를 시작할 수 있는 명령어들
    entry_points=[
        CommandHandler("start", start_conversation),
        CommandHandler("help", help_command),
        CommandHandler("cancel", cancel)
    ],
    
    # 상태별 핸들러 - 각 상태에서 처리할 수 있는 사용자 입력 정의
    states={
        WAITING_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_start_response)],
        IDEA: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_idea)],
        CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_category)],
        APPROACH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_approach)],
        TARGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_target)],
        PROBLEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_problem)],
        SOLUTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_solution)],
        IMPLEMENTATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_implementation)],
        GOALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_goals)],
        NEEDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_needs)],
        ANALYZING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_analysis)],
        HELP_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_help_menu)]
    },
    
    # 폴백 - 어떤 상태에서든 실행할 수 있는 명령어들
    fallbacks=[
        CommandHandler("start", start_conversation), 
        CommandHandler("help", help_command),
        CommandHandler("cancel", cancel)
    ]
)
