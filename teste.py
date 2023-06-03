
from datetime import datetime
from datetime import date
dia1 = date.today().strftime('%d-%m-%Y')
hora1 = datetime.now().strftime('%H:%M')
print(dia1)
print(hora1)