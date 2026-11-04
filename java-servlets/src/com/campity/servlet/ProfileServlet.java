package com.campity.servlet;

import com.campity.dao.TransactionDAO;
import com.campity.dao.UserDAO;
import com.campity.model.Transaction;
import com.campity.model.User;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.List;

@WebServlet(urlPatterns = {"/profile"})
public class ProfileServlet extends HttpServlet {

    private final UserDAO userDAO = new UserDAO();
    private final TransactionDAO transactionDAO = new TransactionDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("userId") == null) {
            resp.sendRedirect(req.getContextPath() + "/auth/login");
            return;
        }

        int userId = (int) session.getAttribute("userId");
        User user = userDAO.findById(userId);
        List<Transaction> transactions = transactionDAO.getTransactionsForUser(userId, 25);

        req.setAttribute("user", user);
        req.setAttribute("transactions", transactions);
        req.getRequestDispatcher("/profile.jsp").forward(req, resp);
    }
}
