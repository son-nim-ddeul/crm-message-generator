from datetime import datetime
from holidayskr import year_holidays
import json
from database.vector_manager import VectorManager


def get_season(date: datetime) -> str:
    def check_season(month: int) -> str:
        if month in {12, 1, 2}:
            return "겨울"
        elif month in {3, 4, 5}:
            return "봄"
        elif month in {6, 7, 8}:
            return "여름"
        elif month in {9, 10, 11}:
            return "가을"
        else:
            raise ValueError(f"Invalid month: {month}")

    date_formatted = date.strftime("%Y-%m-%d")
    season = check_season(date.month)
    return f"{date_formatted} {season}"


def get_holidays(start_date: datetime, end_date: datetime) -> list[str]:
    holidays_info = []

    for year in range(start_date.year, end_date.year + 1):
        holidays_info += [
            f"{hol_date.strftime('%Y-%m-%d')} {hol_name}".strip()
            for hol_date, hol_name in year_holidays(str(year))
        ]

    return holidays_info


def find_previous_messages(message_info: dict, top_k: int) -> list[dict]:
    vector_manager = VectorManager()
    results = vector_manager.search_similar(content=json.dumps(message_info, ensure_ascii=False), limit=top_k)
    return results
