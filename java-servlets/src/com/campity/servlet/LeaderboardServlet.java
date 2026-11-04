package com.campity.servlet;

import com.campity.dao.UserDAO;
import com.campity.model.User;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@WebServlet(urlPatterns = {"/leaderboard"})
public class LeaderboardServlet extends HttpServlet {

    private final UserDAO userDAO = new UserDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        List<User> topUsers = userDAO.getLeaderboard(20);
        req.setAttribute("topUsers", topUsers);
        req.getRequestDispatcher("/leaderboard.jsp").forward(req, resp);
    }
}
