-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 28, 2017 at 03:22 PM
-- Server version: 5.5.55-0+deb8u1
-- PHP Version: 5.6.30-0+deb8u1
SET
  SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET
  time_zone = "+00:00";
  /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
  /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
  /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
  /*!40101 SET NAMES utf8 */;
--
  -- Database: `pi-access`
  --
  -- --------------------------------------------------------
  --
  -- Table structure for table `access_list`
  --
  CREATE TABLE IF NOT EXISTS `access_list` (
    `user_id` int(11) NOT NULL,
    `name` varchar(100) NOT NULL,
    `card_key` varchar(36) NOT NULL,
    `card_id` varchar(20) NOT NULL,
    `access` tinyint(1) DEFAULT 0,
    `admin` tinyint(1) DEFAULT 0
  ) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = latin1;
-- --------------------------------------------------------
  --
  -- Table structure for table `access_log`
  --
  CREATE TABLE IF NOT EXISTS `access_log` (
    `access_id` int(11) NOT NULL,
    `card_key_presented` varchar(36) DEFAULT NULL,
    `card_key_presented_datetime` datetime DEFAULT NULL,
    `card_id_presented` varchar(20) DEFAULT NULL,
    `access_granted` tinyint(1) DEFAULT NULL,
    `name_presented` varchar(20) DEFAULT NULL
  ) ENGINE = InnoDB AUTO_INCREMENT = 116 DEFAULT CHARSET = latin1;
--
  -- Indexes for dumped tables
  --
  --
  -- Indexes for table `access_list`
  --
ALTER TABLE `access_list`
ADD
  PRIMARY KEY (`user_id`),
ADD
  UNIQUE KEY `card_key` (`card_key`);
--
  -- Indexes for table `access_log`
  --
ALTER TABLE `access_log`
ADD
  PRIMARY KEY (`access_id`);
ALTER TABLE `access_list`
MODIFY
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 3;
--
  -- AUTO_INCREMENT for table `access_log`
  --
ALTER TABLE `access_log`
MODIFY
  `access_id` int(11) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 116;
  /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
  /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
  /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;