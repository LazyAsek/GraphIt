from pathlib import Path
import os

def saveTicker(stock_list,name):
    with open(f"saved_configs\{name}","w") as file :
        for i in range(0,len(stock_list)-1):
            file.write(str(stock_list[i])+"\n")
        file.write(str(stock_list[-1]))

def loadTicker(name):
    with open(f"saved_configs\{name}","r") as file :
        return file.read().strip().split()

def savedNames():
    cur=[]
    for file in Path("saved_configs").iterdir():
        if file.is_file():
            cur.append(file.name)
    return cur

def deleteConfig(name):
    path = os.path.join("saved_configs", name)
    if os.path.exists(path):
        os.remove(path)