<?php
// Campity Database Connection & Auto-Migration (PDO SQLite)

$dbPath = __DIR__ . '/../../campity.db';

try {
    $pdo = new PDO("sqlite:" . $dbPath);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

    // Auto-create database schema matching Campity models
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            credits REAL DEFAULT 100.0,
            xp INTEGER DEFAULT 0,
            reputation REAL DEFAULT 5.0,
            role TEXT DEFAULT 'Junior Tasker',
            badges TEXT DEFAULT '[]',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            reward REAL NOT NULL,
            stake_amount REAL DEFAULT 0.0,
            status TEXT DEFAULT 'OPEN',
            escrow_status TEXT DEFAULT 'HELD',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            deadline DATETIME,
            accepted_at DATETIME,
            poster_id INTEGER NOT NULL,
            solver_id INTEGER,
            file_path TEXT,
            FOREIGN KEY (poster_id) REFERENCES users(id),
            FOREIGN KEY (solver_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            amount REAL NOT NULL,
            tx_type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            quest_id INTEGER,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id),
            FOREIGN KEY (quest_id) REFERENCES quests(id)
        );
    ");

} catch (PDOException $e) {
    die("Database Connection Error: " . htmlspecialchars($e->getMessage()));
}
