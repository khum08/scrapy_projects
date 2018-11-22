/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50527
Source Host           : localhost:3306
Source Database       : subsidy

Target Server Type    : MYSQL
Target Server Version : 50527
File Encoding         : 65001

Date: 2018-08-21 21:57:31
*/

SET FOREIGN_KEY_CHECKS=0;

CREATE DATABASE IF NOT EXISTS `subsidy`;

-- ----------------------------
-- Table structure for subsidy
-- ----------------------------
DROP TABLE IF EXISTS `subsidy`;
CREATE TABLE `subsidy` (
  `id_card` varchar(30) NOT NULL COMMENT '身份证',
  `name` varchar(15) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL COMMENT '0/公示；1/其他',
  PRIMARY KEY (`id_card`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of subsidy
-- ----------------------------
