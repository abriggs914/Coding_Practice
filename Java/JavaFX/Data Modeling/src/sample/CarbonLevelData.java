package sample;

import javafx.scene.paint.Color;

import java.util.ArrayList;
import java.util.HashMap;

public class CarbonLevelData extends DataSet{

    CarbonLevelData() {
        super("Carbon Levels (1959 - 2017)", Color.LIGHTGOLDENRODYELLOW);
        addData();
//        this.initializeDataSet(addData());
    }

    private void addData() {
//        HashMap<String, Double> data = new HashMap<>();
        String[] colNames = {"Year", "Annual Increase", "Uncertainty"};
        this.put("1959-11-01", 0.96);    // 	0.31
        this.put("1960-11-01", 0.71);    // 	0.27
        this.put("1961-11-01", 0.78);    // 	0.27
        this.put("1962-11-01", 0.56);    // 	0.27
        this.put("1963-11-01", 0.57);    // 	0.28
        this.put("1964-11-01", 0.49);    // 	0.27
        this.put("1965-11-01", 1.1);    // 0.26
        this.put("1966-11-01", 1.1);    // 0.28
        this.put("1967-11-01", 0.61);    // 	0.34
        this.put("1968-11-01", 0.99);    // 	0.32
        this.put("1969-11-01", 1.32);    // 	0.29
        this.put("1970-11-01", 1.13);    // 	0.32
        this.put("1971-11-01", 0.73);    // 	0.3
        this.put("1972-11-01", 1.47);    // 	0.31
        this.put("1973-11-01", 1.46);    // 	0.31
        this.put("1974-11-01", 0.68);    // 	0.31
        this.put("1975-11-01", 1.23);    // 	0.27
        this.put("1976-11-01", 0.97);    // 	0.28
        this.put("1977-11-01", 1.92);    // 	0.29
        this.put("1978-11-01", 1.29);    // 	0.24
        this.put("1979-11-01", 2.14);    // 	0.26
        this.put("1980-11-01", 1.7);    // 0.11
        this.put("1981-11-01", 1.15);    // 	0.07
        this.put("1982-11-01", 0.99);    // 	0.07
        this.put("1983-11-01", 1.85);    // 	0.09
        this.put("1984-11-01", 1.24);    // 	0.12
        this.put("1985-11-01", 1.62);    // 	0.1
        this.put("1986-11-01", 1.02);    // 	0.11
        this.put("1987-11-01", 2.7);    // 0.1
        this.put("1988-11-01", 2.25);    // 	0.09
        this.put("1989-11-01", 1.38);    // 	0.11
        this.put("1990-11-01", 1.17);    // 	0.09
        this.put("1991-11-01", 0.74);    // 	0.09
        this.put("1992-11-01", 0.7);    // 0.1
        this.put("1993-11-01", 1.23);    // 	0.07
        this.put("1994-11-01", 1.68);    // 	0.11
        this.put("1995-11-01", 1.95);    // 	0.11
        this.put("1996-11-01", 1.06);    // 	0.08
        this.put("1997-11-01", 1.97);    // 	0.08
        this.put("1998-11-01", 2.82);    // 	0.11
        this.put("1999-11-01", 1.37);    // 	0.08
        this.put("2000-11-01", 1.23);    // 	0.11
        this.put("2001-11-01", 1.82);    // 	0.09
        this.put("2002-11-01", 2.36);    // 	0.07
        this.put("2003-11-01", 2.29);    // 	0.09
        this.put("2004-11-01", 1.57);    // 	0.05
        this.put("2005-11-01", 2.43);    // 	0.08
        this.put("2006-11-01", 1.75);    // 	0.06
        this.put("2007-11-01", 2.09);    // 	0.07
        this.put("2008-11-01", 1.79);    // 	0.05
        this.put("2009-11-01", 1.61);    // 	0.06
        this.put("2010-11-01", 2.43);    // 	0.07
        this.put("2011-11-01", 1.7);    //  0.08
        this.put("2012-11-01", 2.39);    // 	0.07
        this.put("2013-11-01", 2.41);    // 	0.08
        this.put("2014-11-01", 2.04);    // 	0.08
        this.put("2015-11-01", 2.94);    // 	0.07
        this.put("2016-11-01", 2.86);    // 	0.08
        this.put("2017-11-01", 2.14);    // 	0.09
//        return data;
    }
}
