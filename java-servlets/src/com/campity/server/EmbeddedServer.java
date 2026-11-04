package com.campity.server;

import com.campity.algorithm.TaskPriorityQueue;
import com.campity.dao.DBUtil;
import com.campity.dao.QuestDAO;
import com.campity.dao.TransactionDAO;
import com.campity.dao.UserDAO;
import com.campity.model.Quest;
import com.campity.model.Transaction;
import com.campity.model.User;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.sql.Timestamp;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Standalone Embedded Server for TaskFlow Java Backend
 * Serves the Task Management & Posting System on standard JDK HttpServer.
 */
public class EmbeddedServer {

    private static final int PORT = 8080;
    private static final Map<String, Integer> SESSIONS = new ConcurrentHashMap<>();
    private static final UserDAO userDAO = new UserDAO();
    private static final QuestDAO questDAO = new QuestDAO();
    private static final TransactionDAO transactionDAO = new TransactionDAO();

    public static void main(String[] args) throws Exception {
        System.out.println("===============================================================");
        System.out.println("  TaskFlow: Campus Task Management & Posting Java Server      ");
        System.out.println("===============================================================");

        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);

        // Static assets handler
        server.createContext("/assets", new StaticHandler());

        // Core Application Routes
        server.createContext("/", new RootHandler());
        server.createContext("/auth/login", new LoginHandler());
        server.createContext("/auth/register", new RegisterHandler());
        server.createContext("/auth/logout", new LogoutHandler());
        server.createContext("/dashboard", new DashboardHandler());
        server.createContext("/quest/post", new PostTaskHandler());
        server.createContext("/quest/accept", new AcceptTaskHandler());
        server.createContext("/quest/complete", new CompleteTaskHandler());
        server.createContext("/quest/verify", new VerifyTaskHandler());
        server.createContext("/quest/seed", new SeedTaskHandler());
        server.createContext("/leaderboard", new LeaderboardHandler());
        server.createContext("/profile", new ProfileHandler());
        server.createContext("/api/quests/prioritized", new ApiPrioritizedHandler());

        server.setExecutor(null);
        server.start();

        System.out.println("✅ TaskFlow Java Server active and listening on port " + PORT);
        System.out.println("👉 Web Portal: http://localhost:" + PORT);
        System.out.println("👉 Priority Queue API: http://localhost:" + PORT + "/api/quests/prioritized");
    }

    private static User getSessionUser(HttpExchange exchange) {
        String cookieHeader = exchange.getRequestHeaders().getFirst("Cookie");
        if (cookieHeader != null) {
            for (String cookie : cookieHeader.split(";")) {
                String[] pair = cookie.trim().split("=");
                if (pair.length == 2 && "TASKFLOW_SID".equals(pair[0])) {
                    Integer userId = SESSIONS.get(pair[1]);
                    if (userId != null) {
                        return userDAO.findById(userId);
                    }
                }
            }
        }
        return null;
    }

    private static void setSessionCookie(HttpExchange exchange, int userId) {
        String sid = UUID.randomUUID().toString();
        SESSIONS.put(sid, userId);
        exchange.getResponseHeaders().set("Set-Cookie", "TASKFLOW_SID=" + sid + "; Path=/; HttpOnly");
    }

    private static void clearSessionCookie(HttpExchange exchange) {
        String cookieHeader = exchange.getRequestHeaders().getFirst("Cookie");
        if (cookieHeader != null) {
            for (String cookie : cookieHeader.split(";")) {
                String[] pair = cookie.trim().split("=");
                if (pair.length == 2 && "TASKFLOW_SID".equals(pair[0])) {
                    SESSIONS.remove(pair[1]);
                }
            }
        }
        exchange.getResponseHeaders().set("Set-Cookie", "TASKFLOW_SID=; Path=/; Max-Age=0");
    }

    private static Map<String, String> parseFormData(HttpExchange exchange) throws IOException {
        InputStream is = exchange.getRequestBody();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        int len;
        while ((len = is.read(buffer)) != -1) {
            baos.write(buffer, 0, len);
        }
        String body = baos.toString(StandardCharsets.UTF_8);
        Map<String, String> map = new HashMap<>();
        if (!body.isEmpty()) {
            for (String param : body.split("&")) {
                String[] pair = param.split("=");
                if (pair.length == 2) {
                    map.put(URLDecoder.decode(pair[0], "UTF-8"), URLDecoder.decode(pair[1], "UTF-8"));
                } else if (pair.length == 1) {
                    map.put(URLDecoder.decode(pair[0], "UTF-8"), "");
                }
            }
        }
        return map;
    }

    private static void sendHtml(HttpExchange exchange, int status, String html) throws IOException {
        byte[] bytes = html.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }

    private static void sendRedirect(HttpExchange exchange, String location) throws IOException {
        exchange.getResponseHeaders().set("Location", location);
        exchange.sendResponseHeaders(302, -1);
    }

    // --- HTML Layout Helper ---
    private static String renderHeader(String title, User user) {
        StringBuilder sb = new StringBuilder();
        sb.append("<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>");
        sb.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>");
        sb.append("<title>").append(title).append(" | TaskFlow Java</title>");
        sb.append("<link rel='stylesheet' href='/assets/css/style.css'>");
        sb.append("<link rel='stylesheet' href='/assets/css/themes.css'>");
        sb.append("<script src='/assets/js/app.js' defer></script></head><body>");
        sb.append("<header class='navbar'><div class='nav-container'>");
        sb.append("<a href='/' class='brand-logo'><div class='brand-icon'>✓</div><span>TASK<span class='highlight'>FLOW</span> (Java)</span></a><nav><ul class='nav-links'>");
        if (user != null) {
            sb.append("<li><a href='/dashboard' class='nav-link'>Task Feed</a></li>");
            sb.append("<li><a href='/quest/post' class='nav-link'>+ Post Task</a></li>");
            sb.append("<li><a href='/leaderboard' class='nav-link'>Tasker Rankings</a></li>");
            sb.append("<li><div class='user-badge-nav'><span class='currency-badge'>💳 ").append(String.format("%.1f", user.getCredits())).append(" Cr</span>");
            sb.append("<a href='/profile' class='nav-link' style='padding:0;'>").append(user.getUsername()).append("</a></div></li>");
            sb.append("<li><a href='/auth/logout' class='btn btn-sm btn-outline'>Sign Out</a></li>");
        } else {
            sb.append("<li><a href='/' class='nav-link'>Overview</a></li>");
            sb.append("<li><a href='/auth/login' class='nav-link'>Log In</a></li>");
            sb.append("<li><a href='/auth/register' class='btn btn-sm btn-primary'>Sign Up (+100 Credits)</a></li>");
        }
        sb.append("</ul></nav></div></header><div class='main-wrapper'>");
        return sb.toString();
    }

    private static String renderFooter() {
        return "</div><footer class='footer'><div class='nav-container' style='justify-content: space-between; flex-wrap: wrap; gap: 1rem;'>" +
               "<div><strong>TaskFlow Java Servlets Stack</strong> — Priority-Driven Campus Task Management System.</div>" +
               "<div><span>Interface Theme: </span><select onchange='switchTheme(this.value)' class='form-control' style='width: auto; display: inline-block; padding: 0.25rem 0.65rem; font-size: 0.85rem;'>" +
               "<option value='default'>Dark Modern (Default)</option>" +
               "<option value='light'>Clean Light SaaS</option>" +
               "<option value='slate'>Minimalist Slate</option>" +
               "<option value='emerald'>Productivity Emerald</option></select></div></div></footer></body></html>";
    }

    // --- Route Handlers ---

    static class StaticHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String path = exchange.getRequestURI().getPath();
            File file = new File("assets" + path.replace("/assets", ""));
            if (!file.exists()) {
                file = new File("../assets" + path.replace("/assets", ""));
            }
            if (!file.exists()) {
                file = new File("Campity-WebStack-Replication/assets" + path.replace("/assets", ""));
            }

            if (file.exists() && !file.isDirectory()) {
                String mime = "text/plain";
                if (path.endsWith(".css")) mime = "text/css";
                else if (path.endsWith(".js")) mime = "application/javascript";
                else if (path.endsWith(".png")) mime = "image/png";

                byte[] data = Files.readAllBytes(file.toPath());
                exchange.getResponseHeaders().set("Content-Type", mime);
                exchange.sendResponseHeaders(200, data.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(data);
                }
            } else {
                exchange.sendResponseHeaders(404, -1);
            }
        }
    }

    static class RootHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            User user = getSessionUser(exchange);
            StringBuilder html = new StringBuilder(renderHeader("Overview", user));
            html.append("<div class='hero-section'>");
            html.append("<h1 class='hero-title'>Campus Task Management & Posting Network</h1>");
            html.append("<p class='hero-subtitle'>Pure Java Servlets & Priority Queue Implementation. Efficiently post, prioritize, and delegate campus errands with escrow accountability and peer ratings.</p>");
            html.append("<div style='display:flex; gap:1rem; justify-content:center; margin-top:1.5rem;'>");
            if (user != null) {
                html.append("<a href='/dashboard' class='btn btn-primary'>Go to Task Feed</a>");
                html.append("<a href='/quest/post' class='btn btn-outline'>+ Post a Task</a>");
            } else {
                html.append("<a href='/auth/register' class='btn btn-primary'>Register Student Account (+100 Credits)</a>");
                html.append("<a href='/auth/login' class='btn btn-outline'>Student Sign In</a>");
            }
            html.append("</div></div>");

            html.append("<div class='grid-3'>");
            html.append("<div class='card'><div class='card-title'>⚡ Priority Heap Engine</div><p class='quest-desc'>Tasks dynamically prioritized via java.util.PriorityQueue using category urgency weighting and deadline factors.</p></div>");
            html.append("<div class='card'><div class='card-title'>🛡️ Escrow & 10% Stake</div><p class='quest-desc'>Requesters deposit reward in escrow. Helpers lock a 10% stake to prevent task abandonment.</p></div>");
            html.append("<div class='card'><div class='card-title'>📈 Proficiency Tiers</div><p class='quest-desc'>Earn XP and peer star ratings. Advance from Junior Tasker to Associate Tasker, Senior Tasker, and Lead Coordinator!</p></div>");
            html.append("</div>");

            html.append(renderFooter());
            sendHtml(exchange, 200, html.toString());
        }
    }

    static class LoginHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                Map<String, String> data = parseFormData(exchange);
                User u = userDAO.authenticate(data.get("username"), data.get("password"));
                if (u != null) {
                    setSessionCookie(exchange, u.getId());
                    sendRedirect(exchange, "/dashboard");
                    return;
                }
            }

            StringBuilder html = new StringBuilder(renderHeader("Login", null));
            html.append("<div class='form-card'>");
            html.append("<h2 style='text-align:center; margin-bottom:0.5rem; font-weight:800;'>Student Sign In</h2>");
            html.append("<p style='text-align:center; color:var(--text-muted); margin-bottom:1.5rem;'>Sign in to access your assigned tasks and campus feed.</p>");
            html.append("<form method='POST' action='/auth/login'>");
            html.append("<div class='form-group'><label class='form-label'>Student Username</label><input type='text' name='username' class='form-control' required></div>");
            html.append("<div class='form-group'><label class='form-label'>Password</label><input type='password' name='password' class='form-control' required></div>");
            html.append("<button type='submit' class='btn btn-primary' style='width:100%; margin-top:1rem;'>Sign In</button>");
            html.append("</form><div style='text-align:center; margin-top:1.5rem;'><a href='/auth/register'>Need an account? Sign up (+100 Credits)</a></div></div>");
            html.append(renderFooter());
            sendHtml(exchange, 200, html.toString());
        }
    }

    static class RegisterHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                Map<String, String> data = parseFormData(exchange);
                boolean ok = userDAO.register(data.get("username"), data.get("password"));
                if (ok) {
                    sendRedirect(exchange, "/auth/login");
                    return;
                }
            }

            StringBuilder html = new StringBuilder(renderHeader("Sign Up", null));
            html.append("<div class='form-card'>");
            html.append("<h2 style='text-align:center; margin-bottom:0.5rem; font-weight:800;'>Create Student Account</h2>");
            html.append("<p style='text-align:center; color:var(--text-muted); margin-bottom:1.5rem;'>Register and receive 100 free credits to post or accept tasks.</p>");
            html.append("<form method='POST' action='/auth/register'>");
            html.append("<div class='form-group'><label class='form-label'>Student Username</label><input type='text' name='username' class='form-control' required></div>");
            html.append("<div class='form-group'><label class='form-label'>Password</label><input type='password' name='password' class='form-control' required></div>");
            html.append("<button type='submit' class='btn btn-primary' style='width:100%; margin-top:1rem;'>Register (+100 Credits)</button>");
            html.append("</form><div style='text-align:center; margin-top:1.5rem;'><a href='/auth/login'>Already registered? Sign in</a></div></div>");
            html.append(renderFooter());
            sendHtml(exchange, 200, html.toString());
        }
    }

    static class LogoutHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            clearSessionCookie(exchange);
            sendRedirect(exchange, "/");
        }
    }

    static class DashboardHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            User user = getSessionUser(exchange);
            if (user == null) {
                sendRedirect(exchange, "/auth/login");
                return;
            }

            List<Quest> rawOpen = questDAO.getOpenQuests(user.getId());
            List<Quest> prioritized = TaskPriorityQueue.prioritize(rawOpen);
            List<Quest> missions = questDAO.getMissionsForSolver(user.getId());
            List<Quest> posted = questDAO.getQuestsByPoster(user.getId());

            StringBuilder html = new StringBuilder(renderHeader("Task Feed", user));

            // Stats Banner
            html.append("<div class='stats-banner'>");
            html.append("<div class='stat-item'><span class='stat-label'>Wallet Balance</span><span class='stat-value primary'>💳 ").append(String.format("%.1f", user.getCredits())).append(" Cr</span></div>");
            html.append("<div class='stat-item'><span class='stat-label'>Contribution XP</span><span class='stat-value teal'>⭐ ").append(user.getXp()).append(" XP</span></div>");
            html.append("<div class='stat-item'><span class='stat-label'>Peer Trust Rating</span><span class='stat-value emerald'>★ ").append(String.format("%.1f", user.getReputation())).append(" / 5.0</span></div>");
            html.append("<div class='stat-item'><span class='stat-label'>Tasker Level</span><span class='stat-value' style='font-size:1.15rem; color:#818cf8;'>").append(user.getRole()).append("</span></div>");
            html.append("</div>");

            html.append("<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem;'>");
            html.append("<div><h2 style='font-size:1.65rem; font-weight:800;'>Priority Task Feed</h2>");
            html.append("<p style='color:var(--text-muted); font-size:0.9rem;'>Dynamically prioritized by java.util.PriorityQueue Max-Heap engine.</p></div>");
            html.append("<div style='display:flex; gap:0.75rem;'><a href='/quest/seed' class='btn btn-sm btn-outline'>🎲 Load Sample Tasks</a><a href='/quest/post' class='btn btn-sm btn-primary'>+ Post Task</a></div></div>");

            // Open Tasks
            if (prioritized.isEmpty()) {
                html.append("<div class='card' style='text-align:center; padding:3rem 1rem; margin-bottom:2rem;'>");
                html.append("<p style='color:var(--text-muted); font-size:1.1rem; margin-bottom:1rem;'>No open campus tasks available right now.</p>");
                html.append("<a href='/quest/seed' class='btn btn-sm btn-primary'>Load Sample Tasks</a></div>");
            } else {
                html.append("<div class='grid-3' style='margin-bottom:2.5rem;'>");
                for (Quest q : prioritized) {
                    double stake = Math.max(10, Math.floor(q.getReward() * 0.10));
                    html.append("<div class='quest-card priority-").append(q.getUrgencyTier()).append("'><div>");
                    html.append("<div class='quest-header'><span class='badge badge-priority'>Score: ").append(Math.round(q.getPriorityScore())).append("</span>");
                    html.append("<span class='badge badge-category'>").append(q.getCategory()).append("</span></div>");
                    html.append("<h3 class='quest-title'>").append(q.getTitle()).append("</h3>");
                    html.append("<p class='quest-desc'>").append(q.getDescription()).append("</p>");
                    html.append("<div style='font-size:0.8rem; color:var(--text-muted); margin-bottom:0.75rem;'>Posted by <strong>").append(q.getPosterName()).append("</strong> (★ ").append(String.format("%.1f", q.getPosterReputation())).append(")</div></div>");
                    html.append("<div class='quest-footer'><div><div class='reward-tag'>💳 ").append(String.format("%.1f", q.getReward())).append(" Cr</div>");
                    html.append("<span style='font-size:0.725rem; color:var(--text-muted);'>Stake Lock: ").append((int)stake).append(" Cr</span></div>");
                    html.append("<form method='POST' action='/quest/accept'><input type='hidden' name='quest_id' value='").append(q.getId()).append("'>");
                    html.append("<button type='submit' class='btn btn-sm btn-primary'>Accept Task</button></form></div></div>");
                }
                html.append("</div>");
            }

            // My Assigned Tasks
            html.append("<div style='margin-bottom:2.5rem;'><h2 style='font-size:1.4rem; font-weight:700; margin-bottom:1rem;'>My Assigned Tasks (Helper Role)</h2>");
            if (missions.isEmpty()) {
                html.append("<div class='card' style='padding:1.5rem; color:var(--text-muted);'>You have not accepted any tasks yet. Browse the feed above!</div>");
            } else {
                html.append("<div class='table-wrapper'><table class='table'><thead><tr><th>Task Title</th><th>Category</th><th>Requester</th><th>Reward</th><th>Status</th><th>Action</th></tr></thead><tbody>");
                for (Quest m : missions) {
                    html.append("<tr><td><strong>").append(m.getTitle()).append("</strong></td>");
                    html.append("<td><span class='badge badge-category'>").append(m.getCategory()).append("</span></td>");
                    html.append("<td>").append(m.getPosterName()).append("</td>");
                    html.append("<td><span class='currency-badge'>💳 ").append(String.format("%.1f", m.getReward())).append("</span></td>");
                    html.append("<td><span class='badge badge-").append(m.getStatus().toLowerCase()).append("'>").append(m.getStatus()).append("</span></td>");
                    html.append("<td>");
                    if ("ACCEPTED".equals(m.getStatus())) {
                        html.append("<form method='POST' action='/quest/complete' style='display:inline;'><input type='hidden' name='quest_id' value='").append(m.getId()).append("'>");
                        html.append("<button type='submit' class='btn btn-sm btn-teal'>Mark Finished</button></form>");
                    } else {
                        html.append("<span style='font-size:0.85rem; color:var(--text-muted);'>Awaiting Verification</span>");
                    }
                    html.append("</td></tr>");
                }
                html.append("</tbody></table></div>");
            }
            html.append("</div>");

            // My Posted Tasks
            html.append("<div><h2 style='font-size:1.4rem; font-weight:700; margin-bottom:1rem;'>My Posted Tasks (Requester Role)</h2>");
            if (posted.isEmpty()) {
                html.append("<div class='card' style='padding:1.5rem; color:var(--text-muted);'>No tasks posted yet.</div>");
            } else {
                html.append("<div class='table-wrapper'><table class='table'><thead><tr><th>Task Title</th><th>Escrow Budget</th><th>Status</th><th>Assigned Helper</th><th>Action</th></tr></thead><tbody>");
                for (Quest p : posted) {
                    html.append("<tr><td><strong>").append(p.getTitle()).append("</strong></td>");
                    html.append("<td><span class='currency-badge'>💳 ").append(String.format("%.1f", p.getReward())).append("</span></td>");
                    html.append("<td><span class='badge badge-").append(p.getStatus().toLowerCase()).append("'>").append(p.getStatus()).append("</span></td>");
                    html.append("<td>").append(p.getSolverName() != null ? p.getSolverName() : "<em>Unassigned</em>").append("</td>");
                    html.append("<td>");
                    if ("COMPLETED".equals(p.getStatus())) {
                        html.append("<form method='POST' action='/quest/verify' style='display:inline;'><input type='hidden' name='quest_id' value='").append(p.getId()).append("'>");
                        html.append("<button type='submit' class='btn btn-sm btn-primary'>Verify & Pay</button></form>");
                    } else if ("VERIFIED".equals(p.getStatus())) {
                        html.append("<span style='font-size:0.85rem; color:var(--status-open);'>Verified</span>");
                    } else {
                        html.append("<span style='font-size:0.85rem; color:var(--text-muted);'>&mdash;</span>");
                    }
                    html.append("</td></tr>");
                }
                html.append("</tbody></table></div>");
            }
            html.append("</div>");

            html.append(renderFooter());
            sendHtml(exchange, 200, html.toString());
        }
    }

    static class PostTaskHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            User user = getSessionUser(exchange);
            if (user == null) {
                sendRedirect(exchange, "/auth/login");
                return;
            }

            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                Map<String, String> data = parseFormData(exchange);
                Quest q = new Quest();
                q.setTitle(data.get("title"));
                q.setDescription(data.get("description"));
                q.setCategory(data.getOrDefault("category", "Labor"));
                q.setReward(Double.parseDouble(data.getOrDefault("reward", "10")));
                q.setPosterId(user.getId());

                boolean ok = questDAO.createQuest(q);
                if (ok) {
                    sendRedirect(exchange, "/dashboard");
                    return;
                }
            }

            StringBuilder html = new StringBuilder(renderHeader("Post Task", user));
            html.append("<div class='form-card'>");
            html.append("<h2 style='text-align:center; margin-bottom:0.5rem; font-weight:800;'>Post a Campus Task</h2>");
            html.append("<p style='text-align:center; color:var(--text-muted); margin-bottom:1.5rem;'>Available Balance: 💳 ").append(String.format("%.1f", user.getCredits())).append(" Credits</p>");
            html.append("<form method='POST' action='/quest/post'>");
            html.append("<div class='form-group'><label class='form-label'>Task Title</label><input type='text' name='title' class='form-control' required></div>");
            html.append("<div class='form-group'><label class='form-label'>Category</label><select name='category' class='form-control'>");
            html.append("<option value='Urgent'>🚨 Urgent / Time-Sensitive</option><option value='Medical'>💊 Medical</option><option value='Tech Support'>💻 Tech Support</option><option value='Academics'>📚 Academics</option><option value='Logistics'>📦 Logistics</option><option value='Labor' selected>🛠️ General Labor</option></select></div>");
            html.append("<div class='form-group'><label class='form-label'>Reward Budget (Held in Escrow)</label><input type='number' name='reward' class='form-control' min='1' step='0.5' value='25' required></div>");
            html.append("<div class='form-group'><label class='form-label'>Instructions / Deliverables</label><textarea name='description' class='form-control' rows='4' required></textarea></div>");
            html.append("<button type='submit' class='btn btn-primary' style='width:100%; margin-top:1rem;'>Publish & Escrow Credits</button>");
            html.append("</form></div>");
            html.append(renderFooter());
            sendHtml(exchange, 200, html.toString());
        }
    }

    static class AcceptTaskHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            User user = getSessionUser(exchange);
            if (user != null && "POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                Map<String, String> data = parseFormData(exchange);
                int qId = Integer.parseInt(data.get("quest_id"));
                questDAO.acceptQuest(qId, user.getId());
            }
            sendRedirect(exchange, "/dashboard");
        }
    }

    static class CompleteTaskHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            User user = getSessionUser(exchange);
            if (user != null && "POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                Map<String, String> data = parseFormData(exchange);
                int qId = Integer.parseInt(data.get("quest_id"));
                questDAO.completeQuest(qId, user.getId());
            }
            sendRedirect(exchange, "/dashboard");
        }
    }

    static class VerifyTaskHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            User user = getSessionUser(exchange);
            if (user != null && "POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                Map<String, String> data = parseFormData(exchange);
                int qId = Integer.parseInt(data.get("quest_id"));
                questDAO.verifyQuest(qId, user.getId());
            }
            sendRedirect(exchange, "/dashboard");
        }
    }

    static class SeedTaskHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            User user = getSessionUser(exchange);
            if (user != null) {
                questDAO.seedStarterQuests(user.getId());
            }
            sendRedirect(exchange, "/dashboard");
        }
    }

    static class LeaderboardHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            User user = getSessionUser(exchange);
            List<User> list = userDAO.getLeaderboard(20);

            StringBuilder html = new StringBuilder(renderHeader("Tasker Rankings", user));
            html.append("<div style='margin-bottom:2rem; text-align:center;'><h1 class='hero-title' style='font-size:2.2rem;'>Campus Tasker Rankings</h1><p style='color:var(--text-muted);'>Ranked by Contribution Points (XP) & Trust Rating.</p></div>");
            html.append("<div class='table-wrapper'><table class='table'><thead><tr><th>Rank</th><th>Student Tasker</th><th>Proficiency Level</th><th>Trust Rating</th><th>Contribution XP</th></tr></thead><tbody>");
            int rank = 1;
            for (User u : list) {
                String medal = rank == 1 ? "🥇" : (rank == 2 ? "🥈" : (rank == 3 ? "🥉" : "#" + rank));
                html.append("<tr><td style='font-weight:800; font-size:1.1rem;'>").append(medal).append("</td>");
                html.append("<td><strong>").append(u.getUsername()).append("</strong></td>");
                html.append("<td><span class='badge badge-category'>").append(u.getRole()).append("</span></td>");
                html.append("<td>★ ").append(String.format("%.1f", u.getReputation())).append("</td>");
                html.append("<td style='font-weight:700; color:#818cf8; font-family:JetBrains Mono,monospace;'>").append(u.getXp()).append(" XP</td></tr>");
                rank++;
            }
            html.append("</tbody></table></div>");
            html.append(renderFooter());
            sendHtml(exchange, 200, html.toString());
        }
    }

    static class ProfileHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            User user = getSessionUser(exchange);
            if (user == null) {
                sendRedirect(exchange, "/auth/login");
                return;
            }

            List<Transaction> txs = transactionDAO.getTransactionsForUser(user.getId(), 25);
            StringBuilder html = new StringBuilder(renderHeader("Tasker Profile", user));

            html.append("<div class='stats-banner'>");
            html.append("<div class='stat-item'><span class='stat-label'>Username</span><span class='stat-value'>").append(user.getUsername()).append("</span></div>");
            html.append("<div class='stat-item'><span class='stat-label'>Proficiency Level</span><span class='stat-value' style='color:#818cf8;'>").append(user.getRole()).append("</span></div>");
            html.append("<div class='stat-item'><span class='stat-label'>Available Credits</span><span class='stat-value primary'>💳 ").append(String.format("%.1f", user.getCredits())).append(" Cr</span></div>");
            html.append("<div class='stat-item'><span class='stat-label'>Trust Rating</span><span class='stat-value emerald'>★ ").append(String.format("%.1f", user.getReputation())).append(" / 5.0</span></div>");
            html.append("</div>");

            html.append("<div style='margin-top:2rem;'><h2 style='font-size:1.4rem; font-weight:700; margin-bottom:1rem;'>Credit & Escrow Activity Ledger</h2>");
            if (txs.isEmpty()) {
                html.append("<div class='card' style='padding:1.5rem; color:var(--text-muted);'>No activity records found.</div>");
            } else {
                html.append("<div class='table-wrapper'><table class='table'><thead><tr><th>Timestamp</th><th>Type</th><th>Task Title</th><th>Amount</th></tr></thead><tbody>");
                for (Transaction t : txs) {
                    boolean isCredit = (t.getReceiverId() != null && t.getReceiverId() == user.getId());
                    String sign = isCredit ? "+" : "-";
                    String color = isCredit ? "var(--status-open)" : "var(--status-disputed)";
                    html.append("<tr><td>").append(t.getTimestamp()).append("</td>");
                    html.append("<td><span class='badge badge-category'>").append(t.getTxType()).append("</span></td>");
                    html.append("<td>").append(t.getQuestTitle() != null ? t.getQuestTitle() : "<em>Starter Grant</em>").append("</td>");
                    html.append("<td style='font-weight:700; color:").append(color).append("; font-family:JetBrains Mono,monospace;'>").append(sign).append(String.format("%.1f", t.getAmount())).append(" Credits</td></tr>");
                }
                html.append("</tbody></table></div>");
            }
            html.append("</div>");
            html.append(renderFooter());
            sendHtml(exchange, 200, html.toString());
        }
    }

    static class ApiPrioritizedHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            List<Quest> raw = questDAO.getOpenQuests(0);
            List<Quest> sorted = TaskPriorityQueue.prioritize(raw);

            StringBuilder json = new StringBuilder("[");
            for (int i = 0; i < sorted.size(); i++) {
                Quest q = sorted.get(i);
                json.append("{")
                    .append("\"id\":").append(q.getId()).append(",")
                    .append("\"title\":\"").append(q.getTitle().replace("\"", "\\\"")).append("\",")
                    .append("\"category\":\"").append(q.getCategory()).append("\",")
                    .append("\"reward\":").append(q.getReward()).append(",")
                    .append("\"priorityScore\":").append(Math.round(q.getPriorityScore())).append(",")
                    .append("\"urgencyTier\":\"").append(q.getUrgencyTier()).append("\",")
                    .append("\"posterName\":\"").append(q.getPosterName() != null ? q.getPosterName().replace("\"", "\\\"") : "").append("\"")
                    .append("}");
                if (i < sorted.size() - 1) json.append(",");
            }
            json.append("]");

            byte[] bytes = json.toString().getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        }
    }
}
