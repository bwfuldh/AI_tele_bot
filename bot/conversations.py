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

# 대화 상태 정의
(WAITING_START,
 IDEA,           # 기술 개요 (자유 입력)
 PROBLEM,        # 기술적 문제점
 MECHANISM,      # 핵심 작동 원리
 DIFFERENCE,     # 기존 기술과의 차별점
 COMPONENTS,     # 구성요소와 작동 방식
 EFFECTS,        # 기술적 효과
 LIMITATIONS,    # 기술적 한계
 INDUSTRY,       # 산업 분야
 SPECIFICATIONS, # 물리적 특성
 STATUS,         # 개발 상태
 ANALYZING,      # AI 분석 중
 HELP_MENU) = range(13)

# 키보드 메뉴 정의

# 문제점 유형 선택 옵션
PROBLEM_KEYBOARD = [
    ['🔧 성능/효율성', '💡 기술적 한계'],
    ['⚡ 에너지/자원', '🔒 보안/안전성'],
    ['💰 비용/생산성', '🌍 환경 영향'],
    ['✨ 직접 입력']
]

# 작동 원리 선택 옵션
MECHANISM_KEYBOARD = [
    ['⚙️ 기계/물리', '🔌 전기/전자'],
    ['💻 소프트웨어', '🤖 AI/데이터'],
    ['🧪 화학/생물', '📡 통신/네트워크'],
    ['✨ 직접 입력']
]

# 차별점 선택 옵션
DIFFERENCE_KEYBOARD = [
    ['📈 성능 향상', '💰 비용 절감'],
    ['⚡ 효율 개선', '🔒 안전성 강화'],
    ['🌟 혁신 기술', '♻️ 지속가능성'],
    ['✨ 직접 입력']
]

# 구성요소 선택 옵션
COMPONENTS_KEYBOARD = [
    ['🔧 기계 부품', '🔌 전자 부품'],
    ['💾 제어 장치', '📱 인터페이스'],
    ['🧮 프로세서', '💽 저장 장치'],
    ['✨ 직접 입력']
]

# 기술 효과 선택 옵션
EFFECTS_KEYBOARD = [
    ['⚡ 효율 증가', '💰 비용 감소'],
    ['🔒 안전성 향상', '♻️ 환경 개선'],
    ['📈 성능 향상', '🌟 품질 개선'],
    ['✨ 직접 입력']
]

# 기술 한계 선택 옵션
LIMITATIONS_KEYBOARD = [
    ['💰 높은 비용', '⚡ 전력 소비'],
    ['🌡️ 온도 제약', '⏱️ 처리 속도'],
    ['🔒 보안 위험', '🔧 유지보수'],
    ['✨ 직접 입력']
]

# 산업 분야 선택 옵션
INDUSTRY_KEYBOARD = [
    ['🏭 제조/생산', '🔌 전기/전자'],
    ['🚗 자동차/운송', '🏥 의료/바이오'],
    ['🌍 환경/에너지', '🤖 IT/소프트웨어'],
    ['✨ 직접 입력']
]

# 물리적 특성 선택 옵션
SPECIFICATIONS_KEYBOARD = [
    ['📏 크기/무게', '⚡ 전력/성능'],
    ['🌡️ 온도/환경', '⏱️ 속도/정확도'],
    ['🔧 내구성/수명', '🔌 호환성/규격'],
    ['✨ 직접 입력']
]

# 개발 상태 선택 옵션
STATUS_KEYBOARD = [
    ['💡 개념 설계', '📝 상세 설계'],
    ['🛠️ 시제품 제작', '🔬 성능 검증'],
    ['📊 시험 평가', '📋 특허 출원'],
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
    기술 개요 입력 처리 핸들러
    
    사용자가 입력한 기술 설명을 저장하고
    다음 단계(기술적 문제점)로 진행합니다.
    """
    context.user_data['idea'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(PROBLEM_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['problem'],
        reply_markup=reply_markup
    )
    return PROBLEM

async def handle_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    기술적 문제점 처리 핸들러
    
    사용자가 선택한 문제점을 저장하고
    다음 단계(핵심 작동 원리)로 진행합니다.
    """
    context.user_data['problem'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(MECHANISM_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['mechanism'],
        reply_markup=reply_markup
    )
    return MECHANISM

async def handle_mechanism(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    핵심 작동 원리 처리 핸들러
    
    사용자가 선택한 작동 원리를 저장하고
    다음 단계(기존 기술과의 차별점)로 진행합니다.
    """
    context.user_data['mechanism'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(DIFFERENCE_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['difference'],
        reply_markup=reply_markup
    )
    return DIFFERENCE

async def handle_difference(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    차별점 처리 핸들러
    
    사용자가 선택한 차별점을 저장하고
    다음 단계(구성요소와 작동 방식)로 진행합니다.
    """
    context.user_data['difference'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(COMPONENTS_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['components'],
        reply_markup=reply_markup
    )
    return COMPONENTS

async def handle_components(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    구성요소 처리 핸들러
    
    사용자가 선택한 구성요소를 저장하고
    다음 단계(기술적 효과)로 진행합니다.
    """
    context.user_data['components'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(EFFECTS_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['effects'],
        reply_markup=reply_markup
    )
    return EFFECTS

async def handle_effects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    기술적 효과 처리 핸들러
    
    사용자가 선택한 효과를 저장하고
    다음 단계(기술적 한계)로 진행합니다.
    """
    context.user_data['effects'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(LIMITATIONS_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['limitations'],
        reply_markup=reply_markup
    )
    return LIMITATIONS

async def handle_limitations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    기술적 한계 처리 핸들러
    
    사용자가 선택한 한계를 저장하고
    다음 단계(산업 분야)로 진행합니다.
    """
    context.user_data['limitations'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(INDUSTRY_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['industry'],
        reply_markup=reply_markup
    )
    return INDUSTRY

async def handle_industry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    산업 분야 처리 핸들러
    
    사용자가 선택한 산업 분야를 저장하고
    다음 단계(물리적 특성)로 진행합니다.
    """
    context.user_data['industry'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(SPECIFICATIONS_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['specifications'],
        reply_markup=reply_markup
    )
    return SPECIFICATIONS

async def handle_specifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    물리적 특성 처리 핸들러
    
    사용자가 선택한 특성을 저장하고
    다음 단계(개발 상태)로 진행합니다.
    """
    context.user_data['specifications'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(STATUS_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['status'],
        reply_markup=reply_markup
    )
    return STATUS

async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    개발 상태 처리 핸들러
    
    사용자가 선택한 개발 상태를 저장하고
    AI 분석을 시작합니다.
    """
    context.user_data['status'] = update.message.text
    
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

# 대화 핸들러 생성
analysis_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_conversation),
        CommandHandler("help", help_command),
        CommandHandler("cancel", cancel)
    ],
    
    states={
        WAITING_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_start_response)],
        IDEA: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_idea)],
        PROBLEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_problem)],
        MECHANISM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mechanism)],
        DIFFERENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_difference)],
        COMPONENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_components)],
        EFFECTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_effects)],
        LIMITATIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_limitations)],
        INDUSTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_industry)],
        SPECIFICATIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_specifications)],
        STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_status)],
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
