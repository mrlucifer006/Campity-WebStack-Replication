<?php
$pageTitle = "Campus Task Management & Posting System";
require_once __DIR__ . '/includes/header.php';

// Aggregate metrics
$totalTasks = $pdo->query("SELECT COUNT(*) FROM quests")->fetchColumn();
$openTasks = $pdo->query("SELECT COUNT(*) FROM quests WHERE status = 'OPEN'")->fetchColumn();
$totalUsers = $pdo->query("SELECT COUNT(*) FROM users")->fetchColumn();
?>

<div class="hero-section">
    <h1 class="hero-title">Priority-Driven Campus Task Management & Posting Network</h1>
    <p class="hero-subtitle">
        Seamlessly post, prioritize, and delegate campus errands, lab assistance, and academic tasks. Built with intelligent Priority Queue scheduling, secure escrow budgeting, and verified peer delivery.
    </p>

    <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1.5rem;">
        <?php if ($currentUser): ?>
            <a href="dashboard.php" class="btn btn-primary">Go to Task Feed</a>
            <a href="post_quest.php" class="btn btn-outline">+ Post a New Task</a>
        <?php else: ?>
            <a href="register.php" class="btn btn-primary">Get Started (+100 Free Credits)</a>
            <a href="login.php" class="btn btn-outline">Student Login</a>
        <?php endif; ?>
    </div>
</div>

<div class="stats-banner">
    <div class="stat-item">
        <span class="stat-label">Total Tasks Created</span>
        <span class="stat-value primary"><?= $totalTasks ?></span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Open Active Tasks</span>
        <span class="stat-value teal"><?= $openTasks ?></span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Registered Students</span>
        <span class="stat-value emerald"><?= $totalUsers ?></span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Starter Grant</span>
        <span class="stat-value primary">100 Credits</span>
    </div>
</div>

<div class="grid-3">
    <div class="card">
        <div class="card-title">⚡ Dynamic Priority Queue Engine</div>
        <p class="quest-desc">
            Tasks are dynamically sorted using a priority heap algorithm combining Category Urgency (Medical, Urgent, Academic, Tech) with Reward Incentives and deadlines. Urgent tasks always appear first.
        </p>
    </div>

    <div class="card">
        <div class="card-title">🛡️ Escrow Budget & Stake Protection</div>
        <p class="quest-desc">
            Requesters deposit reward credits into escrow upon task posting. Student helpers lock a 10% stake to accept a task, preventing task abandonment and guaranteeing prompt completion.
        </p>
    </div>

    <div class="card">
        <div class="card-title">📈 Reputation & Tier Progression</div>
        <p class="quest-desc">
            Earn Experience Points (XP) and 5-star peer reviews upon verified completion. Advance from Junior Tasker to Associate Tasker, Senior Tasker, and Lead Coordinator!
        </p>
    </div>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
