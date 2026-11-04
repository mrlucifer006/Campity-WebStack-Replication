package com.campity.algorithm;

import com.campity.model.Quest;

import java.util.*;

/**
 * Priority Queue Implementation for Task Ranking
 * Replicates Python's heapq priority queue in Java using java.util.PriorityQueue.
 */
public class TaskPriorityQueue {

    private static final Map<String, Integer> CATEGORY_WEIGHTS = new HashMap<>();

    static {
        CATEGORY_WEIGHTS.put("Medical", 100);
        CATEGORY_WEIGHTS.put("Urgent", 90);
        CATEGORY_WEIGHTS.put("Tech Support", 70);
        CATEGORY_WEIGHTS.put("Academics", 60);
        CATEGORY_WEIGHTS.put("Logistics", 50);
        CATEGORY_WEIGHTS.put("Labor", 40);
    }

    /**
     * Compute composite score for a quest
     */
    public static double calculateScore(Quest q) {
        int weight = CATEGORY_WEIGHTS.getOrDefault(q.getCategory(), 30);
        double reward = q.getReward();

        double deadlineBonus = 0;
        if (q.getDeadline() != null) {
            long diffMs = q.getDeadline().getTime() - System.currentTimeMillis();
            double hoursLeft = diffMs / (1000.0 * 3600.0);
            if (hoursLeft > 0 && hoursLeft <= 24) {
                deadlineBonus = (24 - hoursLeft) * 2;
            }
        }

        return (weight * 10.0) + (reward * 0.5) + deadlineBonus;
    }

    /**
     * Sorts quests in max-heap priority order
     */
    public static List<Quest> prioritize(List<Quest> rawQuests) {
        if (rawQuests == null || rawQuests.isEmpty()) {
            return new ArrayList<>();
        }

        // Custom Comparator for Max-Heap behavior
        Comparator<Quest> priorityComparator = (q1, q2) -> {
            int scoreCompare = Double.compare(q2.getPriorityScore(), q1.getPriorityScore());
            if (scoreCompare != 0) {
                return scoreCompare;
            }
            if (q1.getCreatedAt() != null && q2.getCreatedAt() != null) {
                return q2.getCreatedAt().compareTo(q1.getCreatedAt());
            }
            return 0;
        };

        PriorityQueue<Quest> pq = new PriorityQueue<>(rawQuests.size(), priorityComparator);

        for (Quest q : rawQuests) {
            double score = calculateScore(q);
            q.setPriorityScore(score);

            if (score >= 850) {
                q.setUrgencyTier("high");
            } else if (score >= 500) {
                q.setUrgencyTier("med");
            } else {
                q.setUrgencyTier("low");
            }

            pq.offer(q);
        }

        // Extract elements in prioritized order
        List<Quest> sortedList = new ArrayList<>();
        while (!pq.isEmpty()) {
            sortedList.add(pq.poll());
        }

        return sortedList;
    }
}
