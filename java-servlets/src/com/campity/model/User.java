package com.campity.model;

import java.io.Serializable;
import java.sql.Timestamp;

public class User implements Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private String username;
    private String password;
    private double credits;
    private int xp;
    private double reputation;
    private String role;
    private String badges;
    private Timestamp createdAt;

    public User() {
        this.credits = 100.0;
        this.xp = 0;
        this.reputation = 5.0;
        this.role = "Junior Tasker";
        this.badges = "[]";
    }

    public User(String username, String password) {
        this();
        this.username = username;
        this.password = password;
    }

    // Getters and Setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public double getCredits() { return credits; }
    public void setCredits(double credits) { this.credits = credits; }

    public int getXp() { return xp; }
    public void setXp(int xp) { this.xp = xp; }

    public double getReputation() { return reputation; }
    public void setReputation(double reputation) { this.reputation = reputation; }

    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }

    public String getBadges() { return badges; }
    public void setBadges(String badges) { this.badges = badges; }

    public Timestamp getCreatedAt() { return createdAt; }
    public void setCreatedAt(Timestamp createdAt) { this.createdAt = createdAt; }

    public void updateRoleBasedOnXp() {
        if (xp > 1000) {
            role = "Lead Coordinator";
        } else if (xp > 500) {
            role = "Senior Tasker";
        } else if (xp > 100) {
            role = "Associate Tasker";
        } else {
            role = "Junior Tasker";
        }
    }
}
