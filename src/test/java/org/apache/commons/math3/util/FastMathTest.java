
package org.apache.commons.math3.util;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.lang.reflect.Type;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;


import org.junit.Assert;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;

import org.junit.BeforeClass;
import org.junit.AfterClass;
import org.junit.Test;
import static org.junit.Assert.*;  // for assertEquals, assertTrue, etc.


import java.io.FileWriter; 
import java.io.IOException;
import java.io.File;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;


// Amani
import org.junit.BeforeClass;

import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Scanner; // Import the Scanner class to read text files
import java.util.Random;
import org.junit.FixMethodOrder;
import org.junit.runners.MethodSorters;

@FixMethodOrder(MethodSorters.NAME_ASCENDING)





public class FastMathTest {

    public static int test_count;
	private  static  FastMath model;
    public static FileWriter results_writer;
	
	
	
	private static final double MAX_ERROR_ULP = 0.51;
    private static final int NUMBER_OF_TRIALS = 1000;
    
@BeforeClass
   public static void setUp() {
	try{
		results_writer = new FileWriter("./outputTest/T0.txt");
		} catch (IOException e) {
		}
		test_count=1;
				 		


    }
	
	@AfterClass
public static void tearDown() {
    try {
        if (results_writer != null) {
            results_writer.close();
        }
    } catch (IOException e) {
        e.printStackTrace();
    }
}


  public static void printTestOutput(int line_number,  Object output){
		
		
			try {
        results_writer.write(line_number+", "+output);
		results_writer.write("\n");
		results_writer.flush();
		//System.out.println(line_number+"  "+output);

		
		} catch (IOException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
	
		
		test_count++;
	
	
	
 
	} 

  //amani 10-6
	
	
@Test
public void test01_TanhFailureCases() {
   int count = 1;
   double[] edgeCases = {
        Double.NaN, Double.POSITIVE_INFINITY, Double.NEGATIVE_INFINITY,
        Double.MAX_VALUE, -Double.MAX_VALUE, Double.MIN_VALUE, -Double.MIN_VALUE,
        1e-300, -1e-300, 20.0, -20.0, 0.0
    };

    for (double x : edgeCases) {
        try {
            double actual = FastMathAA.tanhA(x);

            // If no exception, we can optionally assert a range (or skip)
            assertTrue(actual >= -1.0 && actual <= 1.0);
  printTestOutput(test_count, actual); 
        } catch (ArithmeticException e) {
printTestOutput(test_count, Exception.class);  
        } catch (Exception e) {
            printTestOutput(test_count, Exception.class);  
        }
		
    }
}
@Test
public void test02_TanhAccuracyAA() throws Exception {
for (int test_count = 13; test_count < 133; test_count++) {
    double x = -3.0 + 6.0 * (test_count - 13) / (133.0 - 13.0); // deterministic

    try {
        double expected = Math.tanh(x);
        double actual = FastMathAA.tanhA(x);

        // Check numeric accuracy
        assertEquals("Mismatch at x=" + x, expected, actual, 1e-12);

        // Optional: print result for logging
        printTestOutput(test_count, actual);

    } catch (ArithmeticException ae) {
        // Handle known special cases (like out-of-range)
        printTestOutput(test_count, ArithmeticException.class);

    } catch (Exception e) {
        // Handle unexpected exceptions
        printTestOutput(test_count, Exception.class);
    }
}
}


	
	
	
	
	
	
	
	
}
