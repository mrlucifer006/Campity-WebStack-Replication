# Complete text content and data for TaskFlow Project Report

ABSTRACT_TEXT = [
    "In contemporary higher education ecosystems, university students and faculty encounter numerous routine, time-sensitive micro-tasks—ranging from urgently delivering hardware components between specialized laboratories and securing reference books from campus libraries to peer-to-peer programming tutoring and immediate technical troubleshooting. Despite the high density of capable peers willing to assist, traditional informal communication channels such as group chats, bulletin boards, and social media groups frequently fail due to the total absence of systematic task prioritization, high helper abandonment rates, unverified delivery, and the lack of financial guarantees.",
    "This project presents TaskFlow: a decentralized, priority-driven campus task management and posting system engineered to solve campus micro-task coordination friction. TaskFlow was designed and developed through an architectural benchmark and replication study of Campity, a mid-level web application characterized by non-trivial relational transactions and dynamic scheduling. In accordance with rigorous software engineering principles, TaskFlow implements a dual-stack web architecture offering two independent, production-grade backends: a modern PHP 8+ engine utilizing PDO SQLite and an enterprise Java EE 4.0 Servlet architecture utilizing ACID JDBC Data Access Objects (DAOs) and a standalone embedded JDK HTTP server.",
    "The core algorithmic contribution of TaskFlow is an Intelligent Priority Queue scheduling engine that dynamically computes composite urgency scores for all open campus errands based on three multi-dimensional parameters: category criticality weight (Medical: 100, Urgent: 90, Tech Support: 70, Academics: 60, Logistics: 50, Labor: 40), economic reward value, and proximity to deadline. Tasks are structured and dispatched in a Max-Heap priority order, guaranteeing that high-impact and critical university errands receive immediate attention over casual requests.",
    "To resolve counterparty risk and eliminate helper dropout, TaskFlow introduces an atomic two-way financial escrow protocol. When a task is posted, 100% of the reward credits are placed into escrow. To accept a task, a helper must lock a mandatory 10% accountability stake from their wallet. Upon task delivery and requester verification, the escrowed bounty and the helper's stake are atomically released alongside gamified Experience Points (XP) and peer trust ratings. Comprehensive empirical evaluation demonstrates that TaskFlow achieves zero database concurrency locks under concurrent transactions, sub-millisecond API response latency in Java (0.65 ms) and 3.2 ms in PHP, and provides an intuitive, responsive glassmorphic user interface adaptable across multiple campus operational themes."
]

ABBREVIATIONS = [
    ("ACID", "Atomicity, Consistency, Isolation, Durability"),
    ("API", "Application Programming Interface"),
    ("Bcrypt", "Blowfish-based Cryptographic Key Derivation Function"),
    ("CSS", "Cascading Style Sheets"),
    ("DAO", "Data Access Object Pattern"),
    ("FSM", "Finite State Machine"),
    ("GUI", "Graphical User Interface"),
    ("HTML", "HyperText Markup Language"),
    ("HTTP", "HyperText Transfer Protocol"),
    ("JAR", "Java Archive"),
    ("JDBC", "Java Database Connectivity"),
    ("JDK", "Java Development Kit"),
    ("JSON", "JavaScript Object Notation"),
    ("JSP", "JavaServer Pages"),
    ("JVM", "Java Virtual Machine"),
    ("MVC", "Model-View-Controller"),
    ("ORM", "Object-Relational Mapping"),
    ("PDO", "PHP Data Objects"),
    ("RBAC", "Role-Based Access Control"),
    ("REST", "Representational State Transfer"),
    ("RPS", "Requests Per Second"),
    ("SQL", "Structured Query Language"),
    ("UI / UX", "User Interface / User Experience"),
    ("WAL", "Write-Ahead Logging"),
    ("WAR", "Web Application Archive"),
    ("XP", "Experience Points")
]

FIGURES_LIST = [
    ("3.1", "TaskFlow Dual-Stack System Architecture", "6"),
    ("3.2", "TaskFlow Relational Entity-Relationship (ER) Schema", "9"),
    ("4.1", "Intelligent Priority Queue Scheduling Pipeline", "11"),
    ("4.2", "Task Urgency Category Weighting & Point Allocation Matrix", "13"),
    ("5.1", "Task Lifecycle & Financial Escrow Finite State Machine", "17"),
    ("6.1", "Java Standalone EmbeddedServer & Verification Suite Output", "24"),
    ("7.1", "Performance Benchmarking: Throughput & Latency Comparison", "28"),
    ("7.2", "TaskFlow Modern SaaS Dashboard User Interface Layout", "30")
]
