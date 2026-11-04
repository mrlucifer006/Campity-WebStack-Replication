<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="com.campity.model.User, java.util.List" %>
<%
    List<User> topUsers = (List<User>) request.getAttribute("topUsers");
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tasker Rankings | TaskFlow Java</title>
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/style.css">
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/themes.css">
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
                <li><a href="<%= request.getContextPath() %>/leaderboard" class="nav-link active">Tasker Rankings</a></li>
                <li><a href="<%= request.getContextPath() %>/auth/logout" class="btn btn-sm btn-outline">Sign Out</a></li>
            </ul>
        </div>
    </header>

    <div class="main-wrapper">
        <div style="margin-bottom:2rem; text-align:center;">
            <h1 class="hero-title" style="font-size:2.2rem;">Campus Tasker Rankings</h1>
            <p style="color:var(--text-muted);">Ranked by Contribution Points (XP), Peer Rating, and Verified Deliveries.</p>
        </div>

        <div class="table-wrapper">
            <table class="table">
                <thead>
                    <tr><th>Rank</th><th>Student Tasker</th><th>Proficiency Tier</th><th>Trust Rating</th><th>Contribution XP</th></tr>
                </thead>
                <tbody>
                    <% if (topUsers != null) {
                        int rank = 1;
                        for (User u : topUsers) {
                            String medal = rank == 1 ? "🥇" : (rank == 2 ? "🥈" : (rank == 3 ? "🥉" : "#" + rank));
                    %>
                        <tr>
                            <td style="font-weight:800; font-size:1.1rem;"><%= medal %></td>
                            <td><strong><%= u.getUsername() %></strong></td>
                            <td><span class="badge badge-category"><%= u.getRole() %></span></td>
                            <td>★ <%= String.format("%.1f", u.getReputation()) %></td>
                            <td style="font-weight:700; color:#818cf8; font-family:'JetBrains Mono',monospace;"><%= u.getXp() %> XP</td>
                        </tr>
                    <%      rank++;
                        }
                    } %>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
