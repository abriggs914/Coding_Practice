import java.util.ArrayList;
import java.util.Arrays;

public class LawOfCosines {
	
	public static class InvalidTriangleCreation extends Throwable {
		public InvalidTriangleCreation(int code, String message) {
			System.out.println("\nInvalid Triangle creation");
			switch (code) {
				case 1	:	System.out.println("Angles do not sum to 180."); break;
				case 2	:	System.out.println("Side length cannot be equal to 0."); break;
				case 3	:	System.out.println("Triangles cannot have more than 3 sides."); break;
				case 4	:	System.out.println("Internal angle cannot be <= 0."); break;
				case 5	:	System.out.println("Triangles cannot have more than 3 internal angles."); break;
				case 6	:	System.out.println("Given angles have more than 3 distinct joining sides."); break;
				default	:	System.out.println("Invalid Triangle creation.");
			}
			System.out.println(message + "\n");
			this.printStackTrace();
			System.out.println("\n");
		}
	}
	
	public static class Triangle {
		private String name;
		private ArrayList<Side> sides;
		private ArrayList<Angle> angles;
		private boolean onOrigin;
		private boolean placed;
		
		public Side a, b, c;
		public Angle A, B, C;
		public double ax, ay, bx, by, cx, cy;
		
		// Empty triangle
		public Triangle(String name) {
			this.init(name);
		}
		
		// SSS triangle
		public Triangle(String name, Side a, Side b, Side c, String code) throws InvalidTriangleCreation{
			this.init(name);
			this.addSides(a, b, c);
		}
		
		// AAA triangle
		public Triangle(String name, Angle a, Angle b, Angle c, String code) throws InvalidTriangleCreation{
			double s = a.angle + b.angle + c.angle;
			if (s != 180) {
				throw new InvalidTriangleCreation(1, "Sum: " + s);
			}
			this.init(name);
			this.addAngles(a, b, c);
		}
	
		public Triangle(String name, Angle angle, String code) throws InvalidTriangleCreation{
			this.init(name);
			Side a = angle.a;
			Side b = angle.b;
			if (a != null && b != null) {
				this.addSides(a, b);
			}
			Angle a1, a2;
			a1 = new Angle("A", 0);
			a2 = new Angle("B", 0);
			this.setAngleA(a1);
			this.setAngleB(a2);
			this.addAngles(angle);
		}
	
	/*	
		// SAS triangle
		public Triangle(String name, Side a, Angle b, Side c) throws InvalidTriangleCreation{
			this.init(name);
			this.addSides(a, c);
			this.addAngles(b);
		}
		
		// ASS triangle
		public Triangle(String name, Angle a, Side b, Side c) throws InvalidTriangleCreation{
			this.init(name);
			this.addSides(b, c);
			this.addAngles(a);
		}
		
		// SSA triangle
		public Triangle(String name, Side a, Side b, Angle c) throws InvalidTriangleCreation{
			this.init(name);
			this.addSides(a, b);
			this.addAngles(c);
		}
		
		// ASA triangle
		public Triangle(String name, Angle a, Side b, Angle c) throws InvalidTriangleCreation{
			this.init(name);
			this.addSides(b);
			this.addAngles(a, c);
		}
		
		// AAS triangle
		public Triangle(String name, Angle a, Angle b, Side c) throws InvalidTriangleCreation{
			this.init(name);
			this.addSides(c);
			this.addAngles(a, b);
		}
		
		// SAA triangle
		public Triangle(String name, Side a, Angle b, Angle c) throws InvalidTriangleCreation{
			this.init(name);
			this.addSides(a);
			this.addAngles(b, c);
		}
		*/
		private void init(String name) {
			this.name = name;
			this.placed = false;
			this.sides = new ArrayList<>();
			this.angles = new ArrayList<>();
		}
		
		// Logically check if the current state of this Triangle object can be completely solved.
		public boolean solvable(String code) {
			boolean dims = (this.sides.size() + this.angles.size()) >= 3;
			boolean init = false;
			if (code.equals(SIDE_A)) {
				init = this.b != null && this.c != null && this.A != null;
				init |= this.a != null;
			}
			else if (code.equals(SIDE_B)) {
				init = this.a != null && this.c != null && this.B != null;
				init |= this.b != null;
			}
			else if (code.equals(SIDE_C)) {
				init = this.a != null && this.b != null && this.C != null;
				init |= this.c != null;
			}
			else if (code.equals(ANGLE_A) || code.equals(ANGLE_B) || code.equals(ANGLE_C)) {
				init = this.a != null && this.b != null && this.c != null;
				init |= ((code.equals(ANGLE_A) && this.A != null) || (code.equals(ANGLE_B) && this.B != null) || (code.equals(ANGLE_C) && this.C != null));
			}
			else {
				System.out.println("INVALID code");
			}
			return dims && init;
		}
		
		public boolean isPlaced() {
			return this.placed;
		}
		
		public void addSides(Side... sides) throws InvalidTriangleCreation{
			for (int i = 0; i < sides.length; i++) {
				if (sides[i].length <= 0) {
					throw new InvalidTriangleCreation(2, "Side: <" + sides[i].length + "> is invalid");
				}
				this.sides.add(sides[i]);
				if (this.sides.size() > 3) {
					throw new InvalidTriangleCreation(3, "");
				}
				//int j = i % 3;
			}
			for (int i = 0; i < this.sides.size(); i++) {
				System.out.println("j: " + i);
				switch (i) {
					case 0	:	this.a = this.sides.get(i); break;
					case 1	:	this.b = this.sides.get(i); break;
					case 2	:	this.c = this.sides.get(i); break;
					default :	System.out.println("INDEX OUT OF BOUNDS");
				}
			}
			// if (this.sides.size() == 3) {
				// this.a = this.sides.get(0);
				// this.b = this.sides.get(1);
				// this.c = this.sides.get(2);
			// }
		}
				
		public void addAngles(Angle... angles) throws InvalidTriangleCreation{
			double sum = 0;
			ArrayList<Side> sides = new ArrayList<>();
			for (int i = 0; i < this.angles.size(); i++) {
				Angle angle = this.angles.get(i);
				sum += angle.angle;
				Side a = angle.a;
				Side b = angle.b;
				if (!sides.contains(a)) {
					sides.add(a);
				}
				if (!sides.contains(b)) {
					sides.add(b);
				}
			}
			for (int i = 0; i < angles.length; i++) {
				Angle angle = angles[i];
				Side a = angle.a;
				Side b = angle.b;
				if (!sides.contains(a)) {
					sides.add(a);
				}
				if (!sides.contains(b)) {
					sides.add(b);
				}
				if (sides.size() > 3) {
					throw new InvalidTriangleCreation(6, "");
				}
				if (angle.angle <= 0) {
					throw new InvalidTriangleCreation(4, "Angle: <" + angle.angle + "> is invalid");
				}
				sum += angle.angle;
				this.angles.add(angle);
				if (this.angles.size() > 3) {
					throw new InvalidTriangleCreation(5, "");
				}
			}
			if (this.angles.size() == 3) {
				if (sum != 180) {
					throw new InvalidTriangleCreation(1, "Angle sum: " + sum + ", is too large");
				}
				// this.A = this.angles.get(0);
				// this.B = this.angles.get(1);
				// this.C = this.angles.get(2);
			}
			for (int i = 0; i < this.angles.size(); i++) {
				System.out.println("j: " + i);
				switch (i) {
					case 0	:	this.A = this.angles.get(i); break;
					case 1	:	this.B = this.angles.get(i); break;
					case 2	:	this.C = this.angles.get(i); break;
					default :	System.out.println("INDEX OUT OF BOUNDS");
				}
			}
		}
		
		public void setSideA(Side a) {this.a = a;}
		public void setSideB(Side b) {this.b = b;}
		public void setSideC(Side c) {this.c = c;}
		public void setAngleA(Angle A) {this.A = A;}
		public void setAngleB(Angle B) {this.B = B;}
		public void setAngleC(Angle C) {this.C = C;}
		
		public String toString() {
			return "\n" + this.name + "\nsides: " + this.sides + "\nAngles: " + this.angles;
		}
	}

	public static class Side {
	
		private String name;
		private double length;

		public Side(String name, double num) {
			this.name = name;
			this.length = num;
		}
		
		public boolean known() {
			return this.length != 0;
		}
		
		public String toString() {
			return "<Side " + this.name + ", l: " + this.length + ">";
		}
	}

	public static class Angle {
	
		private String name;
		private double angle;
		private Side a;
		private Side b;		

		public Angle(String name, double num) {
			this.name = name;
			this.angle = num;
		}

		public Angle(String name, Side a, Side b, double num) {
			this.name = name;
			this.a = a;
			this.b = b;
			this.angle = num;
		}
		
		public boolean known() {
			return this.angle != 0;
		}
		
		public String toString() {
			return "<Angle " + this.name + ", a: " + this.a + ", b: " + this.b + ", d: " + this.angle + ">";
		}
	}
	
	public static double lawOfCosines(Triangle t, String code) {
		double a, b, c, A, B, C, x;
		double res = 0;
		if (t.solvable(code)) {
			a = ((t.a == null)? 0 : t.a.length);
			b = ((t.b == null)? 0 : t.b.length);
			c = ((t.c == null)? 0 : t.c.length);
			A = ((t.A == null)? 0 : t.A.angle);
			B = ((t.B == null)? 0 : t.B.angle);
			C = ((t.C == null)? 0 : t.C.angle);
			if (code.equals(SIDE_A)){
				res = Math.sqrt(Math.pow(b, 2) + Math.pow(c, 2) - (2 * b * c * (Math.cos(A))));
				if (t.a != null) {
					res = t.a.length;
				}
			}
			else if (code.equals(SIDE_B)) {
				res = Math.sqrt(Math.pow(a, 2) + Math.pow(c, 2) - (2 * a * c * (Math.cos(B))));
				if (t.b != null) {
					res = t.b.length;
				}
			}
			else if (code.equals(SIDE_C)) {
				res = Math.sqrt(Math.pow(a, 2) + Math.pow(b, 2) - (2 * a * b * (Math.cos(C))));
				if (t.c != null) {
					res = t.c.length;
				}
			}
			else if (code.equals (ANGLE_A)) {
				res = Math.toDegrees(Math.acos((Math.pow(a, 2) - (Math.pow(b, 2) + Math.pow(c, 2))) / (-2 * b * c)));
				if (t.A != null) {
					res = t.A.angle;
				}
			}
			else if (code.equals(ANGLE_B)) {
				res = Math.toDegrees(Math.acos((Math.pow(b, 2) - (Math.pow(a, 2) + Math.pow(c, 2))) / (-2 * a * c)));
				if (t.B != null) {
					res = t.B.angle;
				}
			}
			else if (code.equals(ANGLE_C)) {
				res = Math.toDegrees(Math.acos((Math.pow(c, 2) - (Math.pow(a, 2) + Math.pow(b, 2))) / (-2 * a * b)));
				if (t.C != null) {
					res = t.C.angle;
				}
			}
			else {
				System.out.println("INVALID code");
			}
		}
		else {
			System.out.println("UNSOLVABLE");
		}
		return res;
	}
	
	public static final String SIDE_A = "a";
	public static final String SIDE_B = "b";
	public static final String SIDE_C = "c";
	public static final String ANGLE_A = "A";
	public static final String ANGLE_B = "B";
	public static final String ANGLE_C = "C";
	
	public static String codify(String a, String b, String c) {
		return a + b + c;
	}
	
	public static void main(String[] args) {
		
		try {
			
			Side side1 = new Side("a", 48);
			Side side2 = new Side("b", 36);
			Side side3 = new Side("c", 60);
			
			Angle angle1 = new Angle("A", side1, side2, 36);
			Angle angle2 = new Angle("B", side2, side3, 34);
			Angle angle3 = new Angle("C", side1, side3, 110);
			
			Triangle t1 = new Triangle("t1", side1, side2, side3, codify(SIDE_A, SIDE_B, SIDE_C));
			Triangle t2 = new Triangle("t2", angle1, codify(SIDE_A, SIDE_B, ANGLE_C));
			Triangle t3 = new Triangle("t3", angle2, codify(SIDE_B, SIDE_C, ANGLE_A));
			Triangle t4 = new Triangle("t4", angle3, codify(SIDE_A, SIDE_C, ANGLE_B));
			Triangle t5 = new Triangle("t5", angle1, codify(SIDE_A, SIDE_B, ANGLE_C));
			
			System.out.println("\nt1: " + t1);
			System.out.println("\nt2: " + t2);
			System.out.println("\nt3: " + t3);
			System.out.println("\nt4: " + t4);
			System.out.println("\nt5: " + t5);
			
			ArrayList<Triangle> triangles = new ArrayList<>(Arrays.asList(
				t1, t2, t3, t4, t5
			));
			System.out.println("Finding sides and angles:");
			for (int i = 0; i < triangles.size(); i++) {
				Triangle t = triangles.get(i);
				System.out.println("\n" + t);
				System.out.println("a: " + lawOfCosines(t, SIDE_A));
				System.out.println("b: " + lawOfCosines(t, SIDE_B));
				System.out.println("c: " + lawOfCosines(t, SIDE_C));
				System.out.println("A: " + lawOfCosines(t, ANGLE_A));
				System.out.println("B: " + lawOfCosines(t, ANGLE_B));
				System.out.println("C: " + lawOfCosines(t, ANGLE_C));
			}
			System.out.println();
			System.out.println();
		}
		catch(InvalidTriangleCreation e) {
		}
	}
}

// Triangles can be made using:
//-	3 varibles (SSA, AAA, SSS, SAA)
//-	3 points (cartesian plotting points)