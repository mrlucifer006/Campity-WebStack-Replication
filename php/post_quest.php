<?php
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/includes/auth.php';

require_login();
$currentUser = current_user($pdo);

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = trim($_POST['title'] ?? '');
    $description = trim($_POST['description'] ?? '');
    $category = $_POST['category'] ?? 'Labor';
    $reward = (float)($_POST['reward'] ?? 0);
    $deadline = !empty($_POST['deadline']) ? $_POST['deadline'] : null;

    if (empty($title) || empty($description) || $reward <= 0) {
        $error = "Please provide a valid title, description, and reward amount.";
    } elseif ($currentUser['credits'] < $reward) {
        $error = "Insufficient credits. Required: " . number_format($reward, 1) . " Credits, Available: " . number_format($currentUser['credits'], 1) . " Credits.";
    } else {
        // Handle file attachment
        $filePath = null;
        if (isset($_FILES['attachment']) && $_FILES['attachment']['error'] === UPLOAD_ERR_OK) {
            $uploadDir = __DIR__ . '/uploads/';
            if (!is_dir($uploadDir)) {
                mkdir($uploadDir, 0777, true);
            }
            $origName = basename($_FILES['attachment']['name']);
            $safeName = time() . '_' . preg_replace('/[^a-zA-Z0-9_\.-]/', '_', $origName);
            $targetPath = $uploadDir . $safeName;
            if (move_uploaded_file($_FILES['attachment']['tmp_name'], $targetPath)) {
                $filePath = 'uploads/' . $safeName;
            }
        }

        // Deduct Escrow from user balance
        $pdo->beginTransaction();
        try {
            $deduct = $pdo->prepare("UPDATE users SET credits = credits - ? WHERE id = ?");
            $deduct->execute([$reward, $currentUser['id']]);

            // Insert Task
            $stmt = $pdo->prepare("
                INSERT INTO quests (title, description, category, reward, poster_id, status, escrow_status, deadline, file_path) 
                VALUES (?, ?, ?, ?, ?, 'OPEN', 'HELD', ?, ?)
            ");
            $stmt->execute([$title, $description, $category, $reward, $currentUser['id'], $deadline, $filePath]);
            $taskId = $pdo->lastInsertId();

            // Insert Escrow Transaction Log
            $tx = $pdo->prepare("INSERT INTO transactions (sender_id, amount, tx_type, quest_id) VALUES (?, ?, 'ESCROW_DEPOSIT', ?)");
            $tx->execute([$currentUser['id'], $reward, $taskId]);

            $pdo->commit();

            set_flash("Task '$title' successfully published! $reward credits placed in secure escrow.", "success");
            header('Location: dashboard.php');
            exit;
        } catch (Exception $e) {
            $pdo->rollBack();
            $error = "Failed to publish task: " . $e->getMessage();
        }
    }
}

$pageTitle = "Post New Campus Task";
require_once __DIR__ . '/includes/header.php';
?>

<div class="form-card">
    <h2 style="text-align: center; margin-bottom: 0.5rem; font-weight: 800;">Post a Campus Task</h2>
    <p style="text-align: center; color: var(--text-muted); margin-bottom: 1.5rem; font-size: 0.9rem;">
        Available Wallet Balance: <strong class="currency-badge">💳 <?= number_format($currentUser['credits'], 1) ?> Credits</strong>
    </p>

    <?php if ($error): ?>
        <div class="alert alert-danger"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <form method="POST" action="post_quest.php" enctype="multipart/form-data">
        <div class="form-group">
            <label class="form-label" for="title">Task Title</label>
            <input type="text" id="title" name="title" class="form-control" placeholder="e.g. Return Library Research Books & Clear Desk" required>
        </div>

        <div class="form-group">
            <label class="form-label" for="category">Task Category (Determines Priority Weight)</label>
            <select id="category" name="category" class="form-control" required>
                <option value="Urgent">🚨 Urgent / Time-Sensitive (Priority Weight: 90)</option>
                <option value="Medical">💊 Medical / Health (Priority Weight: 100)</option>
                <option value="Tech Support">💻 Tech & Hardware Support (Priority Weight: 70)</option>
                <option value="Academics">📚 Academics & Notes Sharing (Priority Weight: 60)</option>
                <option value="Logistics">📦 Campus Logistics & Delivery (Priority Weight: 50)</option>
                <option value="Labor" selected>🛠️ General Assistance & Labor (Priority Weight: 40)</option>
            </select>
        </div>

        <div class="form-group">
            <label class="form-label" for="reward">Task Reward Budget (Credits)</label>
            <input type="number" id="reward" name="reward" class="form-control" min="1" step="0.5" placeholder="e.g. 50" required>
            <small id="stake-preview" style="color: var(--accent-teal); display: block; margin-top: 0.35rem; font-size: 0.8rem;">
                Helper Stake Requirement: 10 Credits (10% lock refunded upon verified delivery)
            </small>
        </div>

        <div class="form-group">
            <label class="form-label" for="deadline">Target Completion Deadline</label>
            <input type="datetime-local" id="deadline" name="deadline" class="form-control">
        </div>

        <div class="form-group">
            <label class="form-label" for="description">Task Instructions & Deliverables</label>
            <textarea id="description" name="description" class="form-control" rows="4" placeholder="Detail the exact requirements, location, instructions, and handover expectations..." required></textarea>
        </div>

        <div class="form-group">
            <label class="form-label" for="attachment">Deliverable / Reference Document (Optional)</label>
            <input type="file" id="attachment" name="attachment" class="form-control">
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">Escrow Credits & Publish Task</button>
    </form>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
