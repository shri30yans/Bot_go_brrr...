from datetime import datetime 
import pytz 

IST = pytz.timezone('Asia/Kolkata') 

datetime_ist = datetime.now(IST) 
hour = datetime_ist.hour
print(hour)
if hour > 23 or hour < 10:#if time between 12 AM and 10 AM
    print( False)
else:
    print( True)