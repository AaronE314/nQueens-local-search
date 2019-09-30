Dict = {}
value = Dict.setdefault("Value")
if value == None:
    Dict["Value"] = True
    print("RIGHT HERE")
else : 
    print(Dict["Value"])

value = Dict.setdefault("Value")
if value == None:
    Dict[value] = True
    print("RIGHT HERE")
else : 
    print(Dict["Value"])