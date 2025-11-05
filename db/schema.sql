CREATE DATABASE IF NOT EXISTS library_branch1;
USE library_branch1;

CREATE TABLE IF NOT EXISTS branches (
  branch_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  location VARCHAR(255),
  api_endpoint VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS books (
  book_id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255),
  genre VARCHAR(100),
  available BOOLEAN DEFAULT TRUE,
  branch_id INT NOT NULL,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE IF NOT EXISTS users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(150),
  email VARCHAR(150) UNIQUE,
  registered_branch INT NOT NULL,
  FOREIGN KEY (registered_branch) REFERENCES branches(branch_id)
);

CREATE TABLE IF NOT EXISTS loans (
  loan_id INT PRIMARY KEY AUTO_INCREMENT,
  book_id INT NOT NULL,
  user_id INT NOT NULL,
  issue_date DATE,
  due_date DATE,
  return_date DATE NULL,
  branch_id INT NOT NULL,
  status VARCHAR(20) DEFAULT 'borrowed',
  FOREIGN KEY (book_id) REFERENCES books(book_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);


CREATE DATABASE IF NOT EXISTS library_branch2;
USE library_branch2;

CREATE TABLE IF NOT EXISTS branches (
  branch_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  location VARCHAR(255),
  api_endpoint VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS books (
  book_id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255),
  genre VARCHAR(100),
  available BOOLEAN DEFAULT TRUE,
  branch_id INT NOT NULL,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE IF NOT EXISTS users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(150),
  email VARCHAR(150) UNIQUE,
  registered_branch INT NOT NULL,
  FOREIGN KEY (registered_branch) REFERENCES branches(branch_id)
);

CREATE TABLE IF NOT EXISTS loans (
  loan_id INT PRIMARY KEY AUTO_INCREMENT,
  book_id INT NOT NULL,
  user_id INT NOT NULL,
  issue_date DATE,
  due_date DATE,
  return_date DATE NULL,
  branch_id INT NOT NULL,
  status VARCHAR(20) DEFAULT 'borrowed',
  FOREIGN KEY (book_id) REFERENCES books(book_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);