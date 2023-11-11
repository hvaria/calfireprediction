import java.io.IOException;
import java.io.File;

public class myProcessBuilder {
    public static ProcessBuilder createProcessBuilder(String longitude, String latitude, String date) {
        // Command to execute with arguments
        String[] command = {"python", "entry_point.py", longitude, latitude, date};

        // Create a new process builder and set the command and arguments
        ProcessBuilder pb = new ProcessBuilder(command);

        // Set working directory if necessary
        pb.directory(new File("/path/to/working/directory"));

        return pb;
    }

    public static void main(String[] args) {
        String longitude = "-122.431297";
        String latitude = "37.773972";
        String date = "2023-04-20";

        // Create process builder
        ProcessBuilder pb = createProcessBuilder(longitude, latitude, date);

        // Start the process
        try {
            Process process = pb.start();
            // Process output, error handling, etc.
        } catch (IOException e) {
            // Handle exception
        }
    }
}
