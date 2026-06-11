import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class EqualizerServer extends Application {

    // =========================
    // SETTINGS
    // =========================
    private static final int BARS = 20;

    // =========================
    // DATA (STEREO)
    // =========================
    private final Object lock = new Object();

    private final double[] latestLeft = new double[BARS];
    private final double[] latestRight = new double[BARS];

    private final double[] currentLeft = new double[BARS];
    private final double[] currentRight = new double[BARS];

    private volatile double flash = 0.0;

    // =========================
    // NETWORK
    // =========================
    private ServerSocket serverSocket;
    private Socket clientSocket;
    private volatile boolean running = true;

    // =========================
    // UI
    // =========================
    private Canvas canvas;
    private GraphicsContext gc;

    // =========================
    // MODE
    // =========================
    private enum Mode { STEREO }
    private Mode mode = Mode.STEREO;

    // =========================
    // START
    // =========================
    @Override
    public void start(Stage stage) {

        StackPane root = new StackPane();
        root.setStyle("-fx-background-color: black;");

        canvas = new Canvas(1000, 600);
        gc = canvas.getGraphicsContext2D();

        root.getChildren().add(canvas);

        Scene scene = new Scene(root);

        scene.setOnKeyPressed(e -> {
            if (e.getCode() == KeyCode.ESCAPE) {
                stopApp();
            }
        });

        stage.setTitle("Stereo Audio Visualizer");
        stage.setScene(scene);
        stage.show();

        startSocket();
        startRender();
    }

    // =========================
    // SOCKET
    // =========================
    private void startSocket() {

        Thread t = new Thread(() -> {

            try {
                serverSocket = new ServerSocket(6000);
                System.out.println("Listening on 6000");
				System.out.println("VISUALIZER VERSION 2");
                while (running) {

                    try {
                        clientSocket = serverSocket.accept();
                        System.out.println("Client connected");

                        BufferedReader reader = new BufferedReader(
                                new InputStreamReader(clientSocket.getInputStream())
                        );

                        String line;

                        while (running && (line = reader.readLine()) != null) {

                            String[] parts = line.split("\\|");

                            synchronized (lock) {

                                // LEFT
                                if (parts.length > 0 && parts[0].startsWith("L:")) {
                                    String[] vals = parts[0].substring(2).split(",");
                                    for (int i = 0; i < BARS && i < vals.length; i++) {
                                        latestLeft[i] = parse(vals[i]);
                                    }
                                }

                                // RIGHT
                                if (parts.length > 1 && parts[1].startsWith("R:")) {
                                    String[] vals = parts[1].substring(2).split(",");
                                    for (int i = 0; i < BARS && i < vals.length; i++) {
                                        latestRight[i] = parse(vals[i]);
                                    }
                                }

                                // FLASH
                                if (parts.length > 2 && parts[2].startsWith("F:")) {
                                    flash = Math.max(
                                            flash,
                                            parse(parts[2].substring(2))
                                    );
                                }
                            }
                        }

                        System.out.println("Client disconnected");

                    } catch (Exception e) {
                        if (running) {
                            System.out.println("Socket error: " + e.getMessage());
                        }
                    }
                }

            } catch (Exception e) {
                e.printStackTrace();
            }

        });

        t.setDaemon(true);
        t.start();
    }

    // =========================
    // RENDER LOOP
    // =========================
    private void startRender() {

        AnimationTimer timer = new AnimationTimer() {

            @Override
            public void handle(long now) {

                gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());

                // smooth + copy safely
                synchronized (lock) {
                    for (int i = 0; i < BARS; i++) {
                        currentLeft[i] += (latestLeft[i] - currentLeft[i]) * 0.2;
                        currentRight[i] += (latestRight[i] - currentRight[i]) * 0.2;
                    }
                }

                flash *= 0.92;

                drawStereo();
                drawCenterPulse();
            }
        };

        timer.start();
    }

    // =========================
    // STEREO VISUALIZER
    // =========================
    private void drawStereo() {

        double w = canvas.getWidth();
        double h = canvas.getHeight();

        double mid = w / 2;
        double barW = mid / BARS;

        for (int i = 0; i < BARS; i++) {

            double leftH = currentLeft[i] * h * 0.8;
            double rightH = currentRight[i] * h * 0.8;

            // LEFT (cyan)
            gc.setFill(Color.CYAN);
            gc.fillRect(
                    mid - (i + 1) * barW,
                    h - leftH,
                    barW - 2,
                    leftH
            );

            // RIGHT (magenta)
            gc.setFill(Color.MAGENTA);
            gc.fillRect(
                    mid + i * barW,
                    h - rightH,
                    barW - 2,
                    rightH
            );
        }
    }

    // =========================
    // CENTER BEAT PULSE
    // =========================
    private void drawCenterPulse() {

        double beat = flash;

        gc.setGlobalAlpha(0.15 + beat);

        gc.setFill(Color.WHITE);

        double size = 80 + beat * 120;

        gc.fillOval(
                canvas.getWidth() / 2 - size / 2,
                canvas.getHeight() / 2 - size / 2,
                size,
                size
        );

        gc.setGlobalAlpha(1.0);
    }

    // =========================
    // PARSER
    // =========================
    private double parse(String s) {
        try {
            return Double.parseDouble(s);
        } catch (Exception e) {
            return 0;
        }
    }

    // =========================
    // CLEAN EXIT
    // =========================
    private void stopApp() {

        running = false;

        try {
            if (clientSocket != null) clientSocket.close();
            if (serverSocket != null) serverSocket.close();
        } catch (Exception ignored) {}

        System.out.println("Stopped");
        System.exit(0);
    }

    @Override
    public void stop() {
        stopApp();
    }

    // =========================
    // MAIN
    // =========================
    public static void main(String[] args) {
        launch(args);
    }
}