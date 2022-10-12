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

CREATE TABLE `role` (
  `role_name` varchar(100) NOT NULL ,
  `role_code` INT(11) NOT NULL,
  `role_desc` varchar(200) NOT NULL,
  PRIMARY KEY (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Role`
--

INSERT INTO `role` (`role_name`, `role_code`, `role_desc`) VALUES
("Professor", 1, "Respect"),
("Banker", 2, "Good pay"),
("Developer", 3, "Enjoy it");

-- --------------------------------------------------------

--
-- Table structure for table `Skill`
--

CREATE TABLE `skill` (
  `skill_name` varchar(100) NOT NULL,
  `skill_code` INT(11) NOT NULL,
  `skill_desc` varchar(200) NOT NULL,
  PRIMARY KEY (`skill_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `doctor`
--

INSERT INTO `skill` (`skill_name`, `skill_code`, `skill_desc`) VALUES
("Leadership", 1, "good Leadership"),
("Programming", 2, "good Programming"),
("Data Modeling", 3, "good Modeling");

--
-- Table structure for table `RoleSkillRelation`
--

CREATE TABLE `role_skill_relation` (
  `role_code` INT(11) NOT NULL ,
  `skill_code` INT(11) NOT NULL ,

  FOREIGN KEY (`role_code`) REFERENCES `Role` (`role_code`),
  FOREIGN KEY (`skill_code`) REFERENCES `Skill` (`skill_code`),
  UNIQUE (`role_code`, `skill_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `RoleSkillRelation`
--

INSERT INTO `role_skill_relation` (`role_code`, `skill_code`) VALUES
(1, 1),
(2, 2),
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `Course`
--

CREATE TABLE `course` (
  `course_name` varchar(100) NOT NULL,
  `course_code` varchar(100) NOT NULL,
  `course_desc` varchar(200) NOT NULL,
  `course_status` varchar(200) NOT NULL,
  PRIMARY KEY (`course_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Course`
--

INSERT INTO `course` (`course_name`, `course_code`, `course_desc`, `course_status`) VALUES
("Systems Thinking and Design", "COR001", "good Design", 'active'),
("Lean Six Sigma Green Belt Certification", "COR002", " Apply Lean Six Sigma methodology and statistical tools such as Minitab to be used in process analytics", 'active'),
("Service Excellence", "COR004", "The programme provides the learner with the key foundations of what builds customer confidence in the service industry", 'pending'),
("Manage Change", "COR006", "Identify risks associated with change and develop risk mitigation plans.", 'retired'),
("Data Collection and Analysis", "FIN001", "Data is meaningless unless insights and analysis can be drawn to provide useful information for business decision-making. It is imperative that data quality, integrity and security", 'active'),
("Risk and Compliance Reporting", "FIN002", "Regulatory reporting is a requirement for businesses from highly regulated sectors to demonstrate compliance with the necessary regulatory provisions.", 'active'),
("Business Continuity Planning", "FIN003", "Business continuity planning is essential in any business to minimise loss when faced with potential threats and disruptions.", 'retired'),
("Leading and Shaping a Culture in Learning", "HRD001", "This training programme, delivered by the National Centre of Excellence (Workplace Learning), aims to equip participants with the skills and knowledge of the National workplace learning certification framework,", 'active'),
("People Management", "MGT001", "enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.", 'active'),
("Workplace Conflict Management for Professionals", "MGT002", "This course will address the gaps to build consensus and utilise knowledge of conflict management techniques to diffuse tensions and achieve resolutions effectively in the best interests of the organisation.", 'active');

--
-- Table structure for table `SkillCourseRelation`
--

CREATE TABLE `skill_course_relation` (
  `course_code` varchar(200) NOT NULL ,
  `skill_code` INT(11) NOT NULL ,

  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  FOREIGN KEY (`skill_code`) REFERENCES `Skill` (`skill_code`),
  UNIQUE (`course_code`, `skill_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `SkillCourseRelation`
--

INSERT INTO `skill_course_relation` (`course_code`, `skill_code`) VALUES
('COR001', 1),
('COR002', 2),
('COR004', 3);

--
-- Table structure for table `LearningJourney`
--

CREATE TABLE `learning_journey` (
  `lj_id` INT(11) NOT NULL,
  `course_code` varchar(200) NOT NULL,
  `role_code` INT(11) NOT NULL,
  FOREIGN KEY (`role_code`) REFERENCES `Role` (`role_code`),
  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  UNIQUE (`lj_id`, `course_code`, `role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `LearningJourney`
--

INSERT INTO `learning_journey` (`lj_id`, `course_code`, `role_code`) VALUES
(1, 'COR001', 1),
(2, 'COR002', 2),
(3, 'COR002', 2),
(3, 'COR004', 2),
(3, 'COR006', 2);

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