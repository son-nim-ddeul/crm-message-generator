from datetime import datetime
from agents.message.sub_agents.performance_estimation.utils import get_betweem_holiday_list

def test_get_betweem_holiday_list_single_year():
    start_date = datetime(2025, 12, 21)
    end_date = datetime(2026, 12, 15)
    
    holidays = get_betweem_holiday_list(start_date, end_date)
    print(holidays)
