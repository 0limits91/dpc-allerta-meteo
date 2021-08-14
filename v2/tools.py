
from datetime import date, timedelta, datetime

def formatDateToFilename(date):
   return datetime.fromisoformat(str(date)).strftime('%Y%m%d')

