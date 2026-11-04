<?php
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/includes/auth.php';

$pageTitle = "Tasker Rankings & Leaderboard";
require_once __DIR__ . '/includes/header.php';

// Fetch top users by XP
$stmt = $pdo->query("
    SELECT u.*, 
           (SELECT COUNT(*) FROM quests WHERE solver_id = u.id AND status = 'VERIFIED') as completed_count
    FROM users u 
    ORDER BY u.xp DESC, u.reputation DESC 
    LIMIT 20
");
$topUsers = $stmt->fetchAll();
?>

<div style="margin-bottom: 2rem; text-align: center;">
    <h1 class="hero-title" style="font-size: 2.2rem; margin-bottom: 0.5rem;">Campus Tasker Leaderboard</h1>
    <p style="color: var(--text-muted);">Top contributing student taskers ranked by Contribution Points (XP), Peer Rating, and Verified Deliveries.</p>
</div>

<div class="table-wrapper">
    <table class="table">
        <thead>
            <tr>
                <th style="width: 80px;">Rank</th>
                <th>Student Tasker</th>
                <th>Proficiency Level</th>
                <th>Trust Rating</th>
                <th>Completed Tasks</th>
                <th>Contribution Score</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($topUsers as $index => $user): 
                $rank = $index + 1;
                $medal = $rank === 1 ? '🥇' : ($rank === 2 ? '🥈' : ($rank === 3 ? '🥉' : "#$rank"));
            ?>
                <tr>
                    <td style="font-weight: 800; font-size: 1.1rem; color: <?= $rank <= 3 ? '#818cf8' : 'var(--text-muted)' ?>;">
                        <?= $medal ?>
                    </td>
                    <td>
                        <strong><?= htmlspecialchars($user['username']) ?></strong>
                        <?php if ($currentUser && $currentUser['id'] == $user['id']): ?>
                            <span class="badge badge-category" style="margin-left: 0.5rem;">You</span>
                        <?php endif; ?>
                    </td>
                    <td><span class="badge badge-category"><?= htmlspecialchars($user['role']) ?></span></td>
                    <td>★ <?= number_format($user['reputation'], 1) ?></td>
                    <td><?= $user['completed_count'] ?> Tasks</td>
                    <td style="font-weight: 700; color: #818cf8; font-family: 'JetBrains Mono', monospace;">
                        <?= number_format($user['xp']) ?> XP
                    </td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
