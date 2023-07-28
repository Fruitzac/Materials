import csv
import random

with open("Astock.csv",'w', newline="") as w:
    for i in range(1000):
        writer = csv.writer(w,delimiter= ",")
        writer.writerow([round(random.uniform(1,1000),1)] + [round(random.uniform(1,1000),1)] + [round(random.uniform(1,1000),1)])
        
        