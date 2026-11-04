<?php
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/includes/auth.php';

require_login();

$questId = (int)($_GET['quest_id'] ?? 0);
if ($questId <= 0) {
    die("Invalid request");
}

$stmt = $pdo->prepare("SELECT file_path, title FROM quests WHERE id = ?");
$stmt->execute([$questId]);
$quest = $stmt->fetch();

if (!$quest || empty($quest['file_path'])) {
    die("File not found for this bounty.");
}

$realFile = __DIR__ . '/' . $quest['file_path'];
if (!file_exists($realFile)) {
    die("Attachment file missing on server.");
}

header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename="' . basename($realFile) . '"');
header('Expires: 0');
header('Cache-Control: must-revalidate');
header('Pragma: public');
header('Content-Length: ' . filesize($realFile));
readfile($realFile);
exit;
