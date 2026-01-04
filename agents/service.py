import json
import logging
from typing import Optional
from pathlib import Path


logger = logging.getLogger(__name__)


def __load_personas() -> Optional[list[dict]]:
    """JSON 파일에서 페르소나 데이터를 로드합니다."""
    script_dir = Path(__file__).parent
    filename = script_dir / "persona_example.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['personas']
    except FileNotFoundError:
        logger.exception(msg=f"오류: '{filename}' 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        logger.exception(msg=f"오류: '{filename}' 파일의 JSON 형식이 올바르지 않습니다.")
        return None

def find_persona_by_id(persona_id: str) -> Optional[dict]:
    """persona_id로 특정 페르소나를 검색합니다."""
    personas = __load_personas()
    
    if personas is None:
        return None
    
    for persona in personas:
        if persona.get('persona_id') == persona_id:
            return persona
    return None

def format_persona(persona: dict) -> str:
    name = persona.get("name", "Unknown")
    age = persona.get("age", "N/A")
    occupation = persona.get("occupation", "N/A")
    shopping_pattern = ', '.join(persona.get("shopping_pattern", []))
    preferences = ', '.join(persona.get("preferences", []))
    lifestyle = ', '.join(persona.get("lifestyle", []))
    pain_points = ', '.join(persona.get("pain_points", []))
    customer_journey = persona.get("customer_journey", "N/A")
    template = f"""
- name : {name}
- age : {age}
- occupation : {occupation}
- shopping_pattern : {shopping_pattern}
- preferences : {preferences}
- lifestyle : {lifestyle}
- pain_points : {pain_points}
- customer_journey : {customer_journey}
"""
    return template