
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * 
 */

public class HashandSaltPass {


    
    public static String hashPass(String pass, String salt) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] saltedPassword = (pass + salt).getBytes();
            byte[] hashedBytes = md.digest(saltedPassword);

            StringBuilder hexStr = new StringBuilder();
            for (byte b : hashedBytes) {
                hexStr.append(String.format("%02x", b));
            }

            return hexStr.toString();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace(); // Handle error appropriately
            return null;
        }
    }

    public static void main(String[] args) {
        String password = "password";
        SecureRandom random = new SecureRandom();
        byte[] salt = new byte[16];
        random.nextBytes(salt);
        
        
        String salted = Base64.getEncoder().encodeToString(salt);
        String hashedPassword = hashPass(password, salted);

        System.out.println("Password: " + password);
        System.out.println("Salt: " + salted);
        System.out.println("Hashed Pass: " + hashedPassword);
    }

    
}
