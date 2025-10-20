package org.apache.commons.math3.util;

public class FastMath {

    // Stub for exp(double x, double y, double[] hiPrec)
    public static void exp(double x, double y, double[] hiPrec) {
        double r = Math.exp(x + y);   // basic double precision
        hiPrec[0] = r; 
        hiPrec[1] = 0.0;              // no extra precision in stub
    }

    // Stub for expm1(double x, double[] hiPrec)
    public static void expm1(double x, double[] hiPrec) {
        double r = Math.expm1(x);     // basic double precision
        hiPrec[0] = r;
        hiPrec[1] = 0.0;              // no extra precision in stub
    }
}
