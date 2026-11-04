package com.campity.model;

import java.io.Serializable;
import java.sql.Timestamp;

public class Quest implements Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private String title;
    private String description;
    private String category;
    private double reward;
    private double stakeAmount;
    private String status;        // OPEN, ACCEPTED, COMPLETED, VERIFIED
    private String escrowStatus;  // HELD, RELEASED
    private Timestamp createdAt;
    private Timestamp deadline;
    private Timestamp acceptedAt;
    private int posterId;
    private Integer solverId;     // Nullable
    private String filePath;

    // Joined / Calculated fields
    private String posterName;
    private double posterReputation;
    private String solverName;
    private double priorityScore;
    private String urgencyTier;

    public Quest() {
        this.status = "OPEN";
        this.escrowStatus = "HELD";
        this.stakeAmount = 0.0;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public double getReward() { return reward; }
    public void setReward(double reward) { this.reward = reward; }

    public double getStakeAmount() { return stakeAmount; }
    public void setStakeAmount(double stakeAmount) { this.stakeAmount = stakeAmount; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getEscrowStatus() { return escrowStatus; }
    public void setEscrowStatus(String escrowStatus) { this.escrowStatus = escrowStatus; }

    public Timestamp getCreatedAt() { return createdAt; }
    public void setCreatedAt(Timestamp createdAt) { this.createdAt = createdAt; }

    public Timestamp getDeadline() { return deadline; }
    public void setDeadline(Timestamp deadline) { this.deadline = deadline; }

    public Timestamp getAcceptedAt() { return acceptedAt; }
    public void setAcceptedAt(Timestamp acceptedAt) { this.acceptedAt = acceptedAt; }

    public int getPosterId() { return posterId; }
    public void setPosterId(int posterId) { this.posterId = posterId; }

    public Integer getSolverId() { return solverId; }
    public void setSolverId(Integer solverId) { this.solverId = solverId; }

    public String getFilePath() { return filePath; }
    public void setFilePath(String filePath) { this.filePath = filePath; }

    public String getPosterName() { return posterName; }
    public void setPosterName(String posterName) { this.posterName = posterName; }

    public double getPosterReputation() { return posterReputation; }
    public void setPosterReputation(double posterReputation) { this.posterReputation = posterReputation; }

    public String getSolverName() { return solverName; }
    public void setSolverName(String solverName) { this.solverName = solverName; }

    public double getPriorityScore() { return priorityScore; }
    public void setPriorityScore(double priorityScore) { this.priorityScore = priorityScore; }

    public String getUrgencyTier() { return urgencyTier; }
    public void setUrgencyTier(String urgencyTier) { this.urgencyTier = urgencyTier; }
}
