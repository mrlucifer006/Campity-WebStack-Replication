package com.campity.model;

import java.io.Serializable;
import java.sql.Timestamp;

public class Transaction implements Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private Integer senderId;
    private Integer receiverId;
    private double amount;
    private String txType; // UBI_WELCOME, ESCROW_DEPOSIT, STAKE_LOCK, ESCROW_PAYOUT, STAKE_RETURN
    private Timestamp timestamp;
    private Integer questId;
    private String questTitle;

    public Transaction() {}

    public Transaction(Integer senderId, Integer receiverId, double amount, String txType, Integer questId) {
        this.senderId = senderId;
        this.receiverId = receiverId;
        this.amount = amount;
        this.txType = txType;
        this.questId = questId;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public Integer getSenderId() { return senderId; }
    public void setSenderId(Integer senderId) { this.senderId = senderId; }

    public Integer getReceiverId() { return receiverId; }
    public void setReceiverId(Integer receiverId) { this.receiverId = receiverId; }

    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }

    public String getTxType() { return txType; }
    public void setTxType(String txType) { this.txType = txType; }

    public Timestamp getTimestamp() { return timestamp; }
    public void setTimestamp(Timestamp timestamp) { this.timestamp = timestamp; }

    public Integer getQuestId() { return questId; }
    public void setQuestId(Integer questId) { this.questId = questId; }

    public String getQuestTitle() { return questTitle; }
    public void setQuestTitle(String questTitle) { this.questTitle = questTitle; }
}
