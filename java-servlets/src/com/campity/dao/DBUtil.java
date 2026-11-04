package com.campity.dao;

import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class DBUtil {

    private static final String DB_FILE = "campity.db";
    private static final String DB_URL = "jdbc:sqlite:" + DB_FILE;

    static {
        try {
            Class.forName("org.sqlite.JDBC");
            initSchema();
        } catch (ClassNotFoundException e) {
            System.err.println("SQLite JDBC Driver not found: " + e.getMessage());
        }
    }

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(DB_URL);
    }

    private static void initSchema() {
        try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
            stmt.executeUpdate("CREATE TABLE IF NOT EXISTS users (" +
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                    "username TEXT UNIQUE NOT NULL, " +
                    "password TEXT NOT NULL, " +
                    "credits REAL DEFAULT 100.0, " +
                    "xp INTEGER DEFAULT 0, " +
                    "reputation REAL DEFAULT 5.0, " +
                    "role TEXT DEFAULT 'Guest User', " +
                    "badges TEXT DEFAULT '[]', " +
                    "created_at DATETIME DEFAULT CURRENT_TIMESTAMP)");

            stmt.executeUpdate("CREATE TABLE IF NOT EXISTS quests (" +
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                    "title TEXT NOT NULL, " +
                    "description TEXT NOT NULL, " +
                    "category TEXT NOT NULL, " +
                    "reward REAL NOT NULL, " +
                    "stake_amount REAL DEFAULT 0.0, " +
                    "status TEXT DEFAULT 'OPEN', " +
                    "escrow_status TEXT DEFAULT 'HELD', " +
                    "created_at DATETIME DEFAULT CURRENT_TIMESTAMP, " +
                    "deadline DATETIME, " +
                    "accepted_at DATETIME, " +
                    "poster_id INTEGER NOT NULL, " +
                    "solver_id INTEGER, " +
                    "file_path TEXT, " +
                    "FOREIGN KEY (poster_id) REFERENCES users(id), " +
                    "FOREIGN KEY (solver_id) REFERENCES users(id))");

            stmt.executeUpdate("CREATE TABLE IF NOT EXISTS transactions (" +
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                    "sender_id INTEGER, " +
                    "receiver_id INTEGER, " +
                    "amount REAL NOT NULL, " +
                    "tx_type TEXT NOT NULL, " +
                    "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, " +
                    "quest_id INTEGER, " +
                    "FOREIGN KEY (sender_id) REFERENCES users(id), " +
                    "FOREIGN KEY (receiver_id) REFERENCES users(id), " +
                    "FOREIGN KEY (quest_id) REFERENCES quests(id))");

        } catch (SQLException e) {
            System.err.println("Database schema initialization notice: " + e.getMessage());
        }
    }
}
