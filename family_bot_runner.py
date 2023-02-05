from main import main
import traceback
import time
from datetime import datetime as dt

while True:
    try:
        print(f"Started {dt.now()}")
        main()
        print(f"Finished {dt.now()}")
        time.sleep(60)
    except Exception:
        print(traceback.format_exc())



# if __name__ == "__main__":
#     pass
