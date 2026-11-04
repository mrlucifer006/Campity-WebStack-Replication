package com.campity.dao;

import com.campity.model.Transaction;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class TransactionDAO {

    public static boolean recordTransaction(Connection conn, Integer senderId, Integer receiverId, double amount, String txType, Integer questId) throws SQLException {
        String query = "INSERT INTO transactions (sender_id, receiver_id, amount, tx_type, quest_id) VALUES (?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = conn.prepareStatement(query)) {
            if (senderId != null) stmt.setInt(1, senderId); else stmt.setNull(1, Types.INTEGER);
            if (receiverId != null) stmt.setInt(2, receiverId); else stmt.setNull(2, Types.INTEGER);
            stmt.setDouble(3, amount);
            stmt.setString(4, txType);
            if (questId != null) stmt.setInt(5, questId); else stmt.setNull(5, Types.INTEGER);
            return stmt.executeUpdate() > 0;
        }
    }

    public static boolean recordTransaction(Integer senderId, Integer receiverId, double amount, String txType, Integer questId) {
        try (Connection conn = DBUtil.getConnection()) {
            return recordTransaction(conn, senderId, receiverId, amount, txType, questId);
        } catch (SQLException e) {
            System.err.println("Transaction record error: " + e.getMessage());
            return false;
        }
    }

    public List<Transaction> getTransactionsForUser(int userId, int limit) {
        List<Transaction> list = new ArrayList<>();
        String query = "SELECT t.*, q.title as quest_title FROM transactions t " +
                       "LEFT JOIN quests q ON t.quest_id = q.id " +
                       "WHERE t.sender_id = ? OR t.receiver_id = ? " +
                       "ORDER BY t.timestamp DESC LIMIT ?";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, userId);
            stmt.setInt(2, userId);
            stmt.setInt(3, limit);

            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    Transaction t = new Transaction();
                    t.setId(rs.getInt("id"));
                    int sender = rs.getInt("sender_id");
                    t.setSenderId(rs.wasNull() ? null : sender);
                    int receiver = rs.getInt("receiver_id");
                    t.setReceiverId(rs.wasNull() ? null : receiver);
                    t.setAmount(rs.getDouble("amount"));
                    t.setTxType(rs.getString("tx_type"));
                    t.setTimestamp(rs.getTimestamp("timestamp"));
                    int qId = rs.getInt("quest_id");
                    t.setQuestId(rs.wasNull() ? null : qId);
                    t.setQuestTitle(rs.getString("quest_title"));
                    list.add(t);
                }
            }
        } catch (SQLException e) {
            System.err.println("Transaction query error: " + e.getMessage());
        }
        return list;
    }
}
