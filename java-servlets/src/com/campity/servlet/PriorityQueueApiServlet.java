package com.campity.servlet;

import com.campity.algorithm.TaskPriorityQueue;
import com.campity.dao.QuestDAO;
import com.campity.model.Quest;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

@WebServlet(urlPatterns = {"/api/quests/prioritized"})
public class PriorityQueueApiServlet extends HttpServlet {

    private final QuestDAO questDAO = new QuestDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");

        int excludeUserId = 0;
        String excludeParam = req.getParameter("exclude_user");
        if (excludeParam != null && !excludeParam.trim().isEmpty()) {
            try {
                excludeUserId = Integer.parseInt(excludeParam);
            } catch (NumberFormatException ignored) {}
        }

        List<Quest> rawQuests = questDAO.getOpenQuests(excludeUserId);
        List<Quest> sortedQuests = TaskPriorityQueue.prioritize(rawQuests);

        StringBuilder json = new StringBuilder("[");
        for (int i = 0; i < sortedQuests.size(); i++) {
            Quest q = sortedQuests.get(i);
            json.append("{")
                .append("\"id\":").append(q.getId()).append(",")
                .append("\"title\":\"").append(escapeJson(q.getTitle())).append("\",")
                .append("\"category\":\"").append(escapeJson(q.getCategory())).append("\",")
                .append("\"reward\":").append(q.getReward()).append(",")
                .append("\"priorityScore\":").append(Math.round(q.getPriorityScore())).append(",")
                .append("\"urgencyTier\":\"").append(q.getUrgencyTier()).append("\",")
                .append("\"posterName\":\"").append(escapeJson(q.getPosterName())).append("\"")
                .append("}");
            if (i < sortedQuests.size() - 1) {
                json.append(",");
            }
        }
        json.append("]");

        try (PrintWriter out = resp.getWriter()) {
            out.print(json.toString());
            out.flush();
        }
    }

    private String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r");
    }
}
