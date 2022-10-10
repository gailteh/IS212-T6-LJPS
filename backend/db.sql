-- phpMyAdmin SQL Dump
-- version 4.9.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 27, 2021 at 08:33 AM
-- Server version: 5.7.26
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `is212_example`
--
CREATE DATABASE IF NOT EXISTS `is212_SPM` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `is212_SPM`;

-- --------------------------------------------------------

--
-- Table structure for table `Role`
--

CREATE TABLE `Role` (
  `role_name` varchar(100) NOT NULL ,
  `role_code` INT(11) NOT NULL,
  `role_desc` varchar(200) NOT NULL,
  PRIMARY KEY (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Role`
--

INSERT INTO `Role` (`role_name`, `role_code`, `role_desc`) VALUES
("Professor", 1, "Respect"),
("Banker", 2, "Good pay"),
("Developer", 3, "Enjoy it");

-- --------------------------------------------------------

--
-- Table structure for table `Skill`
--

CREATE TABLE `Skill` (
  `skill_name` varchar(100) NOT NULL,
  `skill_code` INT(11) NOT NULL,
  `skill_desc` varchar(200) NOT NULL,
  PRIMARY KEY (`skill_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `doctor`
--

INSERT INTO `Skill` (`skill_name`, `skill_code`, `skill_desc`) VALUES
("Leadership", 1, "good Leadership"),
("Programming", 2, "good Programming"),
("Data Modeling", 3, "good Modeling");

--
-- Table structure for table `RoleSkillRelation`
--

CREATE TABLE `RoleSkillRelation` (
  `role_code` INT(11) NOT NULL ,
  `skill_code` INT(11) NOT NULL ,

  FOREIGN KEY (`role_code`) REFERENCES `Role` (`role_code`),
  FOREIGN KEY (`skill_code`) REFERENCES `Skill` (`skill_code`),
  UNIQUE (`role_code`, `skill_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `RoleSkillRelation`
--

INSERT INTO `RoleSkillRelation` (`role_code`, `skill_code`) VALUES
(1, 1),
(2, 2),
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `Course`
--

CREATE TABLE `Course` (
  `course_name` varchar(100) NOT NULL,
  `course_code` INT(11) NOT NULL,
  `course_desc` varchar(200) NOT NULL,
  PRIMARY KEY (`course_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Course`
--

INSERT INTO `Course` (`course_name`, `course_code`, `course_desc`) VALUES
("Systems Thinking and Design", 1, "good Design"),
("Service Excellence", 2, "good Service"),
("Manage Change", 3, "good Change");

--
-- Table structure for table `SkillCourseRelation`
--

CREATE TABLE `SkillCourseRelation` (
  `course_code` INT(11) NOT NULL ,
  `skill_code` INT(11) NOT NULL ,

  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  FOREIGN KEY (`skill_code`) REFERENCES `Skill` (`skill_code`),
  UNIQUE (`course_code`, `skill_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `SkillCourseRelation`
--

INSERT INTO `SkillCourseRelation` (`course_code`, `skill_code`) VALUES
(1, 1),
(2, 2),
(3, 3);

--
-- Table structure for table `LearningJourney`
--

CREATE TABLE `LearningJourney` (
  `LearningJourney_id` INT(11) NOT NULL,
  `course_code` INT(11) NOT NULL ,
  `role_code` INT(11) NOT NULL,
  FOREIGN KEY (`role_code`) REFERENCES `Role` (`role_code`),
  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  UNIQUE (`LearningJourney_id`, `course_code`, `role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `LearningJourney`
--

INSERT INTO `LearningJourney` (`LearningJourney_id`, `course_code`, `role_code`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3);

-- --
-- -- Constraints for table `RoleSkillRelation`
-- --
-- ALTER TABLE `RoleSkillRelation`
--   ADD CONSTRAINT `role_code` FOREIGN KEY (`role_code`) REFERENCES `Role` (`role_code`),
--   ADD CONSTRAINT `skill_code` FOREIGN KEY (`skill_code`) REFERENCES `Skill` (`skill_code`);

-- --
-- -- Constraints for table `SkillCourseRelation`
-- --
-- ALTER TABLE `SkillCourseRelation`
--   ADD CONSTRAINT `skill_code` FOREIGN KEY (`skill_code`) REFERENCES `Skill` (`skill_code`),
--   ADD CONSTRAINT `course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`);

-- --
-- -- Constraints for table `RoleSkillCourseMapping`
-- --
-- ALTER TABLE `RoleSkillCourseMapping`
--   ADD CONSTRAINT `skill_code` FOREIGN KEY (`skill_code`) REFERENCES `Skill` (`skill_code`),
--   ADD CONSTRAINT `course_code` FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
--   ADD CONSTRAINT `role_code` FOREIGN KEY (`role_code`) REFERENCES `Role` (`role_code`);

-- --
-- -- Constraints for table `LearningJourney`
-- --
-- ALTER TABLE `LearningJourney`
--   ADD CONSTRAINT `skill_code` FOREIGN KEY (`skill_code`) REFERENCES `RoleSkillCourseMapping` (`skill_code`),
--   ADD CONSTRAINT `course_code` FOREIGN KEY (`course_code`) REFERENCES `RoleSkillCourseMapping` (`course_code`),
--   ADD CONSTRAINT `role_code` FOREIGN KEY (`role_code`) REFERENCES `RoleSkillCourseMapping` (`role_code`);