-- Set options
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Drop and create schema
DROP SCHEMA IF EXISTS `opendata`;
CREATE SCHEMA IF NOT EXISTS `opendata` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `opendata`;

-- Table: role
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `role_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE INDEX `name_UNIQUE` (`name`)
) ENGINE=InnoDB;

-- Table: category
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `parent_category_id` INT DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE INDEX `name_UNIQUE` (`name`),
  INDEX `parent_category_idx` (`parent_category_id`),
  CONSTRAINT `parent_category`
    FOREIGN KEY (`parent_category_id`)
    REFERENCES `category` (`category_id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Table: data
DROP TABLE IF EXISTS `data`;
CREATE TABLE `data` (
  `data_id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL,
  `description` LONGTEXT,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `content` VARCHAR(45) NOT NULL,
  `format` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`data_id`, `category_id`),
  UNIQUE INDEX `name_UNIQUE` (`name`),
  INDEX `fk_data_category_idx` (`category_id`),
  CONSTRAINT `fk_data_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `category` (`category_id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Table: user
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `login` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `email_UNIQUE` (`email`),
  UNIQUE INDEX `login_UNIQUE` (`login`)
) ENGINE=InnoDB;

-- Table: access
DROP TABLE IF EXISTS `access`;
CREATE TABLE `access` (
  `access_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `role_id` INT NOT NULL,
  `data_id` INT NOT NULL,
  PRIMARY KEY (`access_id`, `user_id`, `role_id`, `data_id`),
  INDEX `fk_Access_Data_idx` (`data_id`),
  INDEX `fk_Access_Role_idx` (`role_id`),
  INDEX `fk_Access_User_idx` (`user_id`),
  CONSTRAINT `fk_Access_Data`
    FOREIGN KEY (`data_id`)
    REFERENCES `data` (`data_id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Access_Role`
    FOREIGN KEY (`role_id`)
    REFERENCES `role` (`role_id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Access_User`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Table: tag
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `tag_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`tag_id`),
  UNIQUE INDEX `name_UNIQUE` (`name`)
) ENGINE=InnoDB;

-- Table: link
DROP TABLE IF EXISTS `link`;
CREATE TABLE `link` (
  `link_id` INT NOT NULL AUTO_INCREMENT,
  `data_id` INT NOT NULL,
  `tag_id` INT NOT NULL,
  PRIMARY KEY (`link_id`, `data_id`, `tag_id`),
  INDEX `fk_link_data_idx` (`data_id`),
  INDEX `fk_link_tag_idx` (`tag_id`),
  CONSTRAINT `fk_link_data`
    FOREIGN KEY (`data_id`)
    REFERENCES `data` (`data_id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_link_tag`
    FOREIGN KEY (`tag_id`)
    REFERENCES `tag` (`tag_id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Restore SQL settings
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Sample Data Insertion
-- -----------------------------------------------------

-- Data for role
START TRANSACTION;
INSERT INTO `role` (`name`) VALUES ('User'), ('Admin');
COMMIT;

-- Data for category
START TRANSACTION;
INSERT INTO `category` (`name`, `parent_category_id`) VALUES ('Informatics', NULL), ('Statistics', NULL);
COMMIT;

-- Data for data
START TRANSACTION;
INSERT INTO `data` (`category_id`, `description`, `createdAt`, `updatedAt`, `content`, `format`, `name`)
VALUES 
  (1, 'Important tasks', '2023-02-15 15:15:15', '2023-03-15 15:15:15', 'txt', 'txt', 'Informatics'),
  (2, 'Important statistics', '2024-04-18 13:17:09', '2024-04-19 13:17:09', 'xlsx', 'xlsx', 'Statistics');
COMMIT;

-- Data for user
START TRANSACTION;
INSERT INTO `user` (`firstname`, `password`, `lastname`, `email`, `login`)
VALUES 
  ('Vlad', '1234', 'Koleso', 'vald_koleso@gmail.com', 'vlad'),
  ('Daria', '5678', 'Minze', 'minze@gmail.com', 'minze');
COMMIT;

-- Data for access
START TRANSACTION;
INSERT INTO `access` (`user_id`, `role_id`, `data_id`)
VALUES 
  (1, 1, 1),
  (2, 2, 2);
COMMIT;

-- Data for tag
START TRANSACTION;
INSERT INTO `tag` (`name`) VALUES ('informatics'), ('statistics');
COMMIT;

-- Data for link
START TRANSACTION;
INSERT INTO `link` (`data_id`, `tag_id`)
VALUES 
  (1, 1),
  (2, 2);
COMMIT;
