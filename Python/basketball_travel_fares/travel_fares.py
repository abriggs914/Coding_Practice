import math

fares =  {  "Oromocto": {"fare": 15, "distance" : 21.5},
            "Base Gagetown": {"fare": 15, "distance": 25.8},
            "Keswick Ridge": {"fare": 19, "distance": 23.2},
            "Keswick Valley": {"fare": 22, "distance": 29.5},
            "Fredericton Junction": {"fare": 30, "distance": 36.6},
            "Harvey": {"fare": 35, "distance": 49.2},
            "Stanley": {"fare": 38, "distance": 42.6},
            "Minto": {"fare": 38, "distance": 65.3},
            "Gagetown": {"fare": 45, "distance": 58.2},
            "Nackawic": {"fare": 48, "distance": 63.9},
            "Cambridge Narrows": {"fare": 53, "distance": 68.8},
            "Chipman": {"fare": 57, "distance": 91.7},
            "Central NB Academy": {"fare": 60, "distance": 76.9}
                                
}
            
for location, fare_data in fares.items() :
    p = fare_data["fare"]
    d = fare_data["distance"]
    p_km = p / d
    l = len(location)
    for i in range(min(21, l), 21) :
        location += " "
    print("\t$" + str(p) + " for going to " + location + " " + str(d) + " km, ratio: " + str(p_km) + " $ / km.")