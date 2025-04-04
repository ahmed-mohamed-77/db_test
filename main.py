from fastapi import FastAPI, HTTPException, Depends
from database import engine, Weekly_hours, WeekDays, WorkingHours, Base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from func import is_chatbot_active, today_is
import uvicorn


Base.metadata.create_all(engine)

loacal_session = sessionmaker(bind=engine)
Session = loacal_session()
app = FastAPI()


def get_db():
    db = loacal_session()
    try:
        yield db
    finally:
        db.close()
        
# working hours (you can adjust these as needed)
START_TIME = "09:00"  # 9:00 AM
END_TIME = "17:00"    # 6:00 PM

# holiday can be List[str] or str
HOLIDAY = "Sunday"

@app.post("/initialize-working-hours")
def chatbot_working_hours(db = Depends(get_db)):
    try:
        start = datetime.strptime(START_TIME, "%H:%M").time()
        end = datetime.strptime(END_TIME, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid fixed time format")
    
    working_hours = WorkingHours(
        start_time=start,
        end_time=end,
        status=True
    )
    db.add(working_hours)
    db.commit()
    db.refresh(working_hours)
    
    # is chatbot active or not => boolean value
    chatbot_output = is_chatbot_active(holiday=HOLIDAY, start=start, end=end)
    
    today_idx = datetime.today().weekday()
    
    day_output = today_is(today_idx)
    
    new_day = WeekDays(
        day_id = day_output['day_id'],
        days = day_output['today']
    )
    
    try:
        db.add(new_day)
        db.commit()
        db.refresh(new_day)
        
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error inserting weekday entry: {str(e)}"
        )

    if day_output["today"] != HOLIDAY:
        weekly_hours = Weekly_hours(
            week_days_id= new_day.id,
            working_hours_id=working_hours.id
        )
        
    try:
        db.add(weekly_hours)
        db.commit()
        db.refresh(weekly_hours)
        
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error inserting weekday entry: {str(e)}"
        )
    
    
    return {
        "is_chatbot_active": chatbot_output,
        "start_time": START_TIME,
        "end_time": END_TIME,
        "holiday": HOLIDAY,
    }

if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)
