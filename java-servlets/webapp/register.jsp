<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enlist | Campity Java</title>
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/style.css">
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/themes.css">
</head>
<body>
    <header class="navbar">
        <div class="nav-container">
            <a href="<%= request.getContextPath() %>/index.jsp" class="brand-logo">⚔️ <span>CAMP<span class="highlight">ITY</span></span></a>
            <ul class="nav-links">
                <li><a href="<%= request.getContextPath() %>/auth/login" class="nav-link">Login</a></li>
            </ul>
        </div>
    </header>

    <div class="main-wrapper">
        <div class="form-card">
            <h2 style="font-family: 'Cinzel', serif; text-align: center; margin-bottom: 0.5rem; color: var(--accent-gold);">Enlist in the Guild</h2>
            <p style="text-align: center; color: var(--text-muted); margin-bottom: 1.5rem; font-size: 0.9rem;">Receive 100 free Universal Basic Income (UBI) credits.</p>

            <% if (request.getAttribute("error") != null) { %>
                <div class="alert alert-danger"><%= request.getAttribute("error") %></div>
            <% } %>

            <form method="POST" action="<%= request.getContextPath() %>/auth/register">
                <div class="form-group">
                    <label class="form-label">Guild Username</label>
                    <input type="text" name="username" class="form-control" placeholder="Choose a username" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" name="password" class="form-control" placeholder="••••••••" required>
                </div>
                <button type="submit" class="btn btn-gold" style="width: 100%; margin-top: 1rem;">Create Account (+100 Credits)</button>
            </form>
            <div style="text-align: center; margin-top: 1.5rem; font-size: 0.9rem;">
                <a href="<%= request.getContextPath() %>/auth/login">Already enlisted? Sign in here</a>
            </div>
        </div>
    </div>
</body>
</html>
