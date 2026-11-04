# TaskFlow: Priority-Driven Campus Task Management & Posting System
> **Full Stack Replication using HTML5, CSS3, PHP, and Java Servlets**

---

## 📌 Executive Summary & Analysis of Workspace Web Projects

A comprehensive survey of the projects located in `/run/media/mrlucifer006/346E71E66E71A0F2/Personal Projects` identified over 30 web-related repositories. These were analyzed, classified, and benchmarked across architectural tiers:

### 1. Beginner / Foundational Projects
* **`Digital-Checkpoint-System`**: Basic tourist registration and QR checking system. Explicitly designed for beginners using simple HTML/JS and basic Java/Python/Node servers with minimal schema complexity.
* **`quiet-scan`**: Minimal Flask application reading sound levels and persisting credentials to a flat CSV file.
* **`AIML-Assigment`**: Single-route Flask/FastAPI interface rendering an ML prediction template.
* **`biosite`**: Static HTML portfolio wrapped in a Docker container.
* **`message_based_chatbot`**: Lightweight single-page chat dashboard.
* **`sample`**: Static HTML demonstration file.

### 2. Advanced / Enterprise / Distributed Systems
* **`SDC event (Castle Enigma)`**: Multi-service contest platform with Fastify microservices, BullMQ distributed Redis queue, isolated Dockerode execution sandbox, Monaco web IDE, and Kubernetes manifests.
* **`AI-Based-Irrigation-Management-System...`**: Full Next.js (TypeScript, Tailwind, Framer Motion) frontend paired with FastAPI and MLflow predictive pipeline + Flutter PWA.
* **`ATM (Smart Energy ATM)`**: Hybrid real-time IoT architecture combining React/Vite/Tailwind, FastAPI, C computational engine subprocess, Supabase, and ESP32 telemetry WebSockets.
* **`internship (Visitor Management System)`**: Enterprise-grade multi-level RBAC (5 authority levels), WhatsApp daemon, logistics vehicle camera tracking, caching manager, and Android companion app.
* **`WaitWise-Mobile-App`**: Socket.io real-time queue orchestration with Gemini AI triage and Flutter mobile client.
* **`Saveon`**: Serverless Firebase Cloud Functions, Firestore security rules, and IoT hardware simulators.

### 3. Mid-Level Projects & The Selected Benchmark
* **Candidates**: `Campity`, `wooble` (AuraHR), `legacycodereuse`, `Billing`, `Data_Visulization_Frontend_Team-a`.
* **Chosen Mid-Level Benchmark**: **`Campity`**
* **Rationale**: `Campity` represents the ideal mid-level web application:
  1. Complete relational database model with transactions and foreign keys (`Users`, `Tasks`, `Transactions`).
  2. Non-trivial algorithmic core: **Intelligent Priority Queue** using category weights + reward economics + deadlines.
  3. Real-world business logic: Escrow deposits, 10% helper accountability stake locks, review verification, peer star ratings, and XP-driven tier progression.
  4. Multi-page templated frontend with responsive design and custom stylesheets.

---

## 🎨 Theme Transformation: Campus Task Management & Posting System

In accordance with requirements, the gamified fantasy terminology ("Adventurers Guild", "Goblin Maps", "Quests", "Mora") has been refactored into a professional **Campus Task Management & Posting System**:

| Original Term | Refactored Task Management Equivalent | Role in System |
| :--- | :--- | :--- |
| **Quest / Bounty** | **Campus Task** | Unit of work posted by students/faculty |
| **Post Quest** | **Post Task** | Creation form with escrow deduction & category selection |
| **Missions** | **My Assigned Tasks** | Tasks claimed by student helpers |
| **Adventurers** | **Student Taskers** | Community members completing tasks |
| **Guild Ranks** | **Tasker Proficiency Tiers** | `Junior Tasker` → `Associate Tasker` → `Senior Tasker` → `Lead Coordinator` |
| **Mora / Emeralds** | **Campus Task Credits** | Wallet currency held in escrow until verified delivery |
| **Goblin Maps** | **Sample Campus Tasks** | Library book returns, lab projector fixes, prescription deliveries |

---

## 🏗️ System Architecture & Technology Stack

This repository provides two complete, interoperable implementations of the task management platform:

```
Campity-WebStack-Replication/
├── assets/                               # Shared UI & Design System
│   ├── css/
│   │   ├── style.css                     # Modern SaaS Task Management design
│   │   └── themes.css                    # Multi-theme suite (Dark Modern, Clean Light, Slate, Emerald)
│   └── js/
│       └── app.js                        # Dynamic stake calculators, theme switcher, confirmations
├── lib/                                  # Java Servlets & JDBC runtime libraries
│   ├── javax.servlet-api-4.0.1.jar
│   └── sqlite-jdbc-3.42.0.0.jar
├── php/                                  # Complete PHP Web Stack
│   ├── config/database.php               # SQLite PDO connection & auto-schema migration
│   ├── includes/
│   │   ├── PriorityQueue.php             # PHP Priority Queue task sorting engine
│   │   ├── auth.php                      # Session management, bcrypt password security, rank updates
│   │   ├── header.php & footer.php       # Shared layout and navigation components
│   ├── index.php                         # Platform landing & metric summary
│   ├── login.php & register.php          # Auth with 100 starter credit grant
│   ├── dashboard.php                     # Priority Task Feed, Assigned Tasks, Posted Tasks
│   ├── post_quest.php                    # Task creation with escrow lock & file attachment
│   ├── quest_action.php                  # Accept (10% stake), Mark Finished, Verify & Pay
│   ├── profile.php                       # Student tasker profile & credit activity ledger
│   ├── leaderboard.php                   # Campus tasker rankings by XP and trust rating
│   ├── seed.php                          # Seed sample campus tasks across categories
│   └── download.php                      # Secure task attachment deliverable download
└── java-servlets/                        # Complete Java Servlets Web Stack
    ├── src/
    │   ├── com/campity/model/            # User, Quest (Task), Transaction models
    │   ├── com/campity/algorithm/        # TaskPriorityQueue (java.util.PriorityQueue Max-Heap)
    │   ├── com/campity/dao/              # DBUtil, UserDAO, QuestDAO, TransactionDAO (ACID JDBC)
    │   ├── com/campity/servlet/          # AuthServlet, DashboardServlet, QuestServlet, LeaderboardServlet, ProfileServlet, PriorityQueueApiServlet
    │   ├── com/campity/filter/           # AuthFilter for session route protection
    │   └── com/campity/server/           # EmbeddedServer (Standalone runnable on JDK HttpServer)
    └── webapp/
        ├── WEB-INF/web.xml               # Standard Java EE 4.0 Deployment Descriptor
        ├── index.jsp, login.jsp, register.jsp
        ├── dashboard.jsp, post_quest.jsp
        └── leaderboard.jsp, profile.jsp
```

---

## ⚡ The Priority Queue Scheduling Algorithm

Both implementations feature an intelligent priority queue algorithm that ranks available tasks to maximize responsiveness for urgent campus needs:

$$\text{Priority Score} = (\text{Category Weight} \times 10) + (\text{Reward} \times 0.5) + \text{Deadline Urgency Bonus}$$

### Category Weight Matrix:
* **Medical / Health**: `100` (Max Priority)
* **Urgent / Time-Sensitive**: `90`
* **Tech & Hardware Support**: `70`
* **Academics & Notes**: `60`
* **Campus Logistics & Delivery**: `50`
* **General Assistance & Labor**: `40`

---

## 🚀 How to Run the Applications

### Option 1: Running the Java Servlets Stack (Standalone)

The Java implementation includes a pre-compiled standalone `EmbeddedServer` that runs directly on port `8080` without requiring external Tomcat setup:

```bash
cd "Campity-WebStack-Replication"

# Run the Embedded Server:
java -cp "java-servlets/bin:lib/*" com.campity.server.EmbeddedServer
```

* **Web Portal**: Open `http://localhost:8080` in your browser.
* **REST API Endpoint**: Access prioritized tasks at `http://localhost:8080/api/quests/prioritized`.

*(To recompile the Java source files at any time)*:
```bash
javac -d java-servlets/bin -cp "lib/*" $(find java-servlets/src -name "*.java")
```

---

### Option 2: Running the PHP Stack

You can run the PHP implementation using PHP's built-in web server or Apache/Nginx:

```bash
cd "Campity-WebStack-Replication/php"

# Start the built-in development server:
php -S localhost:8000
```

* **Web Portal**: Open `http://localhost:8000` in your browser.
* Database (`campity.db`) will auto-initialize on first page access.
* Click **"Load Sample Tasks"** on the dashboard to populate realistic campus errands.

---

### Option 3: Standard Tomcat / Java EE WAR Deployment

For production Java EE servlet containers (Apache Tomcat 9/10, Jetty):
1. Copy `java-servlets/webapp/` contents to Tomcat `webapps/taskflow/`.
2. Compile classes into `webapps/taskflow/WEB-INF/classes/`.
3. Copy `lib/*.jar` into `webapps/taskflow/WEB-INF/lib/`.
4. Deploy and access via `http://localhost:8080/taskflow/`.
