<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="com.campity.model.User, com.campity.model.Quest, java.util.List" %>
<%
    User user = (User) session.getAttribute("user");
    List<Quest> availableQuests = (List<Quest>) request.getAttribute("availableQuests");
    List<Quest> activeMissions = (List<Quest>) request.getAttribute("activeMissions");
    List<Quest> postedQuests = (List<Quest>) request.getAttribute("postedQuests");
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Feed | TaskFlow Java</title>
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
                <li><a href="<%= request.getContextPath() %>/dashboard" class="nav-link active">Task Feed</a></li>
                <li><a href="<%= request.getContextPath() %>/quest/post" class="nav-link">+ Post Task</a></li>
                <li><a href="<%= request.getContextPath() %>/leaderboard" class="nav-link">Rankings</a></li>
                <li>
                    <div class="user-badge-nav">
                        <span class="currency-badge">💳 <%= String.format("%.1f", user != null ? user.getCredits() : 0.0) %> Cr</span>
                        <a href="<%= request.getContextPath() %>/profile" class="nav-link" style="padding:0;"><%= user != null ? user.getUsername() : "" %></a>
                    </div>
                </li>
                <li><a href="<%= request.getContextPath() %>/auth/logout" class="btn btn-sm btn-outline">Sign Out</a></li>
            </ul>
        </div>
    </header>

    <div class="main-wrapper">
        <% if (session.getAttribute("flashMessage") != null) { %>
            <div class="alert alert-<%= session.getAttribute("flashType") %>">
                <%= session.getAttribute("flashMessage") %>
            </div>
            <% session.removeAttribute("flashMessage"); session.removeAttribute("flashType"); %>
        <% } %>

        <div class="stats-banner">
            <div class="stat-item"><span class="stat-label">Wallet Balance</span><span class="stat-value primary">💳 <%= String.format("%.1f", user != null ? user.getCredits() : 0.0) %> Cr</span></div>
            <div class="stat-item"><span class="stat-label">Contribution XP</span><span class="stat-value teal">⭐ <%= user != null ? user.getXp() : 0 %> XP</span></div>
            <div class="stat-item"><span class="stat-label">Trust Rating</span><span class="stat-value emerald">★ <%= String.format("%.1f", user != null ? user.getReputation() : 5.0) %> / 5.0</span></div>
            <div class="stat-item"><span class="stat-label">Tasker Level</span><span class="stat-value" style="font-size:1.15rem; color:#818cf8;"><%= user != null ? user.getRole() : "" %></span></div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem;">
            <div>
                <h2 style="font-size:1.65rem; font-weight:800;">Priority Task Feed</h2>
                <p style="color:var(--text-muted); font-size:0.9rem;">Tasks sorted dynamically via Java PriorityQueue (Max-Heap).</p>
            </div>
            <div style="display:flex; gap:0.75rem;">
                <a href="<%= request.getContextPath() %>/quest/seed" class="btn btn-sm btn-outline">🎲 Load Sample Tasks</a>
                <a href="<%= request.getContextPath() %>/quest/post" class="btn btn-sm btn-primary">+ Post Task</a>
            </div>
        </div>

        <!-- Available Tasks -->
        <div class="grid-3" style="margin-bottom:2.5rem;">
            <% if (availableQuests != null && !availableQuests.isEmpty()) {
                for (Quest q : availableQuests) {
                    double stake = Math.max(10, Math.floor(q.getReward() * 0.10));
            %>
                <div class="quest-card priority-<%= q.getUrgencyTier() %>">
                    <div>
                        <div class="quest-header">
                            <span class="badge badge-priority">Score: <%= Math.round(q.getPriorityScore()) %></span>
                            <span class="badge badge-category"><%= q.getCategory() %></span>
                        </div>
                        <h3 class="quest-title"><%= q.getTitle() %></h3>
                        <p class="quest-desc"><%= q.getDescription() %></p>
                        <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:0.75rem;">
                            Posted by <strong><%= q.getPosterName() %></strong> (★ <%= String.format("%.1f", q.getPosterReputation()) %>)
                        </div>
                    </div>
                    <div class="quest-footer">
                        <div>
                            <div class="reward-tag">💳 <%= String.format("%.1f", q.getReward()) %> Cr</div>
                            <span style="font-size:0.725rem; color:var(--text-muted);">Required Stake: <%= (int)stake %> Cr</span>
                        </div>
                        <form method="POST" action="<%= request.getContextPath() %>/quest/accept">
                            <input type="hidden" name="quest_id" value="<%= q.getId() %>">
                            <button type="submit" class="btn btn-sm btn-primary">Accept Task</button>
                        </form>
                    </div>
                </div>
            <%  }
               } else { %>
                <div class="card" style="grid-column: 1 / -1; text-align:center; padding:2rem;">
                    No open campus tasks available right now. <a href="<%= request.getContextPath() %>/quest/seed">Click here to load sample tasks</a>.
                </div>
            <% } %>
        </div>
    </div>
</body>
</html>
