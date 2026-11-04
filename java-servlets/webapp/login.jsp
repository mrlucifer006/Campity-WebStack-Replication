<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login | Campity Java</title>
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/style.css">
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/css/themes.css">
</head>
<body>
    <header class="navbar">
        <div class="nav-container">
            <a href="<%= request.getContextPath() %>/index.jsp" class="brand-logo">⚔️ <span>CAMP<span class="highlight">ITY</span></span></a>
            <ul class="nav-links">
                <li><a href="<%= request.getContextPath() %>/index.jsp" class="nav-link">Home</a></li>
                <li><a href="<%= request.getContextPath() %>/auth/register" class="btn btn-sm btn-gold">Sign Up</a></li>
            </ul>
        </div>
    </header>

    <div class="main-wrapper">
        <div class="form-card">
            <h2 style="font-family: 'Cinzel', serif; text-align: center; margin-bottom: 0.5rem; color: var(--accent-gold);">Adventurer Login</h2>
            <p style="text-align: center; color: var(--text-muted); margin-bottom: 1.5rem; font-size: 0.9rem;">Sign in to access your missions and campus feed.</p>

            <% if (request.getAttribute("error") != null) { %>
                <div class="alert alert-danger"><%= request.getAttribute("error") %></div>
            <% } %>

            <form method="POST" action="<%= request.getContextPath() %>/auth/login">
                <div class="form-group">
                    <label class="form-label">Guild Username</label>
                    <input type="text" name="username" class="form-control" placeholder="Your username" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" name="password" class="form-control" placeholder="••••••••" required>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">Enter Campity</button>
            </form>
            <div style="text-align: center; margin-top: 1.5rem; font-size: 0.9rem;">
                <a href="<%= request.getContextPath() %>/auth/register">New adventurer? Enlist (+100 UBI)</a>
            </div>
        </div>
    </div>
</body>
</html>
