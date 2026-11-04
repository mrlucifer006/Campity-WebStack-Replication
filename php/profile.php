<?php
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/includes/auth.php';

require_login();
$currentUser = current_user($pdo);

// Fetch transaction history
$stmt = $pdo->prepare("
    SELECT t.*, q.title as quest_title 
    FROM transactions t 
    LEFT JOIN quests q ON t.quest_id = q.id 
    WHERE t.sender_id = ? OR t.receiver_id = ? 
    ORDER BY t.timestamp DESC 
    LIMIT 25
");
$stmt->execute([$currentUser['id'], $currentUser['id']]);
$transactions = $stmt->fetchAll();

$pageTitle = "Tasker Profile";
require_once __DIR__ . '/includes/header.php';
?>

<div class="stats-banner">
    <div class="stat-item">
        <span class="stat-label">Username</span>
        <span class="stat-value"><?= htmlspecialchars($currentUser['username']) ?></span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Proficiency Level</span>
        <span class="stat-value" style="color: #818cf8;"><?= htmlspecialchars($currentUser['role']) ?></span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Available Balance</span>
        <span class="stat-value primary">💳 <?= number_format($currentUser['credits'], 1) ?> Cr</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Peer Trust Rating</span>
        <span class="stat-value emerald">★ <?= number_format($currentUser['reputation'], 1) ?> / 5.0</span>
    </div>
</div>

<div class="grid-2">
    <!-- Rank Progression & Leveling Details -->
    <div class="card">
        <h3 class="card-title">Tasker Level Progression</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
            Advance your campus tasker tier by successfully completing tasks and earning XP:
        </p>
        <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.75rem;">
            <li style="display: flex; justify-content: space-between; padding: 0.5rem; background: rgba(255,255,255,0.03); border-radius: 6px;">
                <span>Junior Tasker</span>
                <span style="color: var(--text-muted);">0 - 100 XP</span>
            </li>
            <li style="display: flex; justify-content: space-between; padding: 0.5rem; background: rgba(255,255,255,0.03); border-radius: 6px;">
                <span>Associate Tasker</span>
                <span style="color: var(--accent-teal);">101 - 500 XP</span>
            </li>
            <li style="display: flex; justify-content: space-between; padding: 0.5rem; background: rgba(255,255,255,0.03); border-radius: 6px;">
                <span>Senior Tasker</span>
                <span style="color: #818cf8;">501 - 1000 XP</span>
            </li>
            <li style="display: flex; justify-content: space-between; padding: 0.5rem; background: rgba(255,255,255,0.03); border-radius: 6px;">
                <span>Lead Coordinator</span>
                <span style="color: var(--accent-emerald);">1000+ XP</span>
            </li>
        </ul>
    </div>

    <!-- Account Details -->
    <div class="card">
        <h3 class="card-title">Account & Security Status</h3>
        <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 0.5rem;">
            Student Account ID: <strong>#<?= $currentUser['id'] ?></strong>
        </p>
        <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 0.5rem;">
            Registered Date: <strong><?= htmlspecialchars(date('M d, Y', strtotime($currentUser['created_at']))) ?></strong>
        </p>
        <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1.5rem;">
            Total Earned XP: <strong style="color: #818cf8;"><?= number_format($currentUser['xp']) ?> XP</strong>
        </p>
        <a href="logout.php" class="btn btn-sm btn-danger">Log Out of System</a>
    </div>
</div>

<!-- Transaction Ledger -->
<div style="margin-top: 2rem;">
    <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 1rem;">Credit Transaction & Escrow Ledger</h2>
    <?php if (empty($transactions)): ?>
        <div class="card" style="padding: 1.5rem; color: var(--text-muted);">
            No transaction records found.
        </div>
    <?php else: ?>
        <div class="table-wrapper">
            <table class="table">
                <thead>
                    <tr>
                        <th>Date & Time</th>
                        <th>Transaction Type</th>
                        <th>Associated Task</th>
                        <th>Amount</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($transactions as $tx): 
                        $isCredit = ($tx['receiver_id'] == $currentUser['id']);
                        $sign = $isCredit ? '+' : '-';
                        $color = $isCredit ? 'var(--status-open)' : 'var(--status-disputed)';
                    ?>
                        <tr>
                            <td><?= htmlspecialchars(date('M d, Y H:i:s', strtotime($tx['timestamp']))) ?></td>
                            <td><span class="badge badge-category"><?= htmlspecialchars($tx['tx_type']) ?></span></td>
                            <td><?= $tx['quest_title'] ? htmlspecialchars($tx['quest_title']) : '<em>System Starter Grant</em>' ?></td>
                            <td style="font-weight: 700; color: <?= $color ?>; font-family: 'JetBrains Mono', monospace;">
                                <?= $sign ?><?= number_format($tx['amount'], 1) ?> Credits
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    <?php endif; ?>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
