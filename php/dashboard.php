<?php
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/includes/auth.php';
require_once __DIR__ . '/includes/PriorityQueue.php';

require_login();
$currentUser = current_user($pdo);

// 1. Fetch available tasks (Status OPEN, not posted by self)
$stmt = $pdo->prepare("
    SELECT q.*, u.username as poster_name, u.reputation as poster_reputation 
    FROM quests q 
    JOIN users u ON q.poster_id = u.id 
    WHERE q.status = 'OPEN' AND q.poster_id != ? 
    ORDER BY q.created_at DESC
");
$stmt->execute([$currentUser['id']]);
$rawAvailableTasks = $stmt->fetchAll();

// Apply Priority Queue Sorting Algorithm
$availableTasks = TaskPriorityQueue::prioritize($rawAvailableTasks);

// 2. Fetch My Assigned Tasks (where current user is the helper/solver)
$stmt = $pdo->prepare("
    SELECT q.*, u.username as poster_name 
    FROM quests q 
    JOIN users u ON q.poster_id = u.id 
    WHERE q.solver_id = ? AND q.status IN ('ACCEPTED', 'COMPLETED')
    ORDER BY q.created_at DESC
");
$stmt->execute([$currentUser['id']]);
$assignedTasks = $stmt->fetchAll();

// 3. Fetch My Posted Tasks (where current user is the requester)
$stmt = $pdo->prepare("
    SELECT q.*, u.username as solver_name 
    FROM quests q 
    LEFT JOIN users u ON q.solver_id = u.id 
    WHERE q.poster_id = ? 
    ORDER BY q.created_at DESC
");
$stmt->execute([$currentUser['id']]);
$postedTasks = $stmt->fetchAll();

$pageTitle = "Task Management Dashboard";
require_once __DIR__ . '/includes/header.php';
?>

<!-- User Progress & Economics Stats Banner -->
<div class="stats-banner">
    <div class="stat-item">
        <span class="stat-label">Wallet Balance</span>
        <span class="stat-value primary">💳 <?= number_format($currentUser['credits'], 1) ?> Cr</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Contribution XP</span>
        <span class="stat-value teal">⭐ <?= number_format($currentUser['xp']) ?> XP</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Peer Trust Rating</span>
        <span class="stat-value emerald">★ <?= number_format($currentUser['reputation'], 1) ?> / 5.0</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Tasker Level</span>
        <span class="stat-value" style="font-size: 1.15rem; color: #818cf8;"><?= htmlspecialchars($currentUser['role']) ?></span>
    </div>
</div>

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
    <div>
        <h2 style="font-size: 1.65rem; font-weight: 800; letter-spacing: -0.02em;">Priority Task Feed</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Tasks dynamically sorted by the Priority Queue Algorithm (Category Urgency + Reward).</p>
    </div>
    <div style="display: flex; gap: 0.75rem;">
        <a href="seed.php" class="btn btn-sm btn-outline" data-confirm="Populate sample campus tasks?">🎲 Load Sample Tasks</a>
        <a href="post_quest.php" class="btn btn-sm btn-primary">+ Post New Task</a>
    </div>
</div>

<!-- Section 1: Available Marketplace Tasks (Priority Queue Sorted) -->
<?php if (empty($availableTasks)): ?>
    <div class="card" style="text-align: center; padding: 3rem 1rem; margin-bottom: 2rem;">
        <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 1rem;">No open tasks currently available on campus.</p>
        <a href="seed.php" class="btn btn-sm btn-primary">Load Sample Campus Tasks</a>
    </div>
<?php else: ?>
    <div class="grid-3" style="margin-bottom: 2.5rem;">
        <?php foreach ($availableTasks as $task): 
            $stakeReq = max(10, floor($task['reward'] * 0.10));
        ?>
            <div class="quest-card priority-<?= $task['urgency_tier'] ?>">
                <div>
                    <div class="quest-header">
                        <span class="badge badge-priority">Score: <?= round($task['priority_score']) ?></span>
                        <span class="badge badge-category"><?= htmlspecialchars($task['category']) ?></span>
                    </div>

                    <h3 class="quest-title"><?= htmlspecialchars($task['title']) ?></h3>
                    <p class="quest-desc"><?= htmlspecialchars($task['description']) ?></p>

                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.75rem;">
                        Posted by <strong><?= htmlspecialchars($task['poster_name']) ?></strong> (★ <?= number_format($task['poster_reputation'], 1) ?>)
                        <?php if (!empty($task['deadline'])): ?>
                            <br><span>⏳ Due: <?= htmlspecialchars(date('M d, H:i', strtotime($task['deadline']))) ?></span>
                        <?php endif; ?>
                        <?php if (!empty($task['file_path'])): ?>
                            <br><span>📎 <a href="download.php?quest_id=<?= $task['id'] ?>">Attachment</a></span>
                        <?php endif; ?>
                    </div>
                </div>

                <div class="quest-footer">
                    <div>
                        <div class="reward-tag">💳 <?= number_format($task['reward'], 1) ?> Cr</div>
                        <span style="font-size: 0.725rem; color: var(--text-muted);">Required Stake: <?= $stakeReq ?> Cr</span>
                    </div>

                    <form method="POST" action="quest_action.php">
                        <input type="hidden" name="action" value="accept">
                        <input type="hidden" name="quest_id" value="<?= $task['id'] ?>">
                        <button type="submit" class="btn btn-sm btn-primary" data-confirm="Accept this task and lock <?= $stakeReq ?> credits stake?">Accept Task</button>
                    </form>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
<?php endif; ?>

<!-- Section 2: My Assigned Tasks (Helper Role) -->
<div style="margin-bottom: 2.5rem;">
    <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 1rem;">My Assigned Tasks (Helper Role)</h2>
    <?php if (empty($assignedTasks)): ?>
        <div class="card" style="padding: 1.5rem; color: var(--text-muted);">
            You have no active task assignments. Browse the Priority Task Feed above to accept tasks!
        </div>
    <?php else: ?>
        <div class="table-wrapper">
            <table class="table">
                <thead>
                    <tr>
                        <th>Task Title</th>
                        <th>Category</th>
                        <th>Requester</th>
                        <th>Reward</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($assignedTasks as $task): ?>
                        <tr>
                            <td><strong><?= htmlspecialchars($task['title']) ?></strong></td>
                            <td><span class="badge badge-category"><?= htmlspecialchars($task['category']) ?></span></td>
                            <td><?= htmlspecialchars($task['poster_name']) ?></td>
                            <td><span class="currency-badge">💳 <?= number_format($task['reward'], 1) ?></span></td>
                            <td>
                                <?php if ($task['status'] === 'ACCEPTED'): ?>
                                    <span class="badge badge-accepted">In Progress</span>
                                <?php else: ?>
                                    <span class="badge badge-completed">Submitted / In Review</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <?php if ($task['status'] === 'ACCEPTED'): ?>
                                    <form method="POST" action="quest_action.php" style="display:inline;">
                                        <input type="hidden" name="action" value="complete">
                                        <input type="hidden" name="quest_id" value="<?= $task['id'] ?>">
                                        <button type="submit" class="btn btn-sm btn-teal" data-confirm="Mark this task as finished and submit for verification?">Mark Finished</button>
                                    </form>
                                <?php else: ?>
                                    <span style="font-size: 0.85rem; color: var(--text-muted);">Awaiting Requester Review</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    <?php endif; ?>
</div>

<!-- Section 3: My Posted Tasks (Requester Role) -->
<div>
    <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 1rem;">My Posted Tasks (Requester Role)</h2>
    <?php if (empty($postedTasks)): ?>
        <div class="card" style="padding: 1.5rem; color: var(--text-muted);">
            You have not posted any tasks yet. <a href="post_quest.php">Post a task now</a>!
        </div>
    <?php else: ?>
        <div class="table-wrapper">
            <table class="table">
                <thead>
                    <tr>
                        <th>Task Title</th>
                        <th>Escrow Budget</th>
                        <th>Status</th>
                        <th>Assigned Helper</th>
                        <th>Posted Date</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($postedTasks as $pt): ?>
                        <tr>
                            <td><strong><?= htmlspecialchars($pt['title']) ?></strong></td>
                            <td><span class="currency-badge">💳 <?= number_format($pt['reward'], 1) ?></span></td>
                            <td>
                                <?php if ($pt['status'] === 'OPEN'): ?>
                                    <span class="badge badge-open">Open</span>
                                <?php elseif ($pt['status'] === 'ACCEPTED'): ?>
                                    <span class="badge badge-accepted">In Progress</span>
                                <?php elseif ($pt['status'] === 'COMPLETED'): ?>
                                    <span class="badge badge-completed">Submitted for Review</span>
                                <?php elseif ($pt['status'] === 'VERIFIED'): ?>
                                    <span class="badge badge-verified">Verified & Completed</span>
                                <?php endif; ?>
                            </td>
                            <td><?= $pt['solver_name'] ? htmlspecialchars($pt['solver_name']) : '<em>Unassigned</em>' ?></td>
                            <td><?= htmlspecialchars(date('M d, Y H:i', strtotime($pt['created_at']))) ?></td>
                            <td>
                                <?php if ($pt['status'] === 'COMPLETED'): ?>
                                    <form method="POST" action="quest_action.php" style="display:inline;">
                                        <input type="hidden" name="action" value="verify">
                                        <input type="hidden" name="quest_id" value="<?= $pt['id'] ?>">
                                        <button type="submit" class="btn btn-sm btn-primary" data-confirm="Confirm task completion and release payment + stake to <?= htmlspecialchars($pt['solver_name']) ?>?">Verify & Pay</button>
                                    </form>
                                <?php elseif ($pt['status'] === 'VERIFIED'): ?>
                                    <span style="font-size: 0.85rem; color: var(--status-open);">Completed & Paid</span>
                                <?php else: ?>
                                    <span style="font-size: 0.85rem; color: var(--text-muted);">&mdash;</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    <?php endif; ?>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
