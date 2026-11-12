# Database Schema

The platform uses PostgreSQL. Below is the normalized schema managed by SQLAlchemy and Alembic.

## Tables

### 1. `users`
- `id` (PK)
- `username` (Unique, Indexed)
- `email` (Unique, Indexed)
- `hashed_password`
- `is_active` (Boolean)
- `role_id` (FK to `roles.id`)

### 2. `roles`
- `id` (PK)
- `name` (Unique: Admin, Moderator, Contestant)

### 3. `problems`
- `id` (PK)
- `title`, `description`, `input_spec`, `output_spec`, `constraints`
- `difficulty` (Enum: Easy, Medium, Hard, Expert)
- `category` (Enum: Arrays, Strings, DP, etc.)
- `is_published` (Boolean)

### 4. `test_cases`
- `id` (PK)
- `problem_id` (FK to `problems.id`)
- `input_data`, `expected_output`
- `is_sample` (Boolean)

### 5. `submissions`
- `id` (PK)
- `user_id` (FK), `problem_id` (FK)
- `language` (Enum: C++, Python, Java)
- `code` (Text)
- `status` (Enum: Accepted, Wrong Answer, TLE, MLE, etc.)
- `execution_time` (Float)

### 6. `contests`
- `id` (PK)
- `title`, `description`, `start_time`, `end_time`

### 7. `contest_problems` & `contest_participants`
- Many-to-Many association tables connecting contests to problems and users.
