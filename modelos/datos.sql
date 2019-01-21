/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50721
Source Host           : localhost:3306
Source Database       : factura

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-11-21 08:11:25
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for caea
-- ----------------------------
DROP TABLE IF EXISTS `caea`;
CREATE TABLE `caea` (
  `idCAEA` int(11) NOT NULL AUTO_INCREMENT,
  `CAEA` varchar(14) COLLATE utf8_spanish_ci NOT NULL,
  `periodo` varchar(6) COLLATE utf8_spanish_ci NOT NULL,
  `orden` varchar(1) COLLATE utf8_spanish_ci NOT NULL,
  `fchvigdesde` date NOT NULL,
  `fchvighasta` date NOT NULL,
  `fchtopeinf` date NOT NULL,
  `fchproceso` datetime NOT NULL,
  `obs` text COLLATE utf8_spanish_ci NOT NULL,
  `empresa` int(11) NOT NULL,
  `ptovta` varchar(4) COLLATE utf8_spanish_ci NOT NULL,
  `estado` varchar(1) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`idCAEA`),
  KEY `caea_empresa` (`empresa`),
  CONSTRAINT `caea_ibfk_1` FOREIGN KEY (`empresa`) REFERENCES `empresas` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- ----------------------------
-- Records of caea
-- ----------------------------

-- ----------------------------
-- Table structure for cbterel
-- ----------------------------
DROP TABLE IF EXISTS `cbterel`;
CREATE TABLE `cbterel` (
  `idcbterel` int(11) NOT NULL AUTO_INCREMENT,
  `tipocbte` varchar(3) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `ptovta` varchar(4) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `nrocbte` varchar(8) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `nrelacion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idcbterel`),
  KEY `cbterel_nrelacion` (`nrelacion`),
  CONSTRAINT `cbterel_ibfk_1` FOREIGN KEY (`nrelacion`) REFERENCES `encabeza` (`ncontrol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- ----------------------------
-- Records of cbterel
-- ----------------------------

-- ----------------------------
-- Table structure for encabeza
-- ----------------------------
DROP TABLE IF EXISTS `encabeza`;
CREATE TABLE `encabeza` (
  `ncontrol` int(11) NOT NULL AUTO_INCREMENT,
  `fechacbte` date NOT NULL DEFAULT '0000-00-00',
  `tipocbte` varchar(3) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `puntovta` varchar(4) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `cbtenro` varchar(8) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `tipodoc` varchar(2) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `nrodoc` varchar(11) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `imptotal` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `imptotconc` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `impneto` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `impiva` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `imptrib` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `impopex` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `cae` varchar(14) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `vencecae` date NOT NULL DEFAULT '0000-00-00',
  `resultado` varchar(1) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `motivoobs` text COLLATE utf8_spanish_ci,
  `errcode` varchar(6) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `errmsg` varchar(250) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `transferido` bit(1) NOT NULL DEFAULT b'0',
  `empresa` int(11) NOT NULL DEFAULT '1',
  `concepto` varchar(1) COLLATE utf8_spanish_ci NOT NULL DEFAULT '1',
  `errorprog` text COLLATE utf8_spanish_ci,
  `listo` bit(1) NOT NULL DEFAULT b'0',
  `tipows` varchar(2) COLLATE utf8_spanish_ci NOT NULL DEFAULT 'WS',
  `nrelacion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ncontrol`),
  KEY `nrelacion` (`nrelacion`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- ----------------------------
-- Records of encabeza
-- ----------------------------
INSERT INTO `encabeza` VALUES ('17', '2018-11-20', '11', '1', '00000028', '96', '35129034', '100.0000', '0.0000', '100.0000', '0.0000', '0.0000', '0.0000', '68475697249841', '2018-11-30', 'A', '10048: El campo  \'Importe Total\' ImpTotal, debe ser igual  a la  suma de ImpNeto + ImpTrib. Donde ImpNeto es igual al Sub Total', '', '', '\0', '0', '2', '', '\0', 'WS', '2');

-- ----------------------------
-- Table structure for iva
-- ----------------------------
DROP TABLE IF EXISTS `iva`;
CREATE TABLE `iva` (
  `idiva` int(11) NOT NULL AUTO_INCREMENT,
  `ivaid` int(11) NOT NULL DEFAULT '1',
  `baseimp` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `importe` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `transferido` bit(1) NOT NULL DEFAULT b'0',
  `nrelacion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idiva`),
  KEY `iva_nrelacion` (`nrelacion`),
  CONSTRAINT `iva_ibfk_1` FOREIGN KEY (`nrelacion`) REFERENCES `encabeza` (`nrelacion`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- ----------------------------
-- Records of iva
-- ----------------------------
INSERT INTO `iva` VALUES ('18', '5', '0.0000', '21.0000', '\0', '2');

-- ----------------------------
-- Table structure for tributo
-- ----------------------------
DROP TABLE IF EXISTS `tributo`;
CREATE TABLE `tributo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tributoid` int(11) NOT NULL DEFAULT '99',
  `descripcion` varchar(100) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `baseimp` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `alic` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `importe` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `transferido` bit(1) NOT NULL DEFAULT b'0',
  `nrelacion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `tributo_nrelacion` (`nrelacion`),
  CONSTRAINT `tributo_ibfk_1` FOREIGN KEY (`nrelacion`) REFERENCES `encabeza` (`nrelacion`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- ----------------------------
-- Records of tributo
-- ----------------------------
INSERT INTO `tributo` VALUES ('18', '2', '', '0.0000', '0.0000', '5.0000', '\0', '2');
