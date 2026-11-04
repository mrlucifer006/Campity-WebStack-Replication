<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/auth.php';

$currentUser = current_user($pdo);
$flash = get_flash();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= isset($pageTitle) ? htmlspecialchars($pageTitle) . ' | TaskFlow' : 'TaskFlow - Campus Task Management & Posting System' ?></title>
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="stylesheet" href="../assets/css/themes.css">
    <script src="../assets/js/app.js" defer></script>
</head>
<body>
    <header class="navbar">
        <div class="nav-container">
            <a href="index.php" class="brand-logo">
                <div class="brand-icon">✓</div>
                <span>TASK<span class="highlight">FLOW</span></span>
            </a>

            <nav>
                <ul class="nav-links">
                    <?php if ($currentUser): ?>
                        <li><a href="dashboard.php" class="nav-link <?= basename($_SERVER['PHP_SELF']) == 'dashboard.php' ? 'active' : '' ?>">Task Feed</a></li>
                        <li><a href="post_quest.php" class="nav-link <?= basename($_SERVER['PHP_SELF']) == 'post_quest.php' ? 'active' : '' ?>">+ Post Task</a></li>
                        <li><a href="leaderboard.php" class="nav-link <?= basename($_SERVER['PHP_SELF']) == 'leaderboard.php' ? 'active' : '' ?>">Tasker Rankings</a></li>
                        <li>
                            <div class="user-badge-nav">
                                <span class="currency-badge">💳 <?= number_format($currentUser['credits'], 1) ?> Cr</span>
                                <a href="profile.php" class="nav-link" style="padding:0;"><?= htmlspecialchars($currentUser['username']) ?></a>
                            </div>
                        </li>
                        <li><a href="logout.php" class="btn btn-sm btn-outline">Sign Out</a></li>
                    <?php else: ?>
                        <li><a href="index.php" class="nav-link">Overview</a></li>
                        <li><a href="login.php" class="nav-link">Log In</a></li>
                        <li><a href="register.php" class="btn btn-sm btn-primary">Sign Up (+100 Credits)</a></li>
                    <?php endif; ?>
                </ul>
            </nav>
        </div>
    </header>

    <div class="main-wrapper">
        <?php if ($flash): ?>
            <div class="alert alert-<?= htmlspecialchars($flash['type']) ?>">
                <?= htmlspecialchars($flash['message']) ?>
            </div>
        <?php endif; ?>
