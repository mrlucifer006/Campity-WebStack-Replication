<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="com.campity.model.User, com.campity.model.Transaction, java.util.List" %>
<%
    User user = (User) request.getAttribute("user");
    List<Transaction> transactions = (List<Transaction>) request.getAttribute("transactions");
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profile | TaskFlow Java</title>
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
                <li><a href="<%= request.getContextPath() %>/profile" class="nav-link active">Profile</a></li>
                <li><a href="<%= request.getContextPath() %>/auth/logout" class="btn btn-sm btn-outline">Sign Out</a></li>
            </ul>
        </div>
    </header>

    <div class="main-wrapper">
        <div class="stats-banner">
            <div class="stat-item"><span class="stat-label">Student Username</span><span class="stat-value"><%= user != null ? user.getUsername() : "" %></span></div>
            <div class="stat-item"><span class="stat-label">Proficiency Tier</span><span class="stat-value" style="color:#818cf8;"><%= user != null ? user.getRole() : "" %></span></div>
            <div class="stat-item"><span class="stat-label">Available Balance</span><span class="stat-value primary">💳 <%= String.format("%.1f", user != null ? user.getCredits() : 0.0) %> Cr</span></div>
            <div class="stat-item"><span class="stat-label">Peer Trust Rating</span><span class="stat-value emerald">★ <%= String.format("%.1f", user != null ? user.getReputation() : 5.0) %> / 5.0</span></div>
        </div>

        <div style="margin-top:2rem;">
            <h2 style="font-size:1.4rem; font-weight:700; margin-bottom:1rem;">Credit Transaction & Escrow Ledger</h2>
            <div class="table-wrapper">
                <table class="table">
                    <thead>
                        <tr><th>Timestamp</th><th>Transaction Type</th><th>Associated Task</th><th>Amount</th></tr>
                    </thead>
                    <tbody>
                        <% if (transactions != null && !transactions.isEmpty()) {
                            for (Transaction t : transactions) {
                                boolean isCredit = (t.getReceiverId() != null && user != null && t.getReceiverId() == user.getId());
                                String sign = isCredit ? "+" : "-";
                                String color = isCredit ? "var(--status-open)" : "var(--status-disputed)";
                        %>
                            <tr>
                                <td><%= t.getTimestamp() %></td>
                                <td><span class="badge badge-category"><%= t.getTxType() %></span></td>
                                <td><%= t.getQuestTitle() != null ? t.getQuestTitle() : "<em>Starter Grant</em>" %></td>
                                <td style="font-weight:700; color:<%= color %>; font-family:'JetBrains Mono',monospace;">
                                    <%= sign %><%= String.format("%.1f", t.getAmount()) %> Credits
                                </td>
                            </tr>
                        <%  }
                        } else { %>
                            <tr><td colspan="4" style="text-align:center; padding:1.5rem; color:var(--text-muted);">No transaction records yet.</td></tr>
                        <% } %>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
