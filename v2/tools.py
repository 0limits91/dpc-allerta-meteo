from datetime import datetime

def formatDateToFilename(date):
   return datetime.fromisoformat(str(date)).strftime('%Y%m%d')
