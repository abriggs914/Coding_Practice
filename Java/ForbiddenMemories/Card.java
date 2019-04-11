public class Card{

  public int id;
  public String name;
  public String type;
  public String attribute;
  public int cost;
  public int atkPoints;
  public int defPoints;
  public String planet1;
  public String planet2;
  public String starSign;
  public String playState;

  public Card (int id, String name, String type, String attribute,
               int cost, int atkPoints, int defPoints, String planet1,
               String planet2){
    this.id = id;
    this.name = name;
    this.type = type;
    this.attribute = attribute;
    this.cost = cost;
    this.atkPoints = atkPoints;
    this.defPoints = defPoints;
    this.planet1 = planet1;
    this.planet2 = planet2;
  }

  public Card (int id, String name, String type, String attribute,
               int cost, int atkPoints, int defPoints, String planet1,
               String planet2, String playState, String starSign){
    this.id = id;
    this.name = name;
    this.type = type;
    this.attribute = attribute;
    this.cost = cost;
    this.atkPoints = atkPoints;
    this.defPoints = defPoints;
    this.planet1 = planet1;
    this.planet2 = planet2;
    this.playState = playState;
    this.starSign = starSign;
  }

  public int compareTo(Card b){
    int atkP_A = this.atkPoints;
    int atkP_B = b.atkPoints;
    if(atkP_A - atkP_B != 0){
      if(atkP_A >= atkP_B){
        return 1;
      }
      else{
        return 0;
      }
    }
    else{
      int defP_A = this.defPoints;
      int defP_B = b.defPoints;
      if(defP_A >= defP_B){
        return 1;
      }
      else{
        return 0;
      }
    }
  }

  public void setStarSignPlay(String planet) throws CardException{
    if(this.planet1.equals(planet)){
      return;
    }
    else if(this.planet2.equals(planet)){
      String temp = this.planet1;
      this.planet1 = this.planet2;
      this.planet2 = temp;
      return;
    }
    else{
      throw new CardException("IVSS");
    }
  }

  public void starSignInFavour(){
    this.atkPoints += 500;
    this.defPoints += 500;
  }

  public void starSignAgainst(){
    this.atkPoints -= ((this.atkPoints >= 500)? 500 : this.atkPoints);
    this.defPoints -= ((this.defPoints >= 500)? 500 : this.defPoints);
  }

  public void fieldInFavour(){
    this.atkPoints += 500;
    this.defPoints += 500;
  }
  public void fieldAgainst(){
    this.atkPoints -= ((this.atkPoints >= 500)? 500 : this.atkPoints);
    this.defPoints -= ((this.defPoints >= 500)? 500 : this.defPoints);
  }

  public String toString(){
    String res = this.id + " " +
                 this.name + " " +
                 this.type + " " +
                 this.attribute + " " +
                 this.cost + " " +
                 this.atkPoints + " " +
                 this.defPoints + " " +
                 this.planet1 + " " +
                 this.planet2 + "\n";
    return res;
  }
}
