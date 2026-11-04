<?php
// Session & User Authentication Utilities

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

/**
 * Check if a user is currently logged in
 */
function is_logged_in(): bool {
    return isset($_SESSION['user_id']);
}

/**
 * Require login, redirect to login page if guest
 */
function require_login(): void {
    if (!is_logged_in()) {
        set_flash('Please log in to access this section.', 'warning');
        header('Location: login.php');
        exit;
    }
}

/**
 * Fetch currently logged in user profile from database
 */
function current_user(PDO $pdo): ?array {
    if (!is_logged_in()) {
        return null;
    }
    $stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
    $stmt->execute([$_SESSION['user_id']]);
    $user = $stmt->fetch();
    if (!$user) {
        session_destroy();
        return null;
    }
    return $user;
}

/**
 * Recalculate and update user role/rank based on earned XP
 */
function update_user_rank(PDO $pdo, int $userId): void {
    $stmt = $pdo->prepare("SELECT xp FROM users WHERE id = ?");
    $stmt->execute([$userId]);
    $user = $stmt->fetch();
    if (!$user) return;

    $xp = (int)$user['xp'];
    if ($xp > 1000) {
        $role = 'Lead Coordinator';
    } elseif ($xp > 500) {
        $role = 'Senior Tasker';
    } elseif ($xp > 100) {
        $role = 'Associate Tasker';
    } else {
        $role = 'Junior Tasker';
    }

    $update = $pdo->prepare("UPDATE users SET role = ? WHERE id = ?");
    $update->execute([$role, $userId]);
}

/**
 * Set flash message for UI
 */
function set_flash(string $message, string $type = 'success'): void {
    $_SESSION['flash'] = [
        'message' => $message,
        'type'    => $type
    ];
}

/**
 * Retrieve and clear flash message
 */
function get_flash(): ?array {
    if (isset($_SESSION['flash'])) {
        $flash = $_SESSION['flash'];
        unset($_SESSION['flash']);
        return $flash;
    }
    return null;
}
