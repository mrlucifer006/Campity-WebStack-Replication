<?php
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/includes/auth.php';

require_login();
$currentUser = current_user($pdo);

$sampleTasks = [
    [
        'title' => 'Emergency Prescription Pickup from Campus Infirmary',
        'description' => 'Urgent pickup of prescribed medication from Main Gate Health Center and delivery to West Residence Hall 3B.',
        'category' => 'Medical',
        'reward' => 120.0,
        'deadline' => date('Y-m-d H:i:s', strtotime('+3 hours'))
    ],
    [
        'title' => 'Return 4 Library Research Books to Reserve Desk',
        'description' => 'Drop off borrowed IEEE engineering reference volumes at Central Library before 5 PM to avoid late fines.',
        'category' => 'Logistics',
        'reward' => 45.0,
        'deadline' => date('Y-m-d H:i:s', strtotime('+1 day'))
    ],
    [
        'title' => 'Lecture Hall 204 HDMI Projector Calibration & Audio Check',
        'description' => 'HDMI video output is flickering during faculty slides. Need someone to test cable sync and audio jack before 2 PM seminar.',
        'category' => 'Tech Support',
        'reward' => 80.0,
        'deadline' => date('Y-m-d H:i:s', strtotime('+5 hours'))
    ],
    [
        'title' => 'Data Structures AVL & B-Tree Exam Review Notes',
        'description' => 'Need clean, handwritten notes and annotated diagram summaries covering AVL tree rotations and B-Tree insertions.',
        'category' => 'Academics',
        'reward' => 95.0,
        'deadline' => date('Y-m-d H:i:s', strtotime('+12 hours'))
    ],
    [
        'title' => 'Assemble Student Robotics Club Display Booth',
        'description' => 'Assist in carrying tables, mounting registration banners, and running extension cords at the Student Union Hall.',
        'category' => 'Labor',
        'reward' => 50.0,
        'deadline' => date('Y-m-d H:i:s', strtotime('+2 days'))
    ]
];

// Determine poster ID (admin or user #1 or current user)
$adminId = $pdo->query("SELECT id FROM users ORDER BY id ASC LIMIT 1")->fetchColumn();
if (!$adminId) {
    $adminId = $currentUser['id'];
}

$stmt = $pdo->prepare("
    INSERT INTO quests (title, description, category, reward, poster_id, status, escrow_status, deadline) 
    VALUES (?, ?, ?, ?, ?, 'OPEN', 'HELD', ?)
");

$seededCount = 0;
foreach ($sampleTasks as $task) {
    $stmt->execute([
        $task['title'],
        $task['description'],
        $task['category'],
        $task['reward'],
        $adminId,
        $task['deadline']
    ]);
    $seededCount++;
}

set_flash("Sample campus tasks loaded! $seededCount realistic tasks populated across categories.", "success");
header('Location: dashboard.php');
exit;
