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
        $error = "Please provide both username and password.";
    } else {
        $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
        $stmt->execute([$username]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user['password'])) {
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            set_flash("Welcome back, " . htmlspecialchars($user['username']) . "!", "success");
            header('Location: dashboard.php');
            exit;
        } else {
            $error = "Invalid credentials. Please verify your username and password.";
        }
    }
}

$pageTitle = "Student Login";
require_once __DIR__ . '/includes/header.php';
?>

<div class="form-card">
    <h2 style="text-align: center; margin-bottom: 0.5rem; font-weight: 800;">Student Sign In</h2>
    <p style="text-align: center; color: var(--text-muted); margin-bottom: 1.5rem; font-size: 0.9rem;">
        Access your campus tasks, active assignments, and wallet balance.
    </p>

    <?php if ($error): ?>
        <div class="alert alert-danger"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <form method="POST" action="login.php">
        <div class="form-group">
            <label class="form-label" for="username">Student Username</label>
            <input type="text" id="username" name="username" class="form-control" placeholder="Your username" required autocomplete="username">
        </div>

        <div class="form-group">
            <label class="form-label" for="password">Password</label>
            <input type="password" id="password" name="password" class="form-control" placeholder="••••••••" required autocomplete="current-password">
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">Sign In</button>
    </form>

    <div style="text-align: center; margin-top: 1.5rem; font-size: 0.9rem; color: var(--text-muted);">
        Need an account? <a href="register.php">Sign up & get 100 starter credits</a>
    </div>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
