package com.campity.servlet;

import com.campity.dao.QuestDAO;
import com.campity.dao.UserDAO;
import com.campity.model.Quest;
import com.campity.model.User;

import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.File;
import java.io.IOException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@WebServlet(urlPatterns = {"/quest/post", "/quest/accept", "/quest/complete", "/quest/verify", "/quest/seed"})
@MultipartConfig(
        fileSizeThreshold = 1024 * 1024,      // 1 MB
        maxFileSize = 1024 * 1024 * 10,       // 10 MB
        maxRequestSize = 1024 * 1024 * 20     // 20 MB
)
public class QuestServlet extends HttpServlet {

    private final QuestDAO questDAO = new QuestDAO();
    private final UserDAO userDAO = new UserDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String path = req.getServletPath();
        if ("/quest/post".equals(path)) {
            req.getRequestDispatcher("/post_quest.jsp").forward(req, resp);
        } else if ("/quest/seed".equals(path)) {
            HttpSession session = req.getSession(false);
            if (session != null && session.getAttribute("userId") != null) {
                int userId = (int) session.getAttribute("userId");
                questDAO.seedStarterQuests(userId);
                session.setAttribute("flashMessage", "Goblin Maps discovered! Sample campus bounties successfully seeded.");
                session.setAttribute("flashType", "success");
            }
            resp.sendRedirect(req.getContextPath() + "/dashboard");
        } else {
            resp.sendRedirect(req.getContextPath() + "/dashboard");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("userId") == null) {
            resp.sendRedirect(req.getContextPath() + "/auth/login");
            return;
        }

        int userId = (int) session.getAttribute("userId");
        String path = req.getServletPath();

        if ("/quest/post".equals(path)) {
            handlePostQuest(req, resp, userId, session);
        } else if ("/quest/accept".equals(path)) {
            handleAcceptQuest(req, resp, userId, session);
        } else if ("/quest/complete".equals(path)) {
            handleCompleteQuest(req, resp, userId, session);
        } else if ("/quest/verify".equals(path)) {
            handleVerifyQuest(req, resp, userId, session);
        } else {
            resp.sendRedirect(req.getContextPath() + "/dashboard");
        }
    }

    private void handlePostQuest(HttpServletRequest req, HttpServletResponse resp, int userId, HttpSession session) throws ServletException, IOException {
        String title = req.getParameter("title");
        String description = req.getParameter("description");
        String category = req.getParameter("category");
        String rewardStr = req.getParameter("reward");
        String deadlineStr = req.getParameter("deadline");

        if (title == null || description == null || rewardStr == null) {
            req.setAttribute("error", "Title, description, and reward are required.");
            req.getRequestDispatcher("/post_quest.jsp").forward(req, resp);
            return;
        }

        double reward = Double.parseDouble(rewardStr);
        User user = userDAO.findById(userId);

        if (user.getCredits() < reward) {
            req.setAttribute("error", "Insufficient credits. You need " + reward + " Credits.");
            req.getRequestDispatcher("/post_quest.jsp").forward(req, resp);
            return;
        }

        // File upload handling
        String filePath = null;
        try {
            Part filePart = req.getPart("attachment");
            if (filePart != null && filePart.getSize() > 0) {
                String fileName = System.currentTimeMillis() + "_" + filePart.getSubmittedFileName().replaceAll("[^a-zA-Z0-9._-]", "_");
                String uploadDir = req.getServletContext().getRealPath("/uploads");
                File uploadFolder = new File(uploadDir);
                if (!uploadFolder.exists()) uploadFolder.mkdirs();
                filePart.write(uploadDir + File.separator + fileName);
                filePath = "uploads/" + fileName;
            }
        } catch (Exception ignored) {}

        Quest q = new Quest();
        q.setTitle(title);
        q.setDescription(description);
        q.setCategory(category != null ? category : "Labor");
        q.setReward(reward);
        q.setPosterId(userId);
        q.setFilePath(filePath);

        if (deadlineStr != null && !deadlineStr.trim().isEmpty()) {
            try {
                LocalDateTime ldt = LocalDateTime.parse(deadlineStr);
                q.setDeadline(Timestamp.valueOf(ldt));
            } catch (Exception ignored) {}
        }

        boolean created = questDAO.createQuest(q);
        if (created) {
            session.setAttribute("flashMessage", "Ad Astra! Bounty '" + title + "' published and " + reward + " credits held in escrow.");
            session.setAttribute("flashType", "success");
            resp.sendRedirect(req.getContextPath() + "/dashboard");
        } else {
            req.setAttribute("error", "Failed to create bounty. Check balance.");
            req.getRequestDispatcher("/post_quest.jsp").forward(req, resp);
        }
    }

    private void handleAcceptQuest(HttpServletRequest req, HttpServletResponse resp, int userId, HttpSession session) throws IOException {
        int questId = Integer.parseInt(req.getParameter("quest_id"));
        boolean success = questDAO.acceptQuest(questId, userId);
        if (success) {
            session.setAttribute("flashMessage", "Commission accepted! Stake credits locked.");
            session.setAttribute("flashType", "success");
        } else {
            session.setAttribute("flashMessage", "Unable to accept commission. Check stake balance or assignment.");
            session.setAttribute("flashType", "danger");
        }
        resp.sendRedirect(req.getContextPath() + "/dashboard");
    }

    private void handleCompleteQuest(HttpServletRequest req, HttpServletResponse resp, int userId, HttpSession session) throws IOException {
        int questId = Integer.parseInt(req.getParameter("quest_id"));
        boolean success = questDAO.completeQuest(questId, userId);
        if (success) {
            session.setAttribute("flashMessage", "Mission marked finished! Waiting for guild verification.");
            session.setAttribute("flashType", "success");
        } else {
            session.setAttribute("flashMessage", "Failed to update mission status.");
            session.setAttribute("flashType", "danger");
        }
        resp.sendRedirect(req.getContextPath() + "/dashboard");
    }

    private void handleVerifyQuest(HttpServletRequest req, HttpServletResponse resp, int userId, HttpSession session) throws IOException {
        int questId = Integer.parseInt(req.getParameter("quest_id"));
        boolean success = questDAO.verifyQuest(questId, userId);
        if (success) {
            session.setAttribute("flashMessage", "Bounty verified! Escrow payout and stake returned to helper (+50 XP).");
            session.setAttribute("flashType", "success");
        } else {
            session.setAttribute("flashMessage", "Verification failed.");
            session.setAttribute("flashType", "danger");
        }
        resp.sendRedirect(req.getContextPath() + "/dashboard");
    }
}
