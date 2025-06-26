CREATE TABLE users (
    id CHAR(36) PRIMARY KEY NOT NULL,
    created_by VARCHAR(50) NULL,
    updated_by VARCHAR(50) NULL,
    date_created DATETIME NOT NULL,
    date_updated DATETIME NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(500) NOT NULL,
    hash_salt VARCHAR(150) NOT NULL
);

CREATE TABLE students (
    id CHAR(36) PRIMARY KEY NOT NULL,
    created_by VARCHAR(50) NULL,
    updated_by VARCHAR(50) NULL,
    date_created DATETIME NOT NULL,
    date_updated DATETIME NULL,
    user_id CHAR(36) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    phone_number VARCHAR(100) NOT NULL,
    matric_number VARCHAR(50) NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE courses (
    id CHAR(36) PRIMARY KEY NOT NULL,
    created_by VARCHAR(50) NULL,
    updated_by VARCHAR(50) NULL,
    date_created DATETIME NOT NULL,
    date_updated DATETIME NULL,
    code VARCHAR(10) NOT NULL UNIQUE,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500) NULL
);

CREATE TABLE enrollments (
    id CHAR(36) PRIMARY KEY NOT NULL,
    created_by VARCHAR(50) NULL,
    updated_by VARCHAR(50) NULL,
    date_created DATETIME NOT NULL,
    date_updated DATETIME NULL,
    date_enrolled DATETIME NOT NULL,
    session_semester VARCHAR(100) NOT NULL,
    course_id CHAR(36) NOT NULL,
    student_id CHAR(36) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE RESTRICT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE RESTRICT
);

CREATE TABLE assessments (
    id CHAR(36) PRIMARY KEY NOT NULL,
    created_by VARCHAR(50) NULL,
    updated_by VARCHAR(50) NULL,
    date_created DATETIME NOT NULL,
    date_updated DATETIME NULL,
    score DECIMAL(5,2) NOT NULL,
    grade VARCHAR(10) NOT NULL,
    type VARCHAR(20) NOT NULL,
    enrollment_id CHAR(36) NOT NULL,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE RESTRICT
);
