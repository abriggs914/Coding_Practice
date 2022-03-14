package sample;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;

public class WPWTransaction {

    private Date date;
    private HashMap<WPWEntity, Double> fromData;
    private WPWEntity toEntity;
    private double total;
    private boolean isProcessed;

    public WPWTransaction(Date dateIn, HashMap<WPWEntity, Double> fromDataIn, WPWEntity toEntityIn) {
        this.init(dateIn, fromDataIn, toEntityIn);
    }

    private void init(Date dateIn, HashMap<WPWEntity, Double> fromDataIn, WPWEntity toEntityIn) {
        this.date = dateIn;
        this.fromData = fromDataIn;
        this.toEntity = toEntityIn;
        this.total = this.calcFromTotal();
        this.isProcessed = false;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public HashMap<WPWEntity, Double> getFromData() {
        return fromData;
    }

    public void setFromData(HashMap<WPWEntity, Double> fromData) {
        this.fromData = fromData;
    }

    public WPWEntity getToEntity() {
        return toEntity;
    }

    public void setToEntity(WPWEntity toEntityIn) {
        this.toEntity = toEntityIn;
    }

    public boolean isProcessed() {
        return isProcessed;
    }

    public void setProcessed(boolean processed) {
        isProcessed = processed;
    }

    public ArrayList<WPWEntity> getEntities() {
        ArrayList<WPWEntity> entities = new ArrayList<>();
        for (WPWEntity entity : this.fromData.keySet()) {
            if (!entities.contains(entity)) {
                entities.add(entity);
            }
        }
        entities.add(toEntity);
        return entities;
    }

    public ArrayList<WPWEntity> getEntities(boolean includePot) {
        ArrayList<WPWEntity> entities = new ArrayList<>();
        for (WPWEntity entity : this.fromData.keySet()) {
            if (!entities.contains(entity)) {
                if (entity == WPWEntity.POT && !includePot) {
                    continue;
                }
                entities.add(entity);
            }
        }
        if (toEntity != WPWEntity.POT || includePot) {
            entities.add(toEntity);
        }
        return entities;
    }

    public double calcFromTotal() {
        double total = 0;
        for (WPWEntity entity : this.fromData.keySet()) {
            total += this.fromData.get(entity);
        }
        return total;
    }

    @Override
    public String toString(){
        return "<Transaction d: {" + date + "}, $ {" + total + "} from n entities: {" + fromData.size() + "} to: {" + toEntity + "}";
    }

    public static void main(String[] args) {
        // write your code here
    }
}
