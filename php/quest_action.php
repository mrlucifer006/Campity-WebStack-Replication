<?php
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/includes/auth.php';

require_login();
$currentUser = current_user($pdo);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: dashboard.php');
    exit;
}

$action = $_POST['action'] ?? '';
$questId = (int)($_POST['quest_id'] ?? 0);

if ($questId <= 0) {
    set_flash("Invalid task identification.", "danger");
    header('Location: dashboard.php');
    exit;
}

// Fetch task
$stmt = $pdo->prepare("SELECT * FROM quests WHERE id = ?");
$stmt->execute([$questId]);
$quest = $stmt->fetch();

if (!$quest) {
    set_flash("Task not found.", "danger");
    header('Location: dashboard.php');
    exit;
}

if ($action === 'accept') {
    // Validation
    if ($quest['poster_id'] == $currentUser['id']) {
        set_flash("You cannot accept your own posted task.", "danger");
        header('Location: dashboard.php');
        exit;
    }

    if ($quest['status'] !== 'OPEN') {
        set_flash("This task has already been assigned or closed.", "warning");
        header('Location: dashboard.php');
        exit;
    }

    // Required 10% Stake
    $stake = max(10, (int)floor($quest['reward'] * 0.10));

    if ($currentUser['credits'] < $stake) {
        set_flash("Insufficient wallet credits! You need $stake Credits to stake and accept this task.", "danger");
        header('Location: dashboard.php');
        exit;
    }

    // Process Acceptance & Stake Lock
    $pdo->beginTransaction();
    try {
        // Deduct stake
        $deduct = $pdo->prepare("UPDATE users SET credits = credits - ? WHERE id = ?");
        $deduct->execute([$stake, $currentUser['id']]);

        // Update Quest
        $update = $pdo->prepare("
            UPDATE quests 
            SET status = 'ACCEPTED', solver_id = ?, stake_amount = ?, accepted_at = CURRENT_TIMESTAMP 
            WHERE id = ? AND status = 'OPEN'
        ");
        $update->execute([$currentUser['id'], $stake, $questId]);

        // Record Stake Lock Transaction
        $tx = $pdo->prepare("INSERT INTO transactions (sender_id, amount, tx_type, quest_id) VALUES (?, ?, 'STAKE_LOCK', ?)");
        $tx->execute([$currentUser['id'], $stake, $questId]);

        $pdo->commit();
        set_flash("Task successfully accepted! $stake Credits locked as accountability stake.", "success");
    } catch (Exception $e) {
        $pdo->rollBack();
        set_flash("Failed to accept task: " . $e->getMessage(), "danger");
    }

} elseif ($action === 'complete') {
    // Only assigned solver can mark complete
    if ($quest['solver_id'] != $currentUser['id']) {
        set_flash("Unauthorized operation.", "danger");
        header('Location: dashboard.php');
        exit;
    }

    if ($quest['status'] !== 'ACCEPTED') {
        set_flash("Task is not in an active in-progress state.", "warning");
        header('Location: dashboard.php');
        exit;
    }

    $update = $pdo->prepare("UPDATE quests SET status = 'COMPLETED' WHERE id = ?");
    $update->execute([$questId]);

    set_flash("Task marked finished and submitted! Awaiting requester verification.", "success");

} elseif ($action === 'verify') {
    // Only poster can verify
    if ($quest['poster_id'] != $currentUser['id']) {
        set_flash("Unauthorized operation.", "danger");
        header('Location: dashboard.php');
        exit;
    }

    if ($quest['status'] !== 'COMPLETED') {
        set_flash("Task has not been submitted as completed yet.", "warning");
        header('Location: dashboard.php');
        exit;
    }

    $solverId = $quest['solver_id'];
    $reward = (float)$quest['reward'];
    $stake = (float)$quest['stake_amount'];
    $totalPayout = $reward + $stake;

    $pdo->beginTransaction();
    try {
        // Payout reward and return stake to solver
        $creditSolver = $pdo->prepare("
            UPDATE users 
            SET credits = credits + ?, xp = xp + 50, reputation = MIN(5.0, reputation + 0.1) 
            WHERE id = ?
        ");
        $creditSolver->execute([$totalPayout, $solverId]);

        // Mark quest verified and escrow released
        $updateQuest = $pdo->prepare("
            UPDATE quests 
            SET status = 'VERIFIED', escrow_status = 'RELEASED' 
            WHERE id = ?
        ");
        $updateQuest->execute([$questId]);

        // Log Reward Payout
        $tx1 = $pdo->prepare("INSERT INTO transactions (receiver_id, amount, tx_type, quest_id) VALUES (?, ?, 'ESCROW_PAYOUT', ?)");
        $tx1->execute([$solverId, $reward, $questId]);

        // Log Stake Return
        $tx2 = $pdo->prepare("INSERT INTO transactions (receiver_id, amount, tx_type, quest_id) VALUES (?, ?, 'STAKE_RETURN', ?)");
        $tx2->execute([$solverId, $stake, $questId]);

        $pdo->commit();

        // Update solver rank if threshold crossed
        update_user_rank($pdo, $solverId);

        set_flash("Task verified! Payout of $totalPayout Credits (Reward + Stake Refund) released to helper (+50 XP).", "success");
    } catch (Exception $e) {
        $pdo->rollBack();
        set_flash("Verification failed: " . $e->getMessage(), "danger");
    }
}

header('Location: dashboard.php');
exit;
