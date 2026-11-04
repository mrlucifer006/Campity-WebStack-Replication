package com.campity.dao;

import com.campity.model.Quest;
import com.campity.model.User;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class QuestDAO {

    public boolean createQuest(Quest q) {
        String deductQuery = "UPDATE users SET credits = credits - ? WHERE id = ? AND credits >= ?";
        String insertQuery = "INSERT INTO quests (title, description, category, reward, poster_id, status, escrow_status, deadline, file_path) " +
                             "VALUES (?, ?, ?, ?, ?, 'OPEN', 'HELD', ?, ?)";

        try (Connection conn = DBUtil.getConnection()) {
            conn.setAutoCommit(false);
            try {
                // Deduct Escrow
                try (PreparedStatement deductStmt = conn.prepareStatement(deductQuery)) {
                    deductStmt.setDouble(1, q.getReward());
                    deductStmt.setInt(2, q.getPosterId());
                    deductStmt.setDouble(3, q.getReward());
                    int rows = deductStmt.executeUpdate();
                    if (rows == 0) {
                        conn.rollback();
                        return false; // Insufficient funds
                    }
                }

                // Insert Quest
                int questId;
                try (PreparedStatement insertStmt = conn.prepareStatement(insertQuery, Statement.RETURN_GENERATED_KEYS)) {
                    insertStmt.setString(1, q.getTitle());
                    insertStmt.setString(2, q.getDescription());
                    insertStmt.setString(3, q.getCategory());
                    insertStmt.setDouble(4, q.getReward());
                    insertStmt.setInt(5, q.getPosterId());
                    insertStmt.setTimestamp(6, q.getDeadline());
                    insertStmt.setString(7, q.getFilePath());
                    insertStmt.executeUpdate();

                    try (ResultSet keys = insertStmt.getGeneratedKeys()) {
                        if (keys.next()) {
                            questId = keys.getInt(1);
                        } else {
                            conn.rollback();
                            return false;
                        }
                    }
                }

                // Record Escrow Transaction using the SAME active connection
                TransactionDAO.recordTransaction(conn, q.getPosterId(), null, q.getReward(), "ESCROW_DEPOSIT", questId);

                conn.commit();
                return true;
            } catch (SQLException ex) {
                conn.rollback();
                throw ex;
            } finally {
                conn.setAutoCommit(true);
            }
        } catch (SQLException e) {
            System.err.println("Task creation error: " + e.getMessage());
            return false;
        }
    }

    public List<Quest> getOpenQuests(int excludeUserId) {
        List<Quest> list = new ArrayList<>();
        String query = "SELECT q.*, u.username as poster_name, u.reputation as poster_reputation " +
                       "FROM quests q JOIN users u ON q.poster_id = u.id " +
                       "WHERE q.status = 'OPEN' AND q.poster_id != ? ORDER BY q.created_at DESC";

        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, excludeUserId);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    list.add(mapQuest(rs));
                }
            }
        } catch (SQLException e) {
            System.err.println("Open tasks query error: " + e.getMessage());
        }
        return list;
    }

    public List<Quest> getMissionsForSolver(int solverId) {
        List<Quest> list = new ArrayList<>();
        String query = "SELECT q.*, u.username as poster_name, u.reputation as poster_reputation " +
                       "FROM quests q JOIN users u ON q.poster_id = u.id " +
                       "WHERE q.solver_id = ? AND q.status IN ('ACCEPTED', 'COMPLETED') ORDER BY q.created_at DESC";

        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, solverId);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    list.add(mapQuest(rs));
                }
            }
        } catch (SQLException e) {
            System.err.println("Assigned tasks query error: " + e.getMessage());
        }
        return list;
    }

    public List<Quest> getQuestsByPoster(int posterId) {
        List<Quest> list = new ArrayList<>();
        String query = "SELECT q.*, u.username as solver_name " +
                       "FROM quests q LEFT JOIN users u ON q.solver_id = u.id " +
                       "WHERE q.poster_id = ? ORDER BY q.created_at DESC";

        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, posterId);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    Quest q = mapQuest(rs);
                    q.setSolverName(rs.getString("solver_name"));
                    list.add(q);
                }
            }
        } catch (SQLException e) {
            System.err.println("Posted tasks query error: " + e.getMessage());
        }
        return list;
    }

    public Quest findById(int questId) {
        String query = "SELECT q.*, u.username as poster_name, u.reputation as poster_reputation " +
                       "FROM quests q JOIN users u ON q.poster_id = u.id WHERE q.id = ?";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, questId);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapQuest(rs);
                }
            }
        } catch (SQLException e) {
            System.err.println("Task findById error: " + e.getMessage());
        }
        return null;
    }

    public boolean acceptQuest(int questId, int solverId) {
        Quest q = findById(questId);
        if (q == null || !"OPEN".equals(q.getStatus()) || q.getPosterId() == solverId) {
            return false;
        }

        double stake = Math.max(10, Math.floor(q.getReward() * 0.10));

        String deductQuery = "UPDATE users SET credits = credits - ? WHERE id = ? AND credits >= ?";
        String updateQuest = "UPDATE quests SET status = 'ACCEPTED', solver_id = ?, stake_amount = ?, accepted_at = CURRENT_TIMESTAMP WHERE id = ? AND status = 'OPEN'";

        try (Connection conn = DBUtil.getConnection()) {
            conn.setAutoCommit(false);
            try {
                try (PreparedStatement deductStmt = conn.prepareStatement(deductQuery)) {
                    deductStmt.setDouble(1, stake);
                    deductStmt.setInt(2, solverId);
                    deductStmt.setDouble(3, stake);
                    if (deductStmt.executeUpdate() == 0) {
                        conn.rollback();
                        return false; // Insufficient stake
                    }
                }

                try (PreparedStatement updateStmt = conn.prepareStatement(updateQuest)) {
                    updateStmt.setInt(1, solverId);
                    updateStmt.setDouble(2, stake);
                    updateStmt.setInt(3, questId);
                    if (updateStmt.executeUpdate() == 0) {
                        conn.rollback();
                        return false;
                    }
                }

                // Record Stake Lock on SAME active connection
                TransactionDAO.recordTransaction(conn, solverId, null, stake, "STAKE_LOCK", questId);

                conn.commit();
                return true;
            } catch (SQLException ex) {
                conn.rollback();
                throw ex;
            } finally {
                conn.setAutoCommit(true);
            }
        } catch (SQLException e) {
            System.err.println("Task accept error: " + e.getMessage());
            return false;
        }
    }

    public boolean completeQuest(int questId, int solverId) {
        String query = "UPDATE quests SET status = 'COMPLETED' WHERE id = ? AND solver_id = ? AND status = 'ACCEPTED'";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, questId);
            stmt.setInt(2, solverId);
            return stmt.executeUpdate() > 0;
        } catch (SQLException e) {
            System.err.println("Task complete error: " + e.getMessage());
            return false;
        }
    }

    public boolean verifyQuest(int questId, int posterId) {
        Quest q = findById(questId);
        if (q == null || !"COMPLETED".equals(q.getStatus()) || q.getPosterId() != posterId || q.getSolverId() == null) {
            return false;
        }

        int solverId = q.getSolverId();
        double reward = q.getReward();
        double stake = q.getStakeAmount();
        double totalPayout = reward + stake;

        String creditSolver = "UPDATE users SET credits = credits + ?, xp = xp + 50, reputation = MIN(5.0, reputation + 0.1) WHERE id = ?";
        String updateQuest = "UPDATE quests SET status = 'VERIFIED', escrow_status = 'RELEASED' WHERE id = ?";

        try (Connection conn = DBUtil.getConnection()) {
            conn.setAutoCommit(false);
            try {
                try (PreparedStatement creditStmt = conn.prepareStatement(creditSolver)) {
                    creditStmt.setDouble(1, totalPayout);
                    creditStmt.setInt(2, solverId);
                    creditStmt.executeUpdate();
                }

                try (PreparedStatement updateStmt = conn.prepareStatement(updateQuest)) {
                    updateStmt.setInt(1, questId);
                    updateStmt.executeUpdate();
                }

                // Record transactions on SAME active connection
                TransactionDAO.recordTransaction(conn, null, solverId, reward, "ESCROW_PAYOUT", questId);
                TransactionDAO.recordTransaction(conn, null, solverId, stake, "STAKE_RETURN", questId);

                conn.commit();

                // Recalculate rank
                new UserDAO().updateRank(solverId);
                return true;
            } catch (SQLException ex) {
                conn.rollback();
                throw ex;
            } finally {
                conn.setAutoCommit(true);
            }
        } catch (SQLException e) {
            System.err.println("Task verify error: " + e.getMessage());
            return false;
        }
    }

    public void seedStarterQuests(int posterId) {
        String query = "INSERT INTO quests (title, description, category, reward, poster_id, status, escrow_status, deadline) VALUES (?, ?, ?, ?, ?, 'OPEN', 'HELD', ?)";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            Object[][] sampleData = {
                {"Emergency Prescription Pickup from Campus Infirmary", "Urgent pickup of prescribed medication from Main Gate Health Center.", "Medical", 120.0, new Timestamp(System.currentTimeMillis() + 3 * 3600 * 1000)},
                {"Return 4 Library Research Books to Reserve Desk", "Drop off borrowed engineering reference volumes before 5 PM.", "Logistics", 45.0, new Timestamp(System.currentTimeMillis() + 24 * 3600 * 1000)},
                {"Lecture Hall 204 HDMI Projector Calibration & Audio Check", "Test and configure projector HDMI input before 2 PM seminar.", "Tech Support", 80.0, new Timestamp(System.currentTimeMillis() + 5 * 3600 * 1000)},
                {"Data Structures AVL & B-Tree Exam Review Notes", "Clean handwritten notes covering AVL rotations and B-Tree insertions.", "Academics", 95.0, new Timestamp(System.currentTimeMillis() + 12 * 3600 * 1000)},
                {"Assemble Student Robotics Club Display Booth", "Assist in mounting registration banners and running power cables.", "Labor", 50.0, new Timestamp(System.currentTimeMillis() + 48 * 3600 * 1000)}
            };

            for (Object[] row : sampleData) {
                stmt.setString(1, (String) row[0]);
                stmt.setString(2, (String) row[1]);
                stmt.setString(3, (String) row[2]);
                stmt.setDouble(4, (Double) row[3]);
                stmt.setInt(5, posterId);
                stmt.setTimestamp(6, (Timestamp) row[4]);
                stmt.executeUpdate();
            }
        } catch (SQLException e) {
            System.err.println("Starter task seed error: " + e.getMessage());
        }
    }

    private Quest mapQuest(ResultSet rs) throws SQLException {
        Quest q = new Quest();
        q.setId(rs.getInt("id"));
        q.setTitle(rs.getString("title"));
        q.setDescription(rs.getString("description"));
        q.setCategory(rs.getString("category"));
        q.setReward(rs.getDouble("reward"));
        q.setStakeAmount(rs.getDouble("stake_amount"));
        q.setStatus(rs.getString("status"));
        q.setEscrowStatus(rs.getString("escrow_status"));
        q.setCreatedAt(rs.getTimestamp("created_at"));
        q.setDeadline(rs.getTimestamp("deadline"));
        q.setAcceptedAt(rs.getTimestamp("accepted_at"));
        q.setPosterId(rs.getInt("poster_id"));
        int solver = rs.getInt("solver_id");
        q.setSolverId(rs.wasNull() ? null : solver);
        q.setFilePath(rs.getString("file_path"));

        try {
            q.setPosterName(rs.getString("poster_name"));
            q.setPosterReputation(rs.getDouble("poster_reputation"));
        } catch (SQLException ignored) {}

        return q;
    }
}
