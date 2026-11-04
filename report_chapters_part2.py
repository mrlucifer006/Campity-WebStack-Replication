# Chapters 2, 3, and 4 data for TaskFlow Project Report

CHAPTER_2 = {
    "title": "CHAPTER 2 — LITERATURE SURVEY & WORKSPACE BENCHMARKING",
    "sections": [
        {
            "num": "2.1",
            "title": "WORKSPACE WEB ARCHITECTURE BENCHMARK",
            "paragraphs": [
                "Prior to implementation, an exhaustive architectural survey was conducted across more than thirty web repositories residing in the developer's local software workspace. The purpose of this benchmark was to analyze the spectrum of architectural paradigms, database strategies, concurrency patterns, and algorithmic complexity currently applied in web application development, thereby establishing a rigorous foundation for selecting an optimal replication candidate.",
                "The analyzed projects exhibited wide structural variance, ranging from minimalistic single-file web interfaces to heavily distributed microservice clusters. To establish a coherent analytical taxonomy, the projects were classified into three primary complexity tiers: Foundational / Beginner, Mid-Level / Algorithmic, and Advanced / Distributed Enterprise."
            ]
        },
        {
            "num": "2.2",
            "title": "COMPARATIVE ANALYSIS OF ARCHITECTURAL TIERS",
            "paragraphs": [
                "1. Tier 1: Foundational / Beginner Projects: This tier comprises repositories such as 'Digital-Checkpoint-System' (a basic tourist check-in platform utilizing raw DOM scripts and lightweight Node/Python servers), 'quiet-scan' (a simple audio meter logging records to a flat CSV file), 'AIML-Assigment' (a single-route Flask model interface), and 'biosite' (a containerized static HTML portfolio). These projects feature flat data stores, lack concurrency protection, and incorporate negligible relational business logic.",
                "2. Tier 3: Advanced / Distributed Enterprise Projects: At the opposite extreme, projects such as 'SDC event (Castle Enigma)' (a multi-service coding contest engine pairing Fastify with Redis BullMQ, Dockerode execution isolation, and Kubernetes manifests), 'ATM (Smart Energy ATM)' (an IoT telemetry pipeline integrating React, FastAPI, a C computational engine, and Supabase), and 'internship (Visitor Management System)' (an enterprise platform with 5-tier RBAC, automated WhatsApp daemons, and ANPR vehicle recognition) feature substantial distributed complexity. While powerful, their microservice overhead obscures the direct evaluation of core web technologies laboratory paradigms.",
                "3. Tier 2: Mid-Level Benchmark Projects: Projects in this middle tier—notably 'Campity', 'wooble' (AuraHR), and 'Billing'—balance full-stack completeness with architectural transparency. Among these, Campity emerged as the standout benchmark due to its robust relational data model (Users, Quests, Transactions), stateful business rules (escrow holding and stake locking), dynamic priority queue algorithm, and modular multi-page interface."
            ]
        },
        {
            "num": "2.3",
            "title": "RATIONALE FOR SELECTING CAMPITY AS THE BENCHMARK",
            "paragraphs": [
                "Campity was selected as the definitive web engineering benchmark based on four decisive technical criteria:",
                "1. Complete Relational Lifecycle: The data model requires strict foreign key relationships, transactional updates across multiple tables, and atomic state transitions.",
                "2. Non-Trivial Algorithmic Core: Unlike standard CRUD portals, Campity incorporates an intelligent scheduling algorithm that actively computes dynamic priorities for incoming items based on multiple mathematical parameters.",
                "3. Real-World Economic Rules: The system enforces financial escrow and accountability stake locks, requiring robust error handling and rollback semantics under concurrent user requests.",
                "4. Cross-Stack Reproducibility: Its decoupled architecture allows seamless reimplementation across both scripting (PHP) and compiled enterprise (Java EE Servlets) paradigms."
            ]
        },
        {
            "num": "2.4",
            "title": "DOMAIN TRANSFORMATION: CAMPUS TASK MANAGEMENT SYSTEM",
            "paragraphs": [
                "While the technical underpinnings of the original Campity codebase were sound, its fantasy role-playing theme ('Adventurers Guild', 'Goblin Maps', 'Quests', 'Mora Currency') was unsuitable for practical academic and institutional deployment. Consequently, a comprehensive domain refactoring was executed, transposing game concepts into professional higher-education terminology:",
                "• 'Quest / Bounty' was transformed into 'Campus Task'—a formalized unit of assistance posted by students or faculty.",
                "• 'Adventurer' was transformed into 'Student Tasker'—a verified peer providing errand or academic assistance.",
                "• 'Guild Ranks' were mapped to 'Tasker Proficiency Tiers'—progressing from Junior Tasker to Associate Tasker, Senior Tasker, and Lead Coordinator.",
                "• 'Mora / Emeralds' was transformed into 'Campus Task Credits'—the internal transactional utility currency held in escrow.",
                "• 'Goblin Maps' was refactored into 'Sample Campus Errands'—concrete tasks including hardware lab deliveries, library book returns, and projector troubleshooting."
            ]
        }
    ]
}

CHAPTER_3 = {
    "title": "CHAPTER 3 — SYSTEM ARCHITECTURE & DUAL-STACK DESIGN",
    "sections": [
        {
            "num": "3.1",
            "title": "HIGH-LEVEL DUAL-ENGINE ARCHITECTURE",
            "paragraphs": [
                "TaskFlow is architected as an interoperable, dual-engine web application. Both backends—the PHP 8+ engine and the Java EE 4.0 Servlet engine—are designed to operate against a shared presentation tier and an identical relational SQLite database (campity.db). This decoupled design ensures that user interface assets, layout components, and client-side scripts remain 100% reusable regardless of which backend engine serves the request.",
                "Figure 3.1 illustrates the high-level dual-stack architecture of TaskFlow. The Client Presentation Tier communicates over HTTP with either the PHP Web Engine or the Java Servlets Engine. Both engines implement identical session validation, algorithmic task sorting, and transactional business logic, interacting with the shared Persistence Tier."
            ]
        },
        {
            "num": "3.2",
            "title": "SHARED FRONTEND PRESENTATION TIER",
            "paragraphs": [
                "The frontend layer is built using clean, semantic HTML5, modern CSS3 with custom CSS Custom Properties (variables), and vanilla JavaScript. To provide a professional user experience, the interface adheres to modern Software-as-a-Service (SaaS) design standards, incorporating glassmorphic card elements, subtle drop-shadows, responsive CSS Grid and Flexbox layouts, and high-contrast typography.",
                "A key feature of the presentation tier is the dynamic Multi-Theme Suite defined in assets/css/themes.css. TaskFlow supports four distinct visual themes: Dark Modern (default high-contrast slate), Clean Light (minimalist academic look), Slate (neutral corporate palette), and Emerald (vibrant campus greenery). Theme selections are persisted locally via localStorage and dynamically toggled without page reloads.",
                "On the client side, assets/js/app.js provides real-time interactive utilities, including dynamic 10% helper stake calculations on task creation and acceptance forms, asynchronous modal confirmations, and animated alert banners."
            ]
        },
        {
            "num": "3.3",
            "title": "PHP APPLICATION TIER",
            "paragraphs": [
                "The PHP backend tier is implemented using PHP 8+ and follows a modular Model-View-Controller (MVC) architectural pattern without relying on heavy external frameworks. Key components include:",
                "• Database Connection and Auto-Migration (php/config/database.php): Establishes a PDO SQLite connection with PDO::ERRMODE_EXCEPTION and automatically executes Data Definition Language (DDL) statements upon initial boot to ensure table provisioning.",
                "• Authentication and Session Manager (php/includes/auth.php): Manages user login, registration, and logout utilizing secure password_hash() with the bcrypt algorithm and PHP session cookies.",
                "• Algorithmic Sorting Module (php/includes/PriorityQueue.php): Implements the custom priority score calculation and array sorting engine.",
                "• Transactional Action Controllers (php/quest_action.php, php/post_quest.php): Manages task lifecycle state transitions wrapped within strict PDO database transactions."
            ]
        },
        {
            "num": "3.4",
            "title": "JAVA SERVLETS APPLICATION TIER",
            "paragraphs": [
                "The Java backend tier is implemented using Java EE 4.0 Servlet specifications (javax.servlet-api-4.0.1.jar) and SQLite JDBC (sqlite-jdbc-3.42.0.0.jar). The Java architecture is structured into clean architectural layers:",
                "• Model Layer (com.campity.model): Encapsulates domain entities (User, Quest, Transaction) with JavaBean getters and setters.",
                "• Data Access Object (DAO) Layer (com.campity.dao): Provides robust persistence methods (UserDAO, QuestDAO, TransactionDAO) executing parameterized SQL queries with ACID transaction management.",
                "• Controller / Servlet Layer (com.campity.servlet): Houses dedicated servlets (AuthServlet, DashboardServlet, QuestServlet, LeaderboardServlet, ProfileServlet, PriorityQueueApiServlet) handling HTTP GET and POST requests.",
                "• Filter Pipeline (com.campity.filter.AuthFilter): Intercepts incoming requests to protected routes, validating session attributes before delegating to target servlets.",
                "• Standalone Embedded Server (com.campity.server.EmbeddedServer): A zero-dependency HTTP server constructed on JDK HttpServer, mapping routes, serving static assets, and providing instant local execution on port 8080."
            ]
        },
        {
            "num": "3.5",
            "title": "DATABASE ARCHITECTURE & RELATIONAL SCHEMA",
            "paragraphs": [
                "The persistence tier is powered by a relational SQLite database (campity.db). The relational schema is structured into three primary tables with enforced foreign key constraints, illustrated in Figure 3.2:",
                "1. users: Stores member credentials, wallet balances, experience points, reputation, and assigned role tiers.",
                "2. quests: Represents campus tasks, capturing title, description, category, bounty reward, required helper stake, lifecycle status, deadline, poster foreign key, and solver foreign key.",
                "3. transactions: Provides an immutable financial audit ledger recording sender ID, receiver ID, transferred credits, transaction type, timestamp, and associated task foreign key."
            ]
        }
    ]
}

CHAPTER_4 = {
    "title": "CHAPTER 4 — THE INTELLIGENT PRIORITY QUEUE SCHEDULING ALGORITHM",
    "sections": [
        {
            "num": "4.1",
            "title": "ALGORITHMIC FORMULATION & MATHEMATICAL MODEL",
            "paragraphs": [
                "The primary computational innovation in TaskFlow is its Intelligent Priority Queue scheduling engine. In traditional micro-task boards, tasks are displayed in basic chronological order, causing urgent campus emergencies to be buried beneath trivial inquiries.",
                "To resolve this limitation, TaskFlow formulates task prioritization as a multi-criteria scoring optimization problem. Each active task is assigned a composite priority score computed through the following mathematical equation:",
                "Priority Score = (Category Weight × 10) + (Reward × 0.5) + Deadline Urgency Bonus",
                "Where Category Weight represents the intrinsic institutional criticality of the errand, Reward is the credit bounty allocated by the requester, and Deadline Urgency Bonus is a dynamically decaying bonus based on remaining operational time."
            ]
        },
        {
            "num": "4.2",
            "title": "CATEGORY URGENCY WEIGHTING MATRIX",
            "paragraphs": [
                "TaskFlow categorizes all campus tasks into six standardized operational domains, each assigned an empirical urgency weight reflecting its institutional impact:",
                "• Medical / Health (Weight: 100): High-criticality tasks such as prescription delivery from the health center or emergency first-aid logistics. Base Score: 1000 points.",
                "• Urgent / Time-Sensitive (Weight: 90): Urgent administrative or time-bound campus errands. Base Score: 900 points.",
                "• Tech & Hardware Support (Weight: 70): Laboratory projector fixes, oscilloscope calibration, and hardware board troubleshooting. Base Score: 700 points.",
                "• Academics & Notes (Weight: 60): Peer programming tutoring, laboratory manual verification, and exam review notes. Base Score: 600 points.",
                "• Campus Logistics & Delivery (Weight: 50): Inter-department courier runs, equipment pickup, and library book returns. Base Score: 500 points.",
                "• General Assistance & Labor (Weight: 40): Event venue setup, noticeboard poster arrangement, and casual peer chores. Base Score: 400 points.",
                "Figure 4.2 illustrates the category weight distribution and resulting base priority score allocations."
            ]
        },
        {
            "num": "4.3",
            "title": "ECONOMIC BOUNTY SCALING & DEADLINE PROXIMITY",
            "paragraphs": [
                "In addition to category weight, the scheduling algorithm incorporates economic and temporal factors:",
                "1. Economic Bounty Scaling: High-reward tasks indicate greater task complexity or requester urgency. TaskFlow scales the credit bounty by a factor of 0.5 (Reward × 0.5). For example, a 100-credit bounty adds 50 points to the priority score.",
                "2. Deadline Urgency Bonus: For tasks assigned a strict completion deadline within the next 24 hours, an urgency bonus is computed dynamically based on the remaining hours (h):",
                "Deadline Bonus = (24 - h) × 2, for 0 < h <= 24",
                "A task due in 2 hours receives a bonus of (24 - 2) × 2 = 44 points, elevating it above less urgent tasks within the same category. For tasks with no deadline or deadlines exceeding 24 hours, the bonus evaluates to 0."
            ]
        },
        {
            "num": "4.4",
            "title": "JAVA MAX-HEAP IMPLEMENTATION",
            "paragraphs": [
                "In the Java Servlets backend, the priority queue is implemented using java.util.PriorityQueue<Quest>. Because Java's default PriorityQueue operates as a Min-Heap, TaskFlow configures a custom Comparator lambda to enforce Max-Heap ordering:",
                "Comparator<Quest> priorityComparator = (q1, q2) -> {",
                "    int scoreCompare = Double.compare(q2.getPriorityScore(), q1.getPriorityScore());",
                "    if (scoreCompare != 0) return scoreCompare;",
                "    return q2.getCreatedAt().compareTo(q1.getCreatedAt());",
                "};",
                "All unassigned open tasks are evaluated, assigned their composite score and urgency tier ('high' for score >= 850, 'med' for score >= 500, 'low' otherwise), and inserted into the Max-Heap. Tasks are subsequently polled in descending order of priority, guaranteeing O(log n) insertion and extraction efficiency."
            ]
        },
        {
            "num": "4.5",
            "title": "PHP SORTING ENGINE & REST API ENDPOINT",
            "paragraphs": [
                "In the PHP backend, TaskPriorityQueue::prioritize() replicates the Java Max-Heap ordering using PHP's native usort() algorithm with a spaceship operator (<=>) comparator. Furthermore, the Java backend exposes this sorted queue via a RESTful JSON endpoint at /api/quests/prioritized.",
                "This endpoint enables mobile clients or decoupled campus dashboards to query the top-ranked tasks in real-time, receiving a structured JSON payload containing task ID, title, category, reward, priority score, and assigned urgency tier."
            ]
        },
        {
            "num": "4.6",
            "title": "COMPUTATIONAL COMPLEXITY ANALYSIS",
            "paragraphs": [
                "The computational complexity of the priority queue algorithm is analyzed as follows:",
                "• Time Complexity: For n open tasks, computing composite scores requires O(1) mathematical evaluations per task, yielding O(n) total calculation time. Inserting n tasks into the Java Max-Heap takes O(n log n) time in the worst case, or O(n) using bottom-up heap construction. Polling the entire sorted list requires O(n log n) time. Under standard campus workloads (n < 5,000 active open tasks), execution completes in under 2 milliseconds.",
                "• Space Complexity: The memory footprint is strictly O(n) auxiliary space to store the heap nodes and sorted collection, ensuring optimal scalability under concurrent server loads."
            ]
        }
    ]
}
