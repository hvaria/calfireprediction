import java.sql.*;
import java.io.*;

public class SetupLoginDatabase {
    
    public static void main(String[] args) {
       dropDatabase();
    }
    
    private static String getConnectionString() {
        String currDir = System.getProperty("user.dir");
        String dbFile = currDir.concat("/src/main/webapp/WEB-INF/sqlite/login.db");
        return "jdbc:sqlite:" + dbFile;
        
    }
    
    public static void createDatabase() {
        try {
            Class.forName("org.sqlite.JDBC");
            Connection connection = DriverManager.getConnection(getConnectionString());
            Statement statement = connection.createStatement();
            statement.executeUpdate("CREATE TABLE IF NOT EXISTS login (name VARCHAR(30) PRIMARY KEY, password VARCHAR(30));");
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public static void dropDatabase() {
        try {
            Class.forName("org.sqlite.JDBC");
            Connection connection = DriverManager.getConnection(getConnectionString());
            Statement statement = connection.createStatement();
            statement.executeUpdate("DROP TABLE IF EXISTS login");
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
        
    public static void addRecord() {

    }
            
    public static void deleteRecord() {

    }
    
    public static void updateRecord() {

    }
    
    public static void getRecord() {
         
    }
}
