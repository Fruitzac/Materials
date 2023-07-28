import math

def makebars(value,maxvalue, barnumber):
    barvalue = maxvalue / barnumber
    neededbars = math.ceil(value / barvalue)
    airbars = barnumber - neededbars
    return f"[{neededbars*'=' + airbars*' '}]"

print(makebars(139,150, 25))

