import datetime
from time import sleep
start = datetime.datetime.now()
sleep(3)
end = datetime.datetime.now()
diff = end - start
print("Разнциа во времени {} секунд {} микросекунд".format(diff.seconds, diff.microseconds))