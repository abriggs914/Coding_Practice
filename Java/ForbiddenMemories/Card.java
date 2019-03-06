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

  public String toString(){
    String res = this.id + " " +
                 this.name + " " +
                 this.type + " " +
                 this.attribute + " " +
                 this.cost + " " +
                 this.atkPoints + " " +
                 this.defPoints + " " +
                 this.planet1 + " " +
                 this.planet2;
    return res;
  }
}
