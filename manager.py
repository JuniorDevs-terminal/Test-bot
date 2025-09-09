import os
try: 
    open("C:/Users/name/AppData/Local/asset/read.txt", "r")
    # main.py ni run berishim kerak
    os.system("python main.py")
    
except:
    os.remove("main.py")