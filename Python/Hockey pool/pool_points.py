action_points_skater = {"G" : 1,
                        "A" : 1,
                        "PPG" : 1,
                        "PPA" : 1,
                        "SHG" : 1,
                        "SHA" : 1,
                        "GWG" : 1,
                        "HIT" : 0.15,
                        "SOG" : 0.15,
                        "+/-" : 1,
                        "BLK" : 0.15}
action_points_goalie = {"SV" : 0.1,
                        "WIN" : 1,
                        "OTW" : 1,
                        "SOW" : 1,
                        "SO" : 2}
                        
players = {"Nikita Kucherov" : ["TB", 41, 87, 24, 15, 33, 0, 0, 8, 246, 31, 44],
           "Johnny Gaudreau" : ["CGY", 36, 63, 18, 6, 21, 0, 0, 8, 245, 12, 12],
           "Drew Doughty"    : ["LAK", 8, 37, -34, 7, 17, 0, 1, 1, 154, 120, 168],
           "Jake Allen"      : ["STL", 1156, 19, 3]      
        
}
class Player:
    #  0     1      2       3      4    5    6    7    8    9   10   11   12
    # name, team, goals, assists, +/-, ppg, ppa, shg, sha, gwg, sog, blk, hit
    # name, team, saves,  wins,    so
    def __init__(self, playerLst) :
        self.name = playerLst[0]
        self.team = playerLst[1]
        if len(playerLst) > 7:
            self.goals = playerLst[2]
            self.assists = playerLst[3]
            self.plus_minus = playerLst[4]
            self.ppg = playerLst[5]
            self.ppa = playerLst[6]
            self.shg = playerLst[7]
            self.sha = playerLst[8]
            self.gwg = playerLst[9]
            self.sog = playerLst[10]
            self.blocks = playerLst[11]
            self.hits = playerLst[12]
            self.skater = True
        else :
            self.saves = playerLst[2]
            self.wins = playerLst[3]
            self.shutouts = playerLst[4]
            self.skater = False
            
        self.pool_points = self.calc_pool_points()
        
    def __repr__(self) :
        return "\t" + self.name + ", " + self.team + " : " + str(self.pool_points)
        
    def calc_pool_points(self) :
        points = 0.0
        action_points = action_points_skater
        if not self.skater:
            action_points = action_points_goalie
            s_p = self.saves * action_points["SV"]
            w_p = self.wins * action_points["WIN"]
            so_p = self.shutouts * action_points["SO"]
            print("\n\ts_p:\t" + str(s_p) +
                  "\n\tw_p:\t" + str(w_p) +
                  "\n\tso_p:\t" + str(so_p))
            points += s_p + w_p + so_p
            return points;
        else :
            g_p = self.goals * action_points["G"]
            a_p = self.assists * action_points["A"]
            pm_p = self.plus_minus * action_points["+/-"]
            ppg_p = self.ppg * action_points["PPG"]
            ppa_p = self.ppa * action_points["PPA"]
            shg_p = self.shg * action_points["SHG"]
            sha_p = self.sha * action_points["SHA"]
            gwg_p = self.gwg * action_points["GWG"]
            sog_p = self.sog * action_points["SOG"]
            blk_p = self.blocks * action_points["BLK"]
            hit_p = self.hits * action_points["HIT"]
            print("\n\tg_p:\t" + str(g_p) +
                  "\n\ta_p:\t" + str(a_p) +
                  "\n\tpm_p:\t" + str(pm_p) +
                  "\n\tppg_p:\t" + str(ppg_p) +
                  "\n\tppa_p:\t" + str(ppa_p) +
                  "\n\tshg_p:\t" + str(shg_p) +
                  "\n\tsha_p:\t" + str(sha_p) +
                  "\n\tgwg_p:\t" + str(gwg_p) +
                  "\n\tsog_p:\t" + str(sog_p) +
                  "\n\tblk_p:\t" + str(blk_p) +
                  "\n\thit_p:\t" + str(hit_p))
            points += g_p + a_p + pm_p + ppg_p + ppa_p + shg_p + sha_p + gwg_p + sog_p + blk_p + hit_p
            return points;
       
Nikita = Player(["Nikita Kucherov"] + players["Nikita Kucherov"])
Johnny = Player(["Johnny Gaudreau"] + players["Johnny Gaudreau"])
Drew = Player(["Drew Doughty"] + players["Drew Doughty"])
Jake = Player(["Jake Allen"] + players["Jake Allen"])
       
print("\n")
print(Nikita)
print(Johnny)
print(Drew)
print(Jake)