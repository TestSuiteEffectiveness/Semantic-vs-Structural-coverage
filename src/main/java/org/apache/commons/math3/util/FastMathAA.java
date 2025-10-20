/* LittleDarwin generated order-1 mutant
mutant type: AssignmentOperatorReplacementShortcut
----> before:           nb += -(temp - na - yb);
----> after:           nb -= -(temp - na - yb);
----> line number in original file: 68
----> mutated node: 563

*/


package org.apache.commons.math3.util;

public class FastMathAA {
	    private static final long HEX_40000000 = 0x40000000L; // 1073741824L

	public static double tanhA(double x) throws Exception {
      boolean negate = false;

     if (Double.isNaN(x)) {
        throw new IllegalArgumentException("Input cannot be NaN");
    }

    // Check for Infinity or special edge values
    if (Double.isInfinite(x)
        || x == Double.MAX_VALUE
        || x == -Double.MAX_VALUE
        || x == Double.MIN_VALUE
        || x == -Double.MIN_VALUE
        || x == 1e-300
        || x == -1e-300
        || x == 20.0
        || x == -20.0
        || x == 0.0) {
        throw new ArithmeticException("Input value is outside valid range for tanh()");
    }

	if (x != x) {
          return x;
      }

      // tanh[z] = sinh[z] / cosh[z]
      // = (exp(z) - exp(-z)) / (exp(z) + exp(-z))
      // = (exp(2x) - 1) / (exp(2x) + 1)

      // for magnitude > 20, sinh[z] == cosh[z] in double precision

      if (x > 20.0) {
          return 1.0;
      }

      if (x < -20) {
          return -1.0;
      }

      if (x == 0) {
          return x;
      }

      if (x < 0.0) {
          x = -x;
          negate = true;
      }

      double result;
      if (x >= 0.5) {
          double hiPrec[] = new double[2];
          // tanh(x) = (exp(2x) - 1) / (exp(2x) + 1)
          FastMath.exp(x*2.0, 0.0, hiPrec);

          double ya = hiPrec[0] + hiPrec[1];
          double yb = -(ya - hiPrec[0] - hiPrec[1]);

          /* Numerator */
          double na = -1.0 + ya;
          double nb = -(na + 1.0 - ya);
          double temp = na + yb;
          nb -= -(temp - na - yb);
          na = temp;

          /* Denominator */
          double da = 1.0 + ya;
          double db = -(da - 1.0 - ya);
          temp = da + yb;
          db += -(temp - da - yb);
          da = temp;

          temp = da * HEX_40000000;
          double daa = da + temp - temp;
          double dab = da - daa;

          // ratio = na/da
          double ratio = na/da;
          temp = ratio * HEX_40000000;
          double ratioa = ratio + temp - temp;
          double ratiob = ratio - ratioa;

          // Correct for rounding in division
          ratiob += (na - daa*ratioa - daa*ratiob - dab*ratioa - dab*ratiob) / da;

          // Account for nb
          ratiob += nb / da;
          // Account for db
          ratiob += -db * na / da / da;

          result = ratioa + ratiob;
      }
      else {
          double hiPrec[] = new double[2];
		   FastMath.expm1(x*2.0, hiPrec); 
          // tanh(x) = expm1(2x) / (expm1(2x) + 2)
         // expm1(x*2.0, hiPrec);

          double ya = hiPrec[0] + hiPrec[1];
          double yb = -(ya - hiPrec[0] - hiPrec[1]);

          /* Numerator */
          double na = ya;
          double nb = yb;

          /* Denominator */
          double da = 2.0 + ya;
          double db = -(da - 2.0 - ya);
          double temp = da + yb;
          db += -(temp - da - yb);
          da = temp;

          temp = da * HEX_40000000;
          double daa = da + temp - temp;
          double dab = da - daa;

          // ratio = na/da
          double ratio = na/da;
          temp = ratio * HEX_40000000;
          double ratioa = ratio + temp - temp;
          double ratiob = ratio - ratioa;

          // Correct for rounding in division
          ratiob += (na - daa*ratioa - daa*ratiob - dab*ratioa - dab*ratiob) / da;

          // Account for nb
          ratiob += nb / da;
          // Account for db
          ratiob += -db * na / da / da;

          result = ratioa + ratiob;
      }

      if (negate) {
          result = -result;
      }

      return result;
    }

   
    }

