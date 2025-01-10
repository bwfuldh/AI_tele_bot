"""
메시지 포맷팅 모듈

이 모듈은 텔레그램 봇의 모든 메시지 템플릿을 관리합니다.
봇의 성격과 목적에 맞게 메시지를 커스터마이징할 수 있습니다.

주요 구성:
1. 웰컴 메시지와 이미지
2. 질문 목록과 설명
3. 분석 결과 포맷팅

사용자 정의:
- 메시지 톤과 스타일
- 이모지 사용
- 설명 방식
"""

class ElonStyleMessageFormatter:
    """
    메시지 포맷팅 클래스
    
    봇과 사용자 간의 모든 상호작용에 사용되는 메시지를 정의합니다.
    메시지의 톤, 이모지 사용, 설명 방식 등을 일관되게 유지합니다.
    """
    
    # 웰컴 이미지 URL - 자신의 브랜드에 맞는 이미지로 변경하세요
    WELCOME_IMG_URL = "https://imagedelivery.net/csS3I11UbX4B6HoDdrP-iA/051ec1a7-9cff-4ad1-8c4b-9a55a0173700/public"
    
    # 웰컴 메시지 - 봇의 목적과 사용 방법을 명확하게 설명하세요
    WELCOME_MESSAGE = """
✨ 아이디어 분석 도우미

📍 이런 분들에게 추천해요:
🔹 새로운 서비스를 기획 중이신 분
🔹 아이디어를 구체화하고 싶으신 분
🔹 프로젝트를 시작하려는 분

📍 진행 방법:
1️⃣ 아이디어 설명 (자유 입력)
2️⃣ 8개 항목 선택 (버튼 클릭)
3️⃣ AI 분석 결과 확인

📍 명령어:
🔹 /start : 새로운 분석 시작
🔹 /cancel : 분석 취소
🔹 /help : 도움말

📍 소요시간: 3-5분

✨ "시작하기"를 선택해주세요!"""

    # 분석 시작 메시지 - 사용자에게 진행 상황을 알려주는 메시지입니다
    ANALYSIS_START = """
⚙️ 입력된 정보를 분석중입니다...

🤖 AI가 분석을 시작합니다.

⏱️ 잠시만 기다려주세요.
"""

    # 질문 목록 - 각 단계별 질문과 설명을 정의합니다
    QUESTIONS = {
        # 아이디어 입력 - 자유 형식으로 입력받는 유일한 질문입니다
        'idea': """
💡 어떤 아이디어를 가지고 계신가요?

TIP: 구체적으로 설명해주세요.
예시: 반려동물 산책 매칭 앱, 온라인 스터디 플랫폼
""",
        
        # 서비스 분야 선택 - 아이디어의 카테고리를 정의합니다
        'category': """
🎯 어떤 분야의 서비스인가요?

위 카테고리 중에서 선택해주세요.
""",
        
        # 서비스 형태 선택 - 비즈니스 모델을 정의합니다
        'approach': """
📝 어떤 형태의 서비스인가요?

위 서비스 형태 중에서 선택해주세요.
""",
        
        # 타겟 고객 선택 - 주요 사용자층을 정의합니다
        'target': """
👥 주요 타겟층은 누구인가요?

위 대상 중에서 선택해주세요.
""",
        
        # 해결할 문제 선택 - 서비스의 가치 제안을 정의합니다
        'problem': """
❓ 어떤 문제를 해결하나요?

위 문제 유형 중에서 선택해주세요.
""",
        
        # 해결 방식 선택 - 문제 해결 접근 방법을 정의합니다
        'solution': """
💡 어떤 방식으로 해결하나요?

위 해결 방식 중에서 선택해주세요.
""",
        
        # 구현 기술 선택 - 필요한 기술 스택을 정의합니다
        'implementation': """
🛠️ 어떤 기술로 구현하나요?

위 기술 스택 중에서 선택해주세요.
""",
        
        # 목표 선택 - 단기적인 성과 지표를 정의합니다
        'goals': """
🎯 주요 목표는 무엇인가요?

위 목표 중에서 선택해주세요.
""",
        
        # 필요 사항 선택 - 현재 가장 시급한 요구사항을 정의합니다
        'needs': """
📋 현재 가장 필요한 것은?

위 항목 중에서 선택해주세요.
"""
    }

    @staticmethod
    def format_analysis_result(result: dict) -> str:
        """
        분석 결과를 포맷팅하는 메서드
        
        AI가 생성한 분석 결과를 사용자가 읽기 쉬운 형태로 변환합니다.
        
        포맷팅 규칙:
        1. 섹션 구분을 위한 이모지 사용
        2. 중요 포인트는 글머리 기호로 강조
        3. 계층 구조를 들여쓰기로 표현
        
        Args:
            result (dict): AI 분석 결과 데이터
                - summary: 전체 요약
                - case_studies: 유사 사례 분석
                - feasibility: 실현 가능성 평가
                - development_plan: 발전 계획
                - improvements: 개선 제안
                
        Returns:
            str: 포맷팅된 분석 결과 텍스트
        """
        if not result or not isinstance(result, dict):
            return "분석 중 오류가 발생했습니다."

        # 섹션별 데이터 추출
        summary = result.get('summary', '분석 중...')
        case_studies = result.get('case_studies', [])
        feasibility = result.get('feasibility', [])
        development_plan = result.get('development_plan', [])
        improvements = result.get('improvements', [])

        # 메시지 구성
        message_parts = ["✨ 분석이 완료되었습니다!", ""]

        # 요약 섹션 포맷팅
        message_parts.extend(["📝 아이디어 분석:"])
        for line in summary.split('\n'):
            line = line.strip()
            if line:
                if line.startswith('# '):
                    current_subsection = line[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif line.startswith('- '):
                    message_parts.append(f"• {line[2:].strip()}")
                else:
                    message_parts.append(line)

        # 유사 사례 섹션 포맷팅
        if case_studies:
            message_parts.extend(["", "🔍 유사 사례:"])
            for item in case_studies:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        # 실현 가능성 섹션 포맷팅
        if feasibility:
            message_parts.extend(["", "⚡ 실현 가능성:"])
            for item in feasibility:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        # 발전 방향 섹션 포맷팅
        if development_plan:
            message_parts.extend(["", "🎯 발전 방향:"])
            for item in development_plan:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        # 개선 사항 섹션 포맷팅
        if improvements:
            message_parts.extend(["", "💡 개선 사항:"])
            for item in improvements:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        return "\n".join(message_parts)
