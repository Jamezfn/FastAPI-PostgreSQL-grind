# FastAPI PostgreSQL Grind

A comprehensive collection of projects designed to master PostgreSQL database design and FastAPI integration through progressive, hands-on development.

## Overview

This repository contains 12 projects that systematically build your database design and API development skills. Each project introduces new concepts and increases in complexity, covering real-world application patterns from simple CRUD operations to complex multi-tenant systems.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Basic understanding of SQL queries
- Familiarity with FastAPI fundamentals

## Getting Started

Each project is self-contained in its own directory with dedicated setup instructions, database migrations, and API endpoints.
```bash
# Clone the repository
git clone https://github.com/jamezfn/FastAPI-PostgreSQL-grind.git
cd FastAPI-PostgreSQL-grind
```

## Projects

### Project 1: Todo API
**Core Concepts**: Single table design, CRUD operations, timestamps

A minimal task management API introducing fundamental database operations and RESTful endpoint design.

**Key Learning**:
- Table structure and primary keys
- Basic INSERT, SELECT, UPDATE, DELETE operations
- Auto-generated timestamps

---

### Project 2: Blog API
**Core Concepts**: Table relationships, foreign keys, JOINs

A blogging platform with user authentication and post management.

**Key Learning**:
- One-to-many relationships
- JOIN queries across tables
- User authentication patterns
- Cascading deletes

---

### Project 3: Expense Tracker
**Core Concepts**: Multiple relationships, aggregations, filtering

A personal finance tracker with categorized expenses.

**Key Learning**:
- Three-table relationships
- Aggregate functions (SUM, COUNT, AVG)
- GROUP BY and date-based filtering
- Financial data handling

---

### Project 4: E-commerce Product Catalog
**Core Concepts**: Many-to-many relationships, junction tables, search

A product catalog system with categories, tags, and reviews.

**Key Learning**:
- Junction tables for many-to-many relationships
- Full-text search capabilities
- Hierarchical category structures
- Rating and review systems

---

### Project 5: Social Media Clone
**Core Concepts**: Self-referential relationships, activity feeds

A mini social network with posts, comments, likes, and follows.

**Key Learning**:
- Self-joins (users following users)
- Nested comment threads
- Activity feed generation
- Like/unlike patterns
- Notification systems

---

### Project 6: Booking System
**Core Concepts**: Constraints, validations, conflict prevention

An appointment booking system with availability management.

**Key Learning**:
- CHECK and UNIQUE constraints
- Time-based queries and scheduling
- Preventing double-bookings
- Status state management
- Payment tracking

---

### Project 7: Multi-tenant SaaS Application
**Core Concepts**: Data isolation, indexing, query optimization

A workspace-based application with organizational hierarchy.

**Key Learning**:
- Tenant isolation strategies
- Index optimization for performance
- Organization → Team → User hierarchy
- Resource access control
- Query performance tuning

---

### Project 8: Real-time Chat Application
**Core Concepts**: Triggers, materialized views, real-time features

A messaging platform with direct and group conversations.

**Key Learning**:
- Database triggers
- Stored procedures
- LISTEN/NOTIFY for real-time updates
- Message pagination strategies
- Read receipt tracking
- Unread message counts with materialized views

---

### Project 9: Analytics Dashboard
**Core Concepts**: Time-series data, partitioning, window functions

An event tracking and analytics system.

**Key Learning**:
- Table partitioning strategies
- Window functions for analytics
- Common Table Expressions (CTEs)
- Date truncation and time bucketing
- Performance optimization for large datasets

---

### Project 10: Content Management System
**Core Concepts**: Polymorphic associations, JSON fields, versioning

A flexible CMS with multiple content types and revision history.

**Key Learning**:
- JSONB field usage and indexing
- GIN and GiST indexes
- Content versioning patterns
- Soft deletes and archiving
- Polymorphic table design

---

### Project 11: Job Queue System
**Core Concepts**: Concurrency, locks, transaction management

A background job processing system built on PostgreSQL.

**Key Learning**:
- Advisory locks
- FOR UPDATE SKIP LOCKED
- Queue implementation patterns
- Worker management
- Job scheduling and retries
- Transaction isolation levels

---

### Project 12: Marketplace Platform
**Core Concepts**: Full-stack integration, comprehensive system design

A complete marketplace with users, products, orders, payments, and messaging.

**Key Learning**:
- Complex multi-table schema design
- Search optimization
- Payment workflow management
- Review and rating systems
- Message threading
- Notification architecture
- Database migrations at scale
- Backup and restore strategies

---

## Technical Stack

- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Advanced relational database
- **SQLAlchemy**: ORM and query builder
- **Alembic**: Database migration tool
- **Pydantic**: Data validation
- **asyncpg/psycopg2**: PostgreSQL drivers

## Learning Path

Each project is designed to be completed sequentially. The concepts introduced in earlier projects are prerequisites for later ones. 

**Recommended approach**:
1. Complete each project fully before moving to the next
2. Implement all CRUD endpoints
3. Write database migrations
4. Add appropriate indexes
5. Test query performance
6. Document your schema decisions

## Key Concepts Covered

- **Database Design**: Normalization, relationships, constraints
- **Query Optimization**: Indexes, EXPLAIN ANALYZE, query planning
- **Data Integrity**: Foreign keys, constraints, transactions
- **Scalability**: Connection pooling, partitioning, caching strategies
- **Security**: SQL injection prevention, data validation, access control
- **Performance**: Indexing strategies, query optimization, connection management
- **Migrations**: Schema versioning, rollback strategies
- **Testing**: Database fixtures, test isolation, data seeding

## Contributing

Contributions are welcome! Please feel free to submit pull requests with improvements, additional projects, or documentation enhancements.

## License

MIT License - feel free to use these projects for learning and development.

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)