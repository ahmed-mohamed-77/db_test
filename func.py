from datetime import datetime
from typing import Union

def is_chatbot_active(holiday: Union[str, list], start: str, end: str) -> bool:
    current_day = datetime.today().strftime("%A")
    current_hour = datetime.now().hour
    start = str(start)
    start = int(start.split(":")[0])
    end = str(end)
    end = int(end.split(":")[0])

    # Check if today is a holiday
    if isinstance(holiday, list) and current_day in holiday:
        return True
    elif isinstance(holiday, str) and current_day == holiday:
        return True
    
    if current_day != holiday and start < current_hour < end:
        return False  # Disable during working hours
    return True


def today_is(day_no: int):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    seed = []
    
    for i, day in enumerate(weekdays, start=0):
        seed.append({"day_id": i, "today":day})
    
    return seed[day_no]
