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
("Customer Service Officer", 1, "Tasked to answer calls professionally to provide information about products and services, take/ cancel orders, or obtain details of complaints. Keep records of customer interactions and transactions, recording details of inquiries, complaints, and comments, as well as actions are taken."),
("Operations Coordinator", 2, "Responsible for ensuring that all departments are running smoothly. They plan purchases, negotiate contracts and coordinate budgeting to make sure business continues as usual with minimal downtime or interruption from one department's workflow."),
("HR Manager", 3, "Lead and direct the routine functions of the Human Resources (HR) department including hiring and interviewing staff, administering pay, benefits, and leave, and enforcing company policies and practices."),
("Sales Rep", 4, "Responsible for selling products and meeting customer needs while obtaining orders from existing or potential sales outlets. They ensure that the customer is satisfied and adequately taken care of while making a purchase."),
("Sales Manager", 5, "Responsible for leading sales teams to reach sales targets. Sales managers are primarily tasked with hiring and training team members, setting quotas, evaluating and adjusting performance, and developing processes that drive sales."),
("Roving Service Engineer", 6, "Provides technical and maintenance support to the operating units including rotating and reciprocating equipment."),
("Repair Engineer", 7, "Works with engineering and other departments to establish the materials, processes and specifications needed for fabrication, rework and repairs."),
("Operations Manager", 8, "Oversee operational activities at every level of an organization. Their duties include hiring and training employees and managing quality assurance programs."),
("Accountant", 9, "Helps businesses make critical financial decisions by collecting, tracking, and correcting the company's finances. They are responsible for financial audits, reconciling bank statements, and ensuring financial records are accurate throughout the year."),
("Finance Manager", 10, "Responsible for the overall financial health of an organization. Working in many different industries, they produce financial reports, direct investment activities, and develop strategies and plans for the long-term financial goals of their organization.");

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
-- Dumping data for table `Skill`
--

INSERT INTO `skill` (`skill_name`, `skill_code`, `skill_desc`) VALUES
("Analytical Skills", 1, "Ability to deconstruct information into smaller categories in order to draw conclusions. Analytical skill consists of categories that include logical reasoning, critical thinking, communication, research, data analysis and creativity."),
("Communication Skills", 2, "Abilities to pass, receive and process information. Communication skills help you build relationships, share ideas and information and play your role in the workplace effectively."),
("Management Skills", 3, "Management is a process of planning, decision making, organizing, leading, motivation and controlling the human resources, financial, physical, and information resources of an organization to reach its goals efficiently and effectively."),
("Data Handling", 4, "The ability to use data effectively to improve your programs, including looking at lists and summaries, looking for patterns, analyzing results, and making presentations to others."),
("Presentation Skills", 5, "Skills you need in delivering effective and engaging presentations to a variety of audiences. These skills cover a variety of areas such as the structure of your presentation, the design of your slides, the tone of your voice and the body language you convey."),
("Accounting Skills", 6, "Abilities that allow you to accurately and ethically manage financial transactions, analyze financial data and generate financial reports. They include hard skills such as understanding generally accepted accounting principles, mathematical comprehension and data analysis."),
("Leadership Skills", 7, "Strengths and abilities individuals demonstrate that help to oversee processes, guide initiatives and steer their employees toward the achievement of goals"),
("Training Skills", 8, " An employer-provided program that teaches or develops proficiencies for the workplace. The aim of skills training is to equip employees with the knowledge and attributes necessary to carry out their duties at the optimal level."),
("Digital Literacy Skills", 9, "An individual's ability to find, evaluate, and communicate information through typing and other media on various digital platforms."),
("Marketing Skills", 10, "Able to identify customers' problems, sometimes before they do, and find a way of addressing those needs and problems through the products and services that you provide."),
("Hardware Management Skills", 11, "Knowledge and expertise to be able to operate  and maintain particular electronic devices."),
("Software Management Skills", 12, "Abilities that show how well you can use a specific type of computer program."),
("Cybersecurity Skills", 13, "A variety of skills such as troubleshooting, maintaining, and updating information security systems; implementing continuous network monitoring; and providing real-time security solutions."),
("Global Awareness", 14, "A capacity that incorporates the attitudes, knowledge, and skills necessary for a person to competently and perceptively navigate the challenges and opportunities of a globalized world in a way that promotes the greater good.");


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
(1,	2),
(1,	7),
(2,	9), 
(2,	8), 
(3,	10), 
(3,	8), 
(3,	3), 
(4,	12), 
(4,	9), 
(4,	2), 
(5,	6), 
(5,	9), 
(5,	4),
(5,	3), 
(6,	4), 
(6,	14), 
(6,	10), 
(7,	7), 
(7,	3), 
(7,	9), 
(8,	3), 
(9,	9);


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
('COR001',	2),
('COR002', 3), 
('COR002',	2), 
('COR004',	2), 
('COR006',	2), 
('COR006',	12), 
('FIN001',	9), 
('FIN001',	10), 
('FIN002',	9), 
('FIN003',	7), 
('FIN003',	8), 
('HRD001',	8), 
('MGT001',	6), 
('MGT002',	14), 
('COR001',	3), 
('COR002',	9), 
('COR004',	4), 
('COR006',	4);


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
(1,	'COR001',	1), 
(1,	'FIN001',	1), 
(2,	'FIN002',	2), 
(2,	'HRD001',	2), 
(3,	'COR002',	3), 
(3,	'HRD001',	3), 
(3,	'FIN001',	3), 
(4,	'COR001',	4), 
(4,	'FIN002',	4), 
(5,	'MGT001',	5), 
(5,	'FIN002',	5), 
(5,	'COR002',	5), 
(6,	'MGT002',	6), 
(6,	'FIN001',	6);


--
-- Table structure for table `RoleSkillCourseRelation`
--

CREATE TABLE `role_skill_course_relation` (
  `role_code` INT(11) NOT NULL,
  `skill_code` INT(11) NOT NULL,
  `course_code` VARCHAR(200) NOT NULL,
  FOREIGN KEY (`role_code`) REFERENCES `Role` (`role_code`),
  FOREIGN KEY (`skill_code`) REFERENCES `Skill` (`skill_code`),
  FOREIGN KEY (`course_code`) REFERENCES `Course` (`course_code`),
  UNIQUE (`role_code`, `skill_code`, `course_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `RoleSkillCourseRelation`
--

INSERT INTO `role_skill_course_relation` (`role_code`, `skill_code`,`course_code`) VALUES
(1, 2, 'COR001'),
(1, 7, 'FIN003'),
(2, 9, 'COR002'),
(2, 8, 'HRD001'),
(3, 10, 'FIN001'),
(3,	8, 'HRD001'), 
(3,	3, 'COR001'), 
(4,	12, 'COR006'), 
(4,	9, 'FIN002'), 
(4,	2, 'COR001'), 
(5,	6, 'MGT001'), 
(5,	9, 'FIN002'), 
(5,	4, 'COR004'), 
(5,	3, 'COR002'), 
(6,	4, 'COR004'), 
(6,	14, 'MGT002'),
(6,	10, 'FIN001'), 
(7,	7, 'FIN003'), 
(7,	3, 'COR002'), 
(7,	9, 'FIN001'), 
(8,	3, 'COR001'), 
(9,	9, 'FIN002')



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