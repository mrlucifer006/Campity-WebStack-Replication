<?php
/**
 * Campity Intelligent Task Prioritization Engine
 * Replicates Python's heapq priority queue logic in PHP.
 * 
 * Logic:
 * Tasks are prioritized dynamically based on:
 * 1. Category Urgency Weight:
 *    - Medical: 100
 *    - Urgent: 90
 *    - Tech Support: 70
 *    - Academics: 60
 *    - Logistics: 50
 *    - Labor: 40
 *    - Default: 30
 * 2. Economic Reward Value (Higher reward = higher incentive)
 * 3. Proximity to Deadline (Closer deadline = higher urgency boost)
 */

class TaskPriorityQueue {
    private static $categoryWeights = [
        'Medical'      => 100,
        'Urgent'       => 90,
        'Tech Support' => 70,
        'Academics'    => 60,
        'Logistics'    => 50,
        'Labor'        => 40
    ];

    /**
     * Compute composite priority score for a quest
     */
    public static function calculateScore(array $quest): float {
        $category = $quest['category'] ?? 'Labor';
        $weight = self::$categoryWeights[$category] ?? 30;
        $reward = (float)($quest['reward'] ?? 0);

        // Calculate deadline bonus
        $deadlineBonus = 0;
        if (!empty($quest['deadline'])) {
            $hoursLeft = (strtotime($quest['deadline']) - time()) / 3600;
            if ($hoursLeft > 0 && $hoursLeft <= 24) {
                $deadlineBonus = (24 - $hoursLeft) * 2; // Closer deadline gives up to 48 points
            }
        }

        // Composite formula: Category Weight (scaled) + Reward Factor + Deadline Urgency
        return ($weight * 10) + ($reward * 0.5) + $deadlineBonus;
    }

    /**
     * Prioritize and sort an array of quests
     */
    public static function prioritize(array $quests): array {
        foreach ($quests as &$quest) {
            $quest['priority_score'] = self::calculateScore($quest);
            
            // Assign human-readable urgency tier
            if ($quest['priority_score'] >= 850) {
                $quest['urgency_tier'] = 'high';
            } elseif ($quest['priority_score'] >= 500) {
                $quest['urgency_tier'] = 'med';
            } else {
                $quest['urgency_tier'] = 'low';
            }
        }
        unset($quest);

        // Sort descending by priority_score
        usort($quests, function ($a, $b) {
            if ($a['priority_score'] == $b['priority_score']) {
                return strtotime($b['created_at']) <=> strtotime($a['created_at']);
            }
            return ($b['priority_score'] <=> $a['priority_score']);
        });

        return $quests;
    }
}
