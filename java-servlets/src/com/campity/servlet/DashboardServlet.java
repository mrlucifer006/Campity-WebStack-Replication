package com.campity.servlet;

import com.campity.algorithm.TaskPriorityQueue;
import com.campity.dao.QuestDAO;
import com.campity.dao.UserDAO;
import com.campity.model.Quest;
import com.campity.model.User;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.List;

@WebServlet(urlPatterns = {"/dashboard"})
public class DashboardServlet extends HttpServlet {

    private final QuestDAO questDAO = new QuestDAO();
    private final UserDAO userDAO = new UserDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("userId") == null) {
            resp.sendRedirect(req.getContextPath() + "/auth/login");
            return;
        }

        int userId = (int) session.getAttribute("userId");
        User freshUser = userDAO.findById(userId);
        session.setAttribute("user", freshUser);

        // Available Quests dynamically prioritized by Priority Queue
        List<Quest> rawOpenQuests = questDAO.getOpenQuests(userId);
        List<Quest> prioritizedQuests = TaskPriorityQueue.prioritize(rawOpenQuests);

        // Missions (where user is helper)
        List<Quest> activeMissions = questDAO.getMissionsForSolver(userId);

        // Posted Quests (where user is poster)
        List<Quest> postedQuests = questDAO.getQuestsByPoster(userId);

        req.setAttribute("availableQuests", prioritizedQuests);
        req.setAttribute("activeMissions", activeMissions);
        req.setAttribute("postedQuests", postedQuests);

        req.getRequestDispatcher("/dashboard.jsp").forward(req, resp);
    }
}
