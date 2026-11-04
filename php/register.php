<?php
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/includes/auth.php';

if (is_logged_in()) {
    header('Location: dashboard.php');
    exit;
}

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';

    if (empty($username) || empty($password)) {
        $error = "All fields are required.";
    } elseif (strlen($username) < 3) {
        $error = "Username must be at least 3 characters long.";
    } else {
        // Check duplicate
        $stmt = $pdo->prepare("SELECT id FROM users WHERE username = ?");
        $stmt->execute([$username]);
        if ($stmt->fetch()) {
            $error = "Username is already registered. Please choose another or log in.";
        } else {
            $hashed = password_hash($password, PASSWORD_BCRYPT);
            
            // 100 Starter Credits
            $insert = $pdo->prepare("INSERT INTO users (username, password, credits, xp, reputation, role) VALUES (?, ?, 100.0, 0, 5.0, 'Junior Tasker')");
            $insert->execute([$username, $hashed]);
            $newUserId = $pdo->lastInsertId();

            // Record initial welcome credit transaction
            $tx = $pdo->prepare("INSERT INTO transactions (sender_id, receiver_id, amount, tx_type) VALUES (NULL, ?, 100.0, 'SIGNUP_BONUS')");
            $tx->execute([$newUserId]);

            set_flash("Account successfully created! 100 Starter Credits have been deposited to your wallet.", "success");
            header('Location: login.php');
            exit;
        }
    }
}

$pageTitle = "Student Registration";
require_once __DIR__ . '/includes/header.php';
?>

<div class="form-card">
    <h2 style="text-align: center; margin-bottom: 0.5rem; font-weight: 800;">Create Student Account</h2>
    <p style="text-align: center; color: var(--text-muted); margin-bottom: 1.5rem; font-size: 0.9rem;">
        Join the campus task network and receive 100 free credits to post or accept errands.
    </p>

    <?php if ($error): ?>
        <div class="alert alert-danger"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <form method="POST" action="register.php">
        <div class="form-group">
            <label class="form-label" for="username">Student Username / ID</label>
            <input type="text" id="username" name="username" class="form-control" placeholder="e.g. sarah_mit" required autocomplete="username">
        </div>

        <div class="form-group">
            <label class="form-label" for="password">Password</label>
            <input type="password" id="password" name="password" class="form-control" placeholder="••••••••" required autocomplete="new-password">
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">Register & Claim 100 Credits</button>
    </form>

    <div style="text-align: center; margin-top: 1.5rem; font-size: 0.9rem; color: var(--text-muted);">
        Already registered? <a href="login.php">Sign in here</a>
    </div>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
