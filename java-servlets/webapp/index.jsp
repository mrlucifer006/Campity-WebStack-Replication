<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TaskFlow | Java Servlets Edition</title>
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/style.css">
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/themes.css">
</head>
<body>
    <header class="navbar">
        <div class="nav-container">
            <a href="<%= request.getContextPath() %>/index.jsp" class="brand-logo">
                <div class="brand-icon">✓</div>
                <span>TASK<span class="highlight">FLOW</span> (Java)</span>
            </a>
            <nav>
                <ul class="nav-links">
                    <li><a href="<%= request.getContextPath() %>/index.jsp" class="nav-link active">Overview</a></li>
                    <li><a href="<%= request.getContextPath() %>/auth/login" class="nav-link">Sign In</a></li>
                    <li><a href="<%= request.getContextPath() %>/auth/register" class="btn btn-sm btn-primary">Sign Up (+100 Credits)</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="main-wrapper">
        <div class="hero-section">
            <h1 class="hero-title">Priority-Driven Campus Task Management & Posting Network</h1>
            <p class="hero-subtitle">
                Enterprise Java Servlets implementation with JDBC SQLite and java.util.PriorityQueue scheduling.
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1.5rem;">
                <a href="<%= request.getContextPath() %>/auth/register" class="btn btn-primary">Get Started (+100 Credits)</a>
                <a href="<%= request.getContextPath() %>/auth/login" class="btn btn-outline">Student Sign In</a>
            </div>
        </div>

        <div class="grid-3">
            <div class="card">
                <div class="card-title">⚡ Java Priority Queue Engine</div>
                <p class="quest-desc">Uses <code>java.util.PriorityQueue</code> with custom Comparator for dynamic urgency category weighting and deadline proximity calculation.</p>
            </div>
            <div class="card">
                <div class="card-title">🛡️ Escrow Transaction Protocol</div>
                <p class="quest-desc">ACID transaction handling via JDBC Connection commit/rollback ensuring complete financial ledger safety.</p>
            </div>
            <div class="card">
                <div class="card-title">🌐 Multi-Tier REST API</div>
                <p class="quest-desc">Provides <code>/api/quests/prioritized</code> REST JSON endpoint for seamless PHP frontend integration or mobile clients.</p>
            </div>
        </div>
    </div>

    <footer class="footer">
        <div class="nav-container" style="justify-content: center;">
            <div>TaskFlow Java Servlets Stack — Campus Task Management & Posting System</div>
        </div>
    </footer>
</body>
</html>
