package com.campity.servlet;

import com.campity.dao.UserDAO;
import com.campity.model.User;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

@WebServlet(urlPatterns = {"/auth/login", "/auth/register", "/auth/logout"})
public class AuthServlet extends HttpServlet {

    private final UserDAO userDAO = new UserDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String path = req.getServletPath();
        if ("/auth/logout".equals(path)) {
            HttpSession session = req.getSession(false);
            if (session != null) {
                session.invalidate();
            }
            resp.sendRedirect(req.getContextPath() + "/index.jsp");
        } else if ("/auth/register".equals(path)) {
            req.getRequestDispatcher("/register.jsp").forward(req, resp);
        } else {
            req.getRequestDispatcher("/login.jsp").forward(req, resp);
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String path = req.getServletPath();
        String username = req.getParameter("username");
        String password = req.getParameter("password");

        if (username == null || password == null || username.trim().isEmpty() || password.trim().isEmpty()) {
            req.setAttribute("error", "Username and password cannot be empty.");
            req.getRequestDispatcher("/login.jsp").forward(req, resp);
            return;
        }

        username = username.trim();

        if ("/auth/register".equals(path)) {
            boolean success = userDAO.register(username, password);
            if (success) {
                req.getSession().setAttribute("flashMessage", "Welcome to Campity, " + username + "! 100 UBI Credits granted.");
                req.getSession().setAttribute("flashType", "success");
                resp.sendRedirect(req.getContextPath() + "/auth/login");
            } else {
                req.setAttribute("error", "Username is already taken or registration failed.");
                req.getRequestDispatcher("/register.jsp").forward(req, resp);
            }
        } else {
            // Login
            User user = userDAO.authenticate(username, password);
            if (user != null) {
                HttpSession session = req.getSession(true);
                session.setAttribute("user", user);
                session.setAttribute("userId", user.getId());
                session.setAttribute("username", user.getUsername());
                resp.sendRedirect(req.getContextPath() + "/dashboard");
            } else {
                req.setAttribute("error", "Invalid username or password.");
                req.getRequestDispatcher("/login.jsp").forward(req, resp);
            }
        }
    }
}
