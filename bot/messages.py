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
    
    # 웰컴 이미지 URL
    WELCOME_IMG_URL = "https://imagedelivery.net/csS3I11UbX4B6HoDdrP-iA/8f3411e9-f364-416f-d0d2-0c5e851aad00/public"
    
    # 웰컴 메시지
    WELCOME_MESSAGE = """
📝 특허 기술명세서 작성 도우미

📍 이런 분들에게 추천합니다:
🔹 신규 특허 출원을 준비 중이신 분
🔹 기술 아이디어를 체계화하고 싶으신 분
🔹 특허 명세서 초안 작성이 필요하신 분

📍 진행 방법:
1️⃣ 기술 개요 설명 (자유 입력)
2️⃣ 10개 핵심 항목 작성 (버튼/텍스트 입력)
3️⃣ AI 기반 명세서 초안 생성

📍 명령어:
🔹 /start : 새로운 명세서 작성
🔹 /cancel : 작성 취소
🔹 /help : 도움말

📍 소요시간: 5-7분

📋 "시작하기"를 선택해주세요!"""

    # 분석 시작 메시지
    ANALYSIS_START = """
⚙️ 입력된 기술 정보를 분석중입니다...

🤖 AI가 특허 명세서 초안을 작성합니다.

📝 기술적 특징과 청구범위를 체계화하는 중...

⏱️ 잠시만 기다려주세요.
"""

    # 질문 목록
    QUESTIONS = {
        # 기술 개요 입력
        'idea': """
💡 발명하신 기술을 간단히 설명해주세요.

TIP: 핵심 기능과 특징을 중심으로 설명해주세요.
예시: "스마트폰 화면 지문인식 기술", "AI 기반 실시간 번역 시스템"
""",
        
        # 기술적 문제점
        'problem': """
❗ 해결하고자 하는 기술적 문제점은 무엇인가요?

TIP: 기존 기술의 한계나 개선이 필요한 부분을 설명해주세요.
""",
        
        # 핵심 작동 원리
        'mechanism': """
⚙️ 핵심 작동 원리와 메커니즘을 설명해주세요.

TIP: 기술의 동작 과정과 주요 구성요소를 설명해주세요.
""",
        
        # 기존 기술과의 차별점
        'difference': """
✨ 기존 기술과 비교했을 때의 차별점은 무엇인가요?

TIP: 기술적 우위성과 혁신성을 중심으로 설명해주세요.
""",
        
        # 구성요소와 작동 방식
        'components': """
🔧 주요 구성요소와 세부 작동 방식을 설명해주세요.

TIP: 각 부품/모듈의 기능과 상호작용을 설명해주세요.
""",
        
        # 기술적 효과
        'effects': """
📈 본 기술 적용시 얻을 수 있는 효과는 무엇인가요?

TIP: 정량적/정성적 개선 효과를 설명해주세요.
""",
        
        # 기술적 한계
        'limitations': """
⚠️ 예상되는 기술적 한계나 제약사항은 무엇인가요?

TIP: 현재 해결이 필요한 문제점을 설명해주세요.
""",
        
        # 산업 분야
        'industry': """
🏭 적용 가능한 산업분야는 어디인가요?

TIP: 구체적인 활용 분야와 시장을 설명해주세요.
""",
        
        # 물리적 특성
        'specifications': """
📐 기술의 물리적 특성 및 상세 스펙을 설명해주세요.

TIP: 크기, 성능, 정확도 등 수치화 가능한 특성을 설명해주세요.
""",
        
        # 개발 상태
        'status': """
🔍 현재 기술의 개발 진행 상태는 어떠한가요?

TIP: 개발 단계와 검증 현황을 설명해주세요.
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
        message_parts = ["📝 특허 명세서 초안이 작성되었습니다!", ""]

        # 요약 섹션 포맷팅
        message_parts.extend(["📋 기술 요약:"])
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
            message_parts.extend(["", "📚 선행기술 분석:"])
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
            message_parts.extend(["", "⚙️ 기술적 실현성:"])
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
            message_parts.extend(["", "📈 기술 발전성:"])
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
            message_parts.extend(["", "🔧 보완 사항:"])
            for item in improvements:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        return "\n".join(message_parts)
