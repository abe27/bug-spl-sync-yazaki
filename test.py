l = [
    {"factory": "INJ", "receiveno": "TI2021112201", "receivedte": "", "receivepln": 0,},
    {"factory": "INJ", "receiveno": "TI2021112202", "receivedte": "", "receivepln": 0,},
]

n = [item for item in l if item["receiveno"] == "TI2021112203"]
print(len(n))

for a in l:
    print(a)

