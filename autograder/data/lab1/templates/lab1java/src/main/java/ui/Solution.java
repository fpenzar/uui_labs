package ui;

public class Solution {

	public static void main(String ... args) {
		System.out.println("Ovime kreće Vaš program.");
		System.out.println("ovo je dodano");
		for(String arg : args) {
			System.out.printf("Predan argument %s%n", arg);
		}
	}

}
