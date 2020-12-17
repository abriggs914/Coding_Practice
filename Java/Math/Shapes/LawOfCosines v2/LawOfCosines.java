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
		
		public Triangle(String name, Side a, Side b, Side c, Angle A, Angle B, Angle C) {
			this.name = name;
			if (a != null) {
				this.setSideA(a); 
			}
			if (b != null) {
				this.setSideB(b);
			}
			if (c != null) {
				this.setSideC(c);
			}
			if (A != null) {
				this.setAngleA(A);
			}
			if (B != null) {
				this.setAngleB(B);
			}
			if (C != null) {
				this.setAngleC(C);
			}
		}
		
		// // Empty triangle
		// public Triangle(String name) {
			// this.init(name);
		// }
		
		// // SSS triangle
		// public Triangle(String name, Side a, Side b, Side c, String code) throws InvalidTriangleCreation{
			// this.init(name);
			// this.addSides(a, b, c);
		// }
		
		// // AAA triangle
		// public Triangle(String name, Angle a, Angle b, Angle c, String code) throws InvalidTriangleCreation{
			// double s = a.angle + b.angle + c.angle;
			// if (s != 180) {
				// throw new InvalidTriangleCreation(1, "Sum: " + s);
			// }
			// this.init(name);
			// this.addAngles(a, b, c);
		// }
	
		// public Triangle(String name, Angle angle, String code) throws InvalidTriangleCreation{
			// this.init(name);
			// Side a = angle.a;
			// Side b = angle.b;
			// if (a != null && b != null) {
				// this.addSides(a, b);
			// }
			// Angle a1, a2;
			// a1 = new Angle("A", 0);
			// a2 = new Angle("B", 0);
			// this.setAngleA(a1);
			// this.setAngleB(a2);
			// this.addAngles(angle);
		// }
	
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
		
		public void solveRemainingTriangle() {
			ArrayList<String> toCheck = new ArrayList<>(Arrays.asList(SIDE_A, SIDE_B, SIDE_C, ANGLE_A, ANGLE_B, ANGLE_C));
			boolean loop = true;
			boolean changed = false;
			int i = 0;
			while (loop){
				String code = toCheck.get(i);
				if (!this.attrIsKnown(code)) {
					System.out.println("code: " +  code + " is unknown");
					Side s;
					Angle a;
					double n;
					if (this.solvable_LOC(code)) {
						n = lawOfCosines(this, code);;
						System.out.println("\n\n\t\tsolvable LOC\n\tcode:" + code + ", n: " + n + "\n");
						changed = true;
						switch (i) {
							case 0	:	s = new Side("side a", n);
										this.setSideA(s);
										break;
							case 1	:	s = new Side("side b", n);
										this.setSideB(s);
										break;
							case 2	:	s = new Side("side c", n);
										this.setSideC(s);
										break;
							case 3	:	a = new Angle("angle A", n);
										this.setAngleA(a);
										break;
							case 4	:	a = new Angle("angle B", n);
										this.setAngleB(a);
										break;
							case 5	:	a = new Angle("angle C", n);
										this.setAngleC(a);
										break;
							default :	changed = false;
						}
					}
					else if (this.solvable_LOS(code)) {
						n = lawOfSines(this, code);
						System.out.println("\n\n\t\tsolvable LOS\n\tcode:" + code + ", n: " + n + "\n");
						changed = true;
						switch (i) {
							case 0	:	s = new Side("side a", n);
										this.setSideA(s);
										break;
							case 1	:	s = new Side("side b", n);
										this.setSideB(s);
										break;
							case 2	:	s = new Side("side c", n);
										this.setSideC(s);
										break;
							case 3	:	a = new Angle("angle A", n);
										this.setAngleA(a);
										break;
							case 4	:	a = new Angle("angle B", n);
										this.setAngleB(a);
										break;
							case 5	:	a = new Angle("angle C", n);
										this.setAngleC(a);
										break;
							default :	changed = false;
						}
					}
					else {
						System.out.println("code: " + code + " is not solvable using LOS or LOC");
					}
					if (this.solvable_AAA()) {
						changed = true;
						double angleA, angleB, angleC;
						angleA = ((this.attrIsKnown(ANGLE_A))? this.A.angle : 0);
						angleB = ((this.attrIsKnown(ANGLE_B))? this.B.angle : 0);
						angleC = ((this.attrIsKnown(ANGLE_C))? this.C.angle : 0);
						n = 180 - (angleA + angleB + angleC);
						System.out.println("\n\n\t\tsolvable AAA\n\tcode:" + code + ", n: " + n + "\n");
						if (!this.attrIsKnown(ANGLE_A)) {
							a = new Angle("angle A", n);
							this.setAngleA(a);
						}
						else if (!this.attrIsKnown(ANGLE_B)) {
							a = new Angle("angle B", n);
							this.setAngleB(a);
						}
						else if (!this.attrIsKnown(ANGLE_C)) {
							a = new Angle("angle C", n);
							this.setAngleC(a);
						}
					}
				}
				else {
					System.out.println("code: " + code + " is KNOWN");
				}
				
				i += 1;
				if (!changed && i == toCheck.size()){
					break;
				}
				i %= toCheck.size();
				if (changed && i == 0){
					changed = false;
				}
				// System.out.println("j: " + Integer.toString(j) + " c: " + Integer.toString(c));
			}
		}
		
		// Logically check if the current state of this Triangle object can be solved for the given code.
		public boolean solvable_LOC(String code) {
			boolean dims = true;//(this.sides.size() + this.angles.size()) >= 3;
			boolean init = this.attrIsKnown(code);
			// System.out.println(this.toString());
			if (code.equals(SIDE_A)) {
				init |= this.b != null && this.c != null && this.A != null;
			}
			else if (code.equals(SIDE_B)) {
				init |= this.a != null && this.c != null && this.B != null;
			}
			else if (code.equals(SIDE_C)) {
				init |= this.a != null && this.b != null && this.C != null;
			}
			else if (code.equals(ANGLE_A) || code.equals(ANGLE_B) || code.equals(ANGLE_C)) {
				init |= this.a != null && this.b != null && this.c != null;
			}
			else {
				System.out.println("INVALID code");
			}
			return init;
		}
		
		public boolean solvable_LOS(String code) {
			boolean init = this.attrIsKnown(code);
			boolean pair = this.attrIsKnown(SIDE_A, ANGLE_A);// && (!code.equals(SIDE_A) && !code.equals(ANGLE_A));
			pair |= this.attrIsKnown(SIDE_B, ANGLE_B);// && (!code.equals(SIDE_B) && !code.equals(ANGLE_B));
			pair |= this.attrIsKnown(SIDE_C, ANGLE_C);// && (!code.equals(SIDE_C) && !code.equals(ANGLE_C));
			// Side pairS;
			// Angle pairA;
			// if (t.attrIsKnown(SIDE_A, ANGLE_A)) {
				// pairS = t.a;
				// pairA = t.A;
			// }
			// else if (t.attrIsKnown(SIDE_B, ANGLE_B)) {
				// pairS = t.b;
				// pairA = t.B;
			// }
			// else if (t.attrIsKnown(SIDE_C, ANGLE_C)) {
				// pairS = t.c;
				// pairA = t.C;
			// }
			// System.out.println("pair: " + pair);
			if (code.equals(SIDE_A)) {
				init |= pair && this.attrIsKnown(ANGLE_A);
			}
			else if (code.equals(SIDE_B)) {
				init |= pair && this.attrIsKnown(ANGLE_B);
			}
			else if (code.equals(SIDE_C)) {
				init |= pair && this.attrIsKnown(ANGLE_C);
			}
			else if (code.equals(ANGLE_A)) {
				init |= pair && this.attrIsKnown(SIDE_A);
			}
			else if (code.equals(ANGLE_B)) {
				init |= pair && this.attrIsKnown(SIDE_B);
			}
			else if (code.equals(ANGLE_C)) {
				init |= pair && this.attrIsKnown(SIDE_C);
			}
			else {
				System.out.println("INVALID code");
			}
			return init;
		}
		
		public boolean solvable_AAA() {
			int c = 0;
			c += ((this.attrIsKnown(ANGLE_A))? 1 : 0);
			c += ((this.attrIsKnown(ANGLE_B))? 1 : 0);
			c += ((this.attrIsKnown(ANGLE_C))? 1 : 0);
			return c > 1;
		}
		
		public boolean attrIsKnown(String... codes) {
			boolean known = ((codes.length > 0)? true : false);
			for (int i = 0; i < codes.length; i++) {
				String code = codes[i];
				if (code.equals(SIDE_A)) {
					known &= this.a != null;
				}
				else if (code.equals(SIDE_B)) {
					known &= this.b != null;
				}
				else if (code.equals(SIDE_C)) {
					known &= this.c != null;
				}
				else if (code.equals(ANGLE_A)) {
					known &= this.A != null;
				}
				else if (code.equals(ANGLE_B)) {
					known &= this.B != null;
				}
				else if (code.equals(ANGLE_C)) {
					known &= this.C != null;
				}
				// else {
					// return false;
				// }
				// if (!known) {
					// return false;
				// }
			}
			return known;
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
			//return "\n" + this.name + "\nsides: " + this.sides + "\nAngles: " + this.angles;
			String res = "\n" + this.name;
			res += "\na: " + ((this.a == null)? "null" : this.a);
			res += "\nb: " + ((this.b == null)? "null" : this.b);
			res += "\nc: " + ((this.c == null)? "null" : this.c);
			res += "\nA: " + ((this.A == null)? "null" : this.A);
			res += "\nB: " + ((this.B == null)? "null" : this.B);
			res += "\nC: " + ((this.C == null)? "null" : this.C);
			return res;
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
		if (!t.attrIsKnown(code)) {
			if (t.solvable_LOC(code)) {
				a = ((t.attrIsKnown(SIDE_A))? t.a.length : 0);
				b = ((t.attrIsKnown(SIDE_B))? t.b.length : 0);
				c = ((t.attrIsKnown(SIDE_C))? t.c.length : 0);
				A = ((t.attrIsKnown(ANGLE_A))? t.A.angle : 0);
				B = ((t.attrIsKnown(ANGLE_B))? t.B.angle : 0);
				C = ((t.attrIsKnown(ANGLE_C))? t.C.angle : 0);
				if (code.equals(SIDE_A)){
					//System.out.println("b^2: " + Math.pow(b, 2) + "\nc^2: " + Math.pow(c, 2) + "\n2*b*c: " + (2 * b * c) + "\ncos(A): " + Math.cos(A) + "\nMath.toDegrees(Math.cos(A)): " + Math.toDegrees(Math.cos(A)) + "\nRES_1: " + Math.sqrt(Math.pow(b, 2) + Math.pow(c, 2) - (2 * b * c * Math.toDegrees(Math.cos(A)))) + "\nRES_2: " + Math.sqrt(Math.pow(b, 2) + Math.pow(c, 2) - (2 * b * c * (Math.cos(A)))));
					res = Math.sqrt(Math.pow(b, 2) + Math.pow(c, 2) - (2 * b * c * (Math.cos(A))));
					// res = Math.sqrt(b*b + c*c - (2 * b * c * Math.cos(A)));
					
				}
				else if (code.equals(SIDE_B)) {
					res = Math.sqrt(Math.pow(a, 2) + Math.pow(c, 2) - (2 * a * c * (Math.cos(B))));
					// if (t.b != null) {
						// res = t.b.length;
					// }
				}
				else if (code.equals(SIDE_C)) {
					res = Math.sqrt(Math.pow(a, 2) + Math.pow(b, 2) - (2 * a * b * (Math.cos(C))));
					// if (t.c != null) {
						// // res = t.c.length;
					// }
				}
				else if (code.equals (ANGLE_A)) {
					res = Math.toDegrees(Math.acos((Math.pow(a, 2) - (Math.pow(b, 2) + Math.pow(c, 2))) / (-2 * b * c)));
					// res = (Math.acos((Math.pow(a, 2) - (Math.pow(b, 2) + Math.pow(c, 2))) / (-2 * b * c)));
					// if (t.A != null) {
						// res = t.A.angle;
					// }
				}
				else if (code.equals(ANGLE_B)) {
					res = Math.toDegrees(Math.acos((Math.pow(b, 2) - (Math.pow(a, 2) + Math.pow(c, 2))) / (-2 * a * c)));
					// res = (Math.acos((Math.pow(b, 2) - (Math.pow(a, 2) + Math.pow(c, 2))) / (-2 * a * c)));
					// if (t.B != null) {
						// res = t.B.angle;
					// }
				}
				else if (code.equals(ANGLE_C)) {
					res = Math.toDegrees(Math.acos((Math.pow(c, 2) - (Math.pow(a, 2) + Math.pow(b, 2))) / (-2 * a * b)));
					// res = (Math.acos((Math.pow(c, 2) - (Math.pow(a, 2) + Math.pow(b, 2))) / (-2 * a * b)));
					// if (t.C != null) {
						// res = t.C.angle;/
					// }
				}
				else {
					System.out.println("INVALID code");
				}
			}
			else {
				System.out.println("UNSOLVABLE");
			}
		}
		else {
			if (code.equals(SIDE_A)) {
				res = t.a.length;
			}
			else if (code.equals(SIDE_B)) {
				res = t.b.length;
			}
			else if (code.equals(SIDE_C)) {
				res = t.c.length;
			}
			else if (code.equals(ANGLE_A)) {
				res = t.A.angle;
			}
			else if (code.equals(ANGLE_B)) {
				res = t.B.angle;
			}
			else if (code.equals(ANGLE_C)) {
				res = t.C.angle;
			}
		}
		return res;
	}
	
	public static double lawOfSines(Triangle t, String code) {
		// t3 doesnt solve correctly
		double a, b, c, A, B, C;
		double res = 0;
		if (!t.attrIsKnown(code)) {
			if (t.solvable_LOS(code)) {
				a = ((t.attrIsKnown(SIDE_A))? t.a.length : 0);
				b = ((t.attrIsKnown(SIDE_B))? t.b.length : 0);
				c = ((t.attrIsKnown(SIDE_C))? t.c.length : 0);
				A = ((t.attrIsKnown(ANGLE_A))? t.A.angle : 0);
				B = ((t.attrIsKnown(ANGLE_B))? t.B.angle : 0);
				C = ((t.attrIsKnown(ANGLE_C))? t.C.angle : 0);
				Side pairS;
				Angle pairA;
				if (t.attrIsKnown(SIDE_A, ANGLE_A)) {
					pairS = t.a;
					pairA = t.A;
				}
				else if (t.attrIsKnown(SIDE_B, ANGLE_B)) {
					pairS = t.b;
					pairA = t.B;
				}
				else if (t.attrIsKnown(SIDE_C, ANGLE_C)) {
					pairS = t.c;
					pairA = t.C;
				}
				else {
					System.out.println("\n\tQUITTING EARLY\n");
				System.out.println("\t\t\ta: " + a + "\n\t\t\tb: " + b + "\n\t\t\tc: " + c + "\n\t\t\tA: " + A + "\n\t\t\tB: " + B + "\n\t\t\tC: " + C);
				// System.out.println("\tpairS: " + pairS + "\n\tpairA: " + pairA + "\n\tcode: " + code + "\n\tres: " + res);
				
					return res;
				}
				if (code.equals(SIDE_A)) {
					res = Math.sin(A) * (pairS.length / Math.sin(pairA.angle));
				}
				else if (code.equals(SIDE_B)) {
					res = Math.sin(B) * (pairS.length / Math.sin(pairA.angle));
				}
				else if (code.equals(SIDE_C)) {
					res = Math.sin(C) * (pairS.length / Math.sin(pairA.angle));
				}
				else if (code.equals(ANGLE_A)) {
					// res = Math.toDegrees(Math.asin(a * (Math.sin(pairA.angle) / pairS.length)));
					res = Math.toDegrees(Math.asin(a * (Math.sin(Math.toRadians(pairA.angle)) / pairS.length)));
					// System.out.println("pairA.angle: " + pairA.angle + "\nMath.sin(pairA): " + Math.sin(pairA.angle) + "\nMath.toDegrees(Math.sin(pairA)): " + Math.toDegrees(Math.sin(pairA.angle)) + "\nMath.toDegrees(Math.sin(Math.toRadians(pairA))): " + Math.toDegrees(Math.sin(Math.toRadians(pairA.angle))) + "\nMath.sin(Math.toRadians(pairA))): " + Math.sin(Math.toRadians(pairA.angle)));
					// System.out.println("¨Math.asin((Math.sin(Math.toRadians(pairA))) / 60) * 48): " + Math.asin((48 * (Math.sin(Math.toRadians(pairA.angle)) / 60))));
					// System.out.println("¨Math.toDegrees(Math.asin((Math.sin(Math.toRadians(pairA))) / 60) * 48)): " + Math.toDegrees(Math.asin((48 * (Math.sin(Math.toRadians(pairA.angle)) / 60)))));
					// System.out.println("¨Math.toDegrees(Math.asin(Math.toRadians(Math.sin(Math.toRadians(pairA))) / 60) * 48))): " + Math.toDegrees(Math.toRadians(Math.asin((48 * (Math.sin(Math.toRadians(pairA.angle)) / 60))))));
				}
				else if (code.equals(ANGLE_B)) {
					// res = Math.toDegrees(Math.asin(b * (Math.sin(pairA.angle) / pairS.length)));
					res = Math.toDegrees(Math.asin(b * (Math.sin(Math.toRadians(pairA.angle)) / pairS.length)));
				}
				else if (code.equals(ANGLE_C)) {
					// res = Math.toDegrees(Math.asin(c * (Math.sin(pairA.angle) / pairS.length)));
					res = Math.toDegrees(Math.asin(c * (Math.sin(Math.toRadians(pairA.angle)) / pairS.length)));
				}
				System.out.println("\t\t\ta: " + a + "\n\t\t\tb: " + b + "\n\t\t\tc: " + c + "\n\t\t\tA: " + A + "\n\t\t\tB: " + B + "\n\t\t\tC: " + C);
				System.out.println("\tpairS: " + pairS + "\n\tpairA: " + pairA + "\n\tcode: " + code + "\n\tres: " + res);
				
			}
		}
		else {
			if (code.equals(SIDE_A)) {
				res = t.a.length;
			}
			else if (code.equals(SIDE_B)) {
				res = t.b.length;
			}
			else if (code.equals(SIDE_C)) {
				res = t.c.length;
			}
			else if (code.equals(ANGLE_A)) {
				res = t.A.angle;
			}
			else if (code.equals(ANGLE_B)) {
				res = t.B.angle;
			}
			else if (code.equals(ANGLE_C)) {
				res = t.C.angle;
			}
		}
		return res;
	}
	
	public static final String SIDE_A = "a";
	public static final String SIDE_B = "b";
	public static final String SIDE_C = "c";
	public static final String ANGLE_A = "A";
	public static final String ANGLE_B = "B";
	public static final String ANGLE_C = "C";
	
	public static void main(String[] args) {
		
		try {
			
			Side side1 = new Side("a", 48);
			Side side2 = new Side("b", 36);
			Side side3 = new Side("c", 60);
			
			Angle angle1 = new Angle("A", side1, side2, 36);
			Angle angle2 = new Angle("B", side2, side3, 34);
			Angle angle3 = new Angle("C", side1, side3, 110);
			
			Triangle t1 = new Triangle("t1", side1, side2, side3, null, null, null);
			Triangle t2 = new Triangle("t2", side1, side2, null, angle1, null, null);
			Triangle t3 = new Triangle("t3", null, side2, side3, null, angle2, null);
			Triangle t4 = new Triangle("t4", side1, null, side3, null, null, angle3);
			Triangle t5 = new Triangle("t5", side1, side2, null, null, null, angle3);
			
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
				t.solveRemainingTriangle();
				System.out.println("\n" + t);
				// System.out.println("a: " + lawOfCosines(t, SIDE_A));
				// System.out.println("b: " + lawOfCosines(t, SIDE_B));
				// System.out.println("c: " + lawOfCosines(t, SIDE_C));
				// System.out.println("A: " + lawOfCosines(t, ANGLE_A));
				// System.out.println("B: " + lawOfCosines(t, ANGLE_B));
				// System.out.println("C: " + lawOfCosines(t, ANGLE_C));
			}
			System.out.println();
			System.out.println();
			throw new InvalidTriangleCreation(1, "THIS IS JUST A TEST\n\"a\".equals(\"a\"): " + ("a".equals("a")) + "\n\"a\".equals(\"A\"): " + ("a".equals("A")) + "\n\"A\".equals(\"A\"): " + ("A".equals("A")) + "\n\"A\".equals(\"a\"): " + ("A".equals("a")));
		}
		catch(InvalidTriangleCreation e) {
		}
	}
}

// Triangles can be made using:
//-	3 varibles (SSA, AAA, SSS, SAA)
//-	3 points (cartesian plotting points)