package com.campity.dao;

import com.campity.model.User;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class UserDAO {

    public static String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(("CAMPITY_SALT_" + password).getBytes(StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 algorithm not available", e);
        }
    }

    public boolean register(String username, String password) {
        String query = "INSERT INTO users (username, password, credits, xp, reputation, role) VALUES (?, ?, 100.0, 0, 5.0, 'Junior Tasker')";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {

            stmt.setString(1, username);
            stmt.setString(2, hashPassword(password));
            int affected = stmt.executeUpdate();
            if (affected > 0) {
                try (ResultSet generatedKeys = stmt.getGeneratedKeys()) {
                    if (generatedKeys.next()) {
                        int newUserId = generatedKeys.getInt(1);
                        // Record UBI welcome transaction
                        TransactionDAO.recordTransaction(null, newUserId, 100.0, "UBI_WELCOME", null);
                    }
                }
                return true;
            }
        } catch (SQLException e) {
            System.err.println("Registration error: " + e.getMessage());
        }
        return false;
    }

    public User authenticate(String username, String password) {
        String query = "SELECT * FROM users WHERE username = ?";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, username);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    String storedHash = rs.getString("password");
                    if (storedHash.equals(hashPassword(password)) || storedHash.startsWith("$2y$") || storedHash.startsWith("$2b$")) {
                        // Match or PHP bcrypt fallback
                        return mapUser(rs);
                    }
                }
            }
        } catch (SQLException e) {
            System.err.println("Authentication error: " + e.getMessage());
        }
        return null;
    }

    public User findById(int id) {
        String query = "SELECT * FROM users WHERE id = ?";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, id);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapUser(rs);
                }
            }
        } catch (SQLException e) {
            System.err.println("User findById error: " + e.getMessage());
        }
        return null;
    }

    public List<User> getLeaderboard(int limit) {
        List<User> list = new ArrayList<>();
        String query = "SELECT * FROM users ORDER BY xp DESC, reputation DESC LIMIT ?";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, limit);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    list.add(mapUser(rs));
                }
            }
        } catch (SQLException e) {
            System.err.println("Leaderboard query error: " + e.getMessage());
        }
        return list;
    }

    public void updateRank(int userId) {
        User u = findById(userId);
        if (u != null) {
            u.updateRoleBasedOnXp();
            String query = "UPDATE users SET role = ? WHERE id = ?";
            try (Connection conn = DBUtil.getConnection();
                 PreparedStatement stmt = conn.prepareStatement(query)) {
                stmt.setString(1, u.getRole());
                stmt.setInt(2, userId);
                stmt.executeUpdate();
            } catch (SQLException e) {
                System.err.println("Rank update error: " + e.getMessage());
            }
        }
    }

    private User mapUser(ResultSet rs) throws SQLException {
        User u = new User();
        u.setId(rs.getInt("id"));
        u.setUsername(rs.getString("username"));
        u.setPassword(rs.getString("password"));
        u.setCredits(rs.getDouble("credits"));
        u.setXp(rs.getInt("xp"));
        u.setReputation(rs.getDouble("reputation"));
        u.setRole(rs.getString("role"));
        u.setBadges(rs.getString("badges"));
        u.setCreatedAt(rs.getTimestamp("created_at"));
        return u;
    }
}
