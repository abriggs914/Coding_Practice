
AVERY = "A"
KRISTEN = "K"
EMILY = "E"
HAYLEY = "H"
MOM = "M"
DAD = "D"

def who_pays(payee):
    payers = []
    for let in payee:
        if let == AVERY:
            payers.append(AVERY)
        elif let == KRISTEN:
            payers.append(KRISTEN)
        elif let == EMILY:
            payers.append(EMILY)
        elif let == HAYLEY:
            payers.append(HAYLEY)
        elif let == MOM:
            payers.append(MOM)
        elif let == DAD:
            payers.append(DAD)