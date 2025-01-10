"""
LangChain 서비스 모듈

이 모듈은 Anthropic의 Claude AI를 사용하여 사용자 입력을 분석하고
체계적인 보고서를 생성하는 기능을 제공합니다.

주요 기능:
1. 사용자 입력 정보 정리 및 요약
2. 상세 분석 및 제안 생성
3. 결과 파싱 및 구조화

사용자 정의:
- 프롬프트 템플릿 수정
- 분석 섹션 구성 변경
- 결과 포맷 커스터마이징
"""

import os
import asyncio
from typing import Dict, Optional
import anthropic
from langchain.prompts import ChatPromptTemplate
import warnings

# SQLite 관련 경고 무시
warnings.filterwarnings('ignore', category=UserWarning, module='langchain')

class LangChainService:
    """
    LangChain 서비스 클래스
    
    이 클래스는 AI 분석 기능의 핵심 로직을 구현합니다.
    Anthropic의 Claude AI를 사용하여 두 단계로 분석을 수행합니다:
    1단계: 기본 정보 정리 및 요약
    2단계: 상세 분석 및 제안
    """
    def __init__(self):
        """
        서비스 초기화
        
        필요한 설정:
        1. ANTHROPIC_API_KEY 환경 변수
        2. Claude AI 모델 선택
        3. 프롬프트 템플릿 구성
        
        프롬프트 템플릿은 분석의 품질과 일관성을 결정하는 중요한 요소입니다.
        필요에 따라 템플릿을 수정하여 다른 용도로 활용할 수 있습니다.
        """
        # Anthropic API 키 확인
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        
        # Anthropic 클라이언트 설정
        self.client = anthropic.Client(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"
        
        # 1단계: 기본 정보 정리 및 요약
        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 전문적인 분석가입니다.
            제공된 정보를 바탕으로 명확하고 체계적인 분석 보고서를 작성해주세요.
            
            다음 형식을 정확히 따라주세요:
            
            # 제목
            [한 줄로 5단어 이내]
            
            # 핵심 내용
            [한 줄로 10단어 이내]
            
            # 상세 설명
            [3-4문장으로 주요 특징과 장점을 설명]
            
            # 배경 분석
            - 현재 상황: [현재 상태 한 줄 설명]
            - 해결 방안: [한 줄로 설명]
            - 차별점: [한 줄로 설명]
            - 범위: [대상/규모를 구체적으로 설명]
            
            # 실행 계획
            [3-4문장으로 구현 방법과 필요한 자원을 설명]
            
            # 기대 효과
            - 주요 효과: [한 줄로 설명]
            - 부가 효과: [한 줄로 설명]
            - 지속성: [한 줄로 설명]
            
            주의사항:
            1. 각 섹션의 제목은 반드시 '# ' 으로 시작
            2. 리스트 항목은 반드시 '- ' 으로 시작
            3. 모든 내용은 들여쓰기 없이 작성
            4. 빈 줄은 섹션 구분에만 사용
            5. 구체적인 예시와 수치 포함"""),
            
            ("human", """아이디어: {idea}
            분야: {category}
            형태: {approach}
            타겟: {target}
            문제: {problem}
            해결방안: {solution}
            구현기술: {implementation}
            목표: {goals}
            필요사항: {needs}""")
        ])
        
        # 2단계: 상세 분석 및 제안
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 전문적인 컨설턴트입니다.

            1단계에서 정리된 내용을 바탕으로 상세 분석을 수행하고 제안을 해주세요.

            다음 형식으로 응답해주세요:

            # 유사 사례
            - [사례 1]: 특징, 분야, 성공/실패 요인
            - [사례 2]: 특징, 분야, 성공/실패 요인
            - [사례 3]: 특징, 분야, 성공/실패 요인

            # 실현 가능성
            - 기술: [필요한 기술과 난이도]
            - 자원: [필요한 자원]
            - 기간: [예상 소요 기간]
            - 제약: [예상되는 어려움]

            # 발전 방향
            - 단기: [1-3개월 목표]
            - 중기: [3-6개월 목표]
            - 장기: [6개월 이상 목표]
            - 계획: [실행 단계]

            # 개선 사항
            - 보완점: [주요 보완 사항]
            - 방안: [개선 방법]
            - 주의점: [고려 사항]
            - 효과: [예상 효과]

            주의사항:
            1. 각 섹션은 반드시 '# '으로 시작
            2. 모든 항목은 반드시 '- '으로 시작
            3. 빈 줄은 섹션 구분에만 사용
            4. 실제 글로벌 벤처투자 사례와 데이터에 기반하여 구체적인 수치와 전략을 제시"""),
            
            ("human", """사업계획서 요약: {summary}""")
        ])

    def _get_summary(self, data):
        """
        1단계: 기본 정보 정리 및 요약
        
        입력된 데이터를 바탕으로 구조화된 요약을 생성합니다.
        
        Args:
            data (Dict): 사용자 입력 데이터
                - idea: 아이디어 설명
                - category: 서비스 분야
                - approach: 접근 방식
                - target: 목표 고객
                - problem: 해결할 문제
                - solution: 해결 방안
                - implementation: 구현 방식
                - goals: 목표
                - needs: 필요 사항
        
        Returns:
            str: 구조화된 요약 텍스트
        """
        response = self.client.messages.create(
            model=self.model,
            system=self.summary_prompt.messages[0].prompt.template,
            messages=[
                {"role": "user", "content": self.summary_prompt.messages[1].prompt.template.format(**data)}
            ],
            max_tokens=4000
        )
        return response.content[0].text

    def _get_analysis(self, summary):
        """
        2단계: 상세 분석 및 제안
        
        1단계에서 생성된 요약을 바탕으로 상세 분석을 수행합니다.
        
        분석 섹션:
        1. 유사 사례: 참고할 만한 실제 사례들
        2. 실현 가능성: 기술적/자원적 관점의 분석
        3. 발전 방향: 단기/중기/장기 목표
        4. 개선 사항: 보완이 필요한 부분과 방안
        
        Args:
            summary (str): 1단계에서 생성된 요약
            
        Returns:
            str: 상세 분석 결과 텍스트
        """
        response = self.client.messages.create(
            model=self.model,
            system=self.analysis_prompt.messages[0].prompt.template,
            messages=[
                {"role": "user", "content": f"사업계획서 요약: {summary}"}
            ],
            max_tokens=4000
        )
        return response.content[0].text

    async def debug_chain(self, data: Dict) -> None:
        try:
            summary_result = await asyncio.to_thread(self._get_summary, data)
            print("\n=== Summary Chain Result ===")
            print(f"Content: {summary_result}")
            
            analysis_result = await asyncio.to_thread(self._get_analysis, summary_result)
            print("\n=== Analysis Chain Result ===")
            print(f"Content: {analysis_result}")
            
        except Exception as e:
            print(f"\n=== Chain Debug Error ===")
            print(f"Error: {e}")
            print(f"Error Type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

    def _parse_section_content(self, content: str) -> list:
        """
        섹션 내용을 리스트 형태로 파싱
        
        AI가 생성한 텍스트를 구조화된 형태로 변환합니다.
        
        파싱 규칙:
        1. 각 줄을 개별 항목으로 처리
        2. '- '로 시작하는 줄은 리스트 항목으로 처리
        3. 콜론(:)이 있는 경우 레이블과 값으로 분리
        4. 빈 줄은 무시
        
        Args:
            content (str): 파싱할 텍스트
            
        Returns:
            list: 파싱된 항목들의 리스트
        """
        if not content:
            return []
        
        # 줄바꿈으로 분리하고 빈 줄 제거
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # 결과 저장용 리스트
        result = []
        
        for line in lines:
            # 새로운 항목 시작 확인
            if line.startswith('- '):
                # 콜론이 있는 경우 처리
                if ':' in line:
                    label, value = line[2:].split(':', 1)
                    result.append(f"# {label.strip()}")
                    if value.strip():
                        result.append(f"- {value.strip()}")
                else:
                    result.append(line)
            # 일반 텍스트는 리스트 항목으로 변환
            else:
                result.append(f"- {line.strip()}")
        
        # 빈 문자열 제거
        result = [item.strip() for item in result if item.strip()]
        
        return result

    async def analyze_startup(self, data: Dict) -> Optional[Dict]:
        """스타트업 분석 수행"""
        try:
            # 디버깅 실행
            await self.debug_chain(data)

            # 체인 실행
            print("\n=== Chain Execution ===")
            summary = await asyncio.to_thread(self._get_summary, data)
            analysis = await asyncio.to_thread(self._get_analysis, summary)
            
            # 결과를 직접 구성
            analysis_result = {
                'summary': summary,
                'case_studies': [],
                'feasibility': [],
                'development_plan': [],
                'improvements': []
            }
            
            # 섹션 매핑 정의
            section_mapping = {
                '유사 사례': 'case_studies',
                '실현 가능성': 'feasibility',
                '발전 방향': 'development_plan',
                '개선 사항': 'improvements'
            }
            
            # 분석 결과 파싱
            current_section = None
            current_content = []
            
            print("\n=== Parsing Analysis Result ===")
            
            for line in analysis.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('# '):
                    # 이전 섹션의 내용을 처리
                    if current_section and current_content:
                        parsed_content = self._parse_section_content('\n'.join(current_content))
                        if current_section in section_mapping:
                            mapped_section = section_mapping[current_section]
                            print(f"\nProcessing section: {current_section} -> {mapped_section}")
                            print(f"Parsed content: {parsed_content}")
                            analysis_result[mapped_section] = parsed_content
                    
                    # 새로운 섹션 시작
                    current_section = line[2:].strip()
                    print(f"\nNew section: {current_section}")
                    current_content = []
                else:
                    current_content.append(line)
                    print(f"Added content: {line}")
            
            # 마지막 섹션 처리
            if current_section and current_content:
                parsed_content = self._parse_section_content('\n'.join(current_content))
                if current_section in section_mapping:
                    mapped_section = section_mapping[current_section]
                    print(f"\nProcessing final section: {current_section} -> {mapped_section}")
                    print(f"Parsed content: {parsed_content}")
                    analysis_result[mapped_section] = parsed_content

            # 원본 입력 데이터를 결과에 포함
            analysis_result.update({
                'idea': data.get('idea', ''),
                'category': data.get('category', ''),
                'approach': data.get('approach', ''),
                'target': data.get('target', ''),
                'problem': data.get('problem', ''),
                'solution': data.get('solution', ''),
                'implementation': data.get('implementation', ''),
                'goals': data.get('goals', ''),
                'needs': data.get('needs', '')
            })
            
            return analysis_result
            
        except Exception as e:
            print(f"분석 중 오류 발생: {e}")
            return None
