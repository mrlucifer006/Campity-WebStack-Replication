<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="com.campity.model.User" %>
<%
    User user = (User) session.getAttribute("user");
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Post Task | TaskFlow Java</title>
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/style.css">
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/themes.css">
    <script src="<%= request.getContextPath() %>/assets/js/app.js" defer></script>
</head>
<body>
    <header class="navbar">
        <div class="nav-container">
            <a href="<%= request.getContextPath() %>/dashboard" class="brand-logo">
                <div class="brand-icon">✓</div>
                <span>TASK<span class="highlight">FLOW</span></span>
            </a>
            <ul class="nav-links">
                <li><a href="<%= request.getContextPath() %>/dashboard" class="nav-link">Task Feed</a></li>
                <li><a href="<%= request.getContextPath() %>/auth/logout" class="btn btn-sm btn-outline">Sign Out</a></li>
            </ul>
        </div>
    </header>

    <div class="main-wrapper">
        <div class="form-card">
            <h2 style="text-align:center; margin-bottom:0.5rem; font-weight:800;">Post a Campus Task</h2>
            <p style="text-align:center; color:var(--text-muted); margin-bottom:1.5rem;">
                Available Wallet Balance: <span class="currency-badge">💳 <%= String.format("%.1f", user != null ? user.getCredits() : 0.0) %> Credits</span>
            </p>

            <% if (request.getAttribute("error") != null) { %>
                <div class="alert alert-danger"><%= request.getAttribute("error") %></div>
            <% } %>

            <form method="POST" action="<%= request.getContextPath() %>/quest/post" enctype="multipart/form-data">
                <div class="form-group">
                    <label class="form-label">Task Title</label>
                    <input type="text" name="title" class="form-control" required placeholder="e.g. Return Library Research Books">
                </div>
                <div class="form-group">
                    <label class="form-label">Category</label>
                    <select name="category" class="form-control">
                        <option value="Urgent">🚨 Urgent / Time-Sensitive (Weight 90)</option>
                        <option value="Medical">💊 Medical / Health (Weight 100)</option>
                        <option value="Tech Support">💻 Tech & Hardware Support (Weight 70)</option>
                        <option value="Academics">📚 Academics & Notes (Weight 60)</option>
                        <option value="Logistics">📦 Logistics & Delivery (Weight 50)</option>
                        <option value="Labor" selected>🛠️ General Assistance (Weight 40)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Reward Budget (Credits Held in Escrow)</label>
                    <input type="number" id="reward" name="reward" class="form-control" min="1" step="0.5" value="25" required>
                    <small id="stake-preview" style="color:var(--accent-teal); display:block; margin-top:0.35rem;">Helper Stake: 10 Credits (10% lock refunded on delivery)</small>
                </div>
                <div class="form-group">
                    <label class="form-label">Completion Deadline</label>
                    <input type="datetime-local" name="deadline" class="form-control">
                </div>
                <div class="form-group">
                    <label class="form-label">Task Instructions & Deliverables</label>
                    <textarea name="description" class="form-control" rows="4" required></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">Reference File / Document (Optional)</label>
                    <input type="file" name="attachment" class="form-control">
                </div>
                <button type="submit" class="btn btn-primary" style="width:100%; margin-top:1rem;">Publish Task & Escrow Credits</button>
            </form>
        </div>
    </div>
</body>
</html>
