create database studentmanagementsystem

Use studentmanagementsystem

  CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

  
  CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    grade VARCHAR(10) NOT NULL,
    contact_number VARCHAR(10) NOT NULL
);

SELECT * FROM studentmanagementsystem.users;
SELECT * FROM studentmanagementsystem.students;

