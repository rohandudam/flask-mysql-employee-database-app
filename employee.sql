-- create a database with name employee_data
CREATE DATABASE IF NOT EXISTS `employee_data`;

use `employee_data`;

-- create a table with name employee
CREATE TABLE IF NOT EXISTS `employee` (
         id    		  	INT UNSIGNED  NOT NULL AUTO_INCREMENT,
         email		  	VARCHAR(100)   NOT NULL DEFAULT '',
         name         	VARCHAR(30)   NOT NULL DEFAULT '',
         department_id	INT UNSIGNED  NOT NULL DEFAULT 0,
         PRIMARY KEY  (id)
       );

-- create a table with name department
CREATE TABLE IF NOT EXISTS department (
         id    INT UNSIGNED  NOT NULL AUTO_INCREMENT,
         name         VARCHAR(30)   NOT NULL DEFAULT '',
         PRIMARY KEY  (id)
       );

-- add entries to department table
INSERT INTO department (name) VALUES ('HR'), ('ENG');