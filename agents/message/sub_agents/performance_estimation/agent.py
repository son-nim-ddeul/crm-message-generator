from google.adk.agents import ParallelAgent
from .pipeline import (
    aspirational_dreamer_estimation,
    empathetic_supporter_estimation,
    playful_entertainer_estimation,
    rational_advisor_estimation
)

# ParrellAgent - message_type 별 이전 작성된 콘텐츠는 state에 저장되어 있음
# 1. before_agent_callback : 각 메시지 바탕으로 RAG 조회 시작 TOP-K : 5
# => 조회된 내용을 알고리즘에 맞게 (기획서 참고) 포맷팅하여 state에 관리 -> {message_type}_estimation
#  => 발송 일자 날짜, 근접 공휴일 (전후), 계절, 분기 데이터 조회 Tool 추가
#  => https://github.com/dr-prodigy/python-holidays / 나머지는 직접 구현
# => 병렬적으로 도는 strategic_estimation_agent는 {message_type}_estimation를 프롬프트에 injection
# => 만약 조회된 결과가 없거나 유사도가 너무 낮다면 평가할 수 있는 이력이 없습니다를 반환
# => 최종적으로 유사도, 주요 마케팅성과, 날짜데이터 기반으로 현재 콘텐츠가 어떻게 마케팅 성과를 낼것 같은지 예측 + 추가적으로 어떤 것이 있으면 좋은지 결과 반환
performance_estimation_agent = ParallelAgent(
    name="performance_estimation_agent",
    description="각 전략별 마케팅 예상 성과를 추측합니다.",
    sub_agents=[
        aspirational_dreamer_estimation,
        empathetic_supporter_estimation,
        playful_entertainer_estimation,
        rational_advisor_estimation
    ]
)
