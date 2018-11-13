/*
Navicat MySQL Data Transfer

Source Server         : capiovi
Source Server Version : 50554
Source Host           : 186.5.255.145:13306
Source Database       : fe

Target Server Type    : MYSQL
Target Server Version : 50554
File Encoding         : 65001

Date: 2018-11-13 17:07:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for caea
-- ----------------------------
DROP TABLE IF EXISTS `caea`;
CREATE TABLE `caea` (
  `idCAEA` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `CAEA` varchar(14) NOT NULL DEFAULT '',
  `Periodo` varchar(6) NOT NULL DEFAULT '',
  `Orden` char(1) NOT NULL DEFAULT '',
  `FchVigDesde` date NOT NULL DEFAULT '0000-00-00',
  `FchVigHasta` date NOT NULL DEFAULT '0000-00-00',
  `FchTopeInf` date NOT NULL DEFAULT '0000-00-00',
  `FchProceso` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `obs` text,
  `empresa` int(11) NOT NULL DEFAULT '1',
  `ptovta` char(4) NOT NULL DEFAULT '',
  `estado` char(1) NOT NULL DEFAULT '',
  `transferido` bit(1) NOT NULL DEFAULT b'0',
  `nrelacion` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`idCAEA`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for cbterel
-- ----------------------------
DROP TABLE IF EXISTS `cbterel`;
CREATE TABLE `cbterel` (
  `idCbteRel` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nrocontrol` int(10) unsigned NOT NULL DEFAULT '0',
  `TipoCbte` char(3) NOT NULL DEFAULT '',
  `PtoVta` char(4) NOT NULL DEFAULT '',
  `NroCbte` char(8) NOT NULL DEFAULT '',
  `nrelacion` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`idCbteRel`),
  KEY `nrocontrol` (`nrocontrol`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for encabeza
-- ----------------------------
DROP TABLE IF EXISTS `encabeza`;
CREATE TABLE `encabeza` (
  `ncontrol` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `fechacbte` date NOT NULL DEFAULT '0000-00-00',
  `tipocbte` varchar(3) NOT NULL DEFAULT '',
  `puntovta` varchar(4) NOT NULL DEFAULT '',
  `cbtenro` varchar(8) NOT NULL DEFAULT '',
  `tipodoc` varchar(2) NOT NULL DEFAULT '',
  `nrodoc` varchar(11) NOT NULL DEFAULT '0',
  `imptotal` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `imptotconc` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `impneto` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `impiva` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `imptrib` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `impopex` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `cae` varchar(14) NOT NULL DEFAULT '',
  `vencecae` date NOT NULL DEFAULT '0000-00-00',
  `resultado` varchar(1) NOT NULL DEFAULT '',
  `motivoobs` varchar(250) NOT NULL DEFAULT '',
  `errcode` varchar(6) NOT NULL DEFAULT '',
  `errmsg` varchar(250) NOT NULL DEFAULT '',
  `transferido` bit(1) NOT NULL DEFAULT b'0',
  `empresa` int(3) NOT NULL DEFAULT '1',
  `concepto` char(1) NOT NULL DEFAULT '1',
  `errorprog` text,
  `listo` bit(1) NOT NULL DEFAULT b'0',
  `tipows` varchar(2) NOT NULL DEFAULT 'WS',
  `nrelacion` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`ncontrol`),
  KEY `empresa` (`empresa`),
  CONSTRAINT `encabeza_ibfk_1` FOREIGN KEY (`empresa`) REFERENCES `shared`.`empresas` (`codigo`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3658 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for iva
-- ----------------------------
DROP TABLE IF EXISTS `iva`;
CREATE TABLE `iva` (
  `idiva` int(11) NOT NULL AUTO_INCREMENT,
  `nrocontrol` int(11) unsigned NOT NULL DEFAULT '0',
  `ivaid` int(11) NOT NULL DEFAULT '0',
  `baseimp` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `importe` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `transferido` bit(1) NOT NULL DEFAULT b'0',
  `nrelacion` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`idiva`),
  KEY `nrocontrol` (`nrocontrol`)
) ENGINE=InnoDB AUTO_INCREMENT=3668 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for tributo
-- ----------------------------
DROP TABLE IF EXISTS `tributo`;
CREATE TABLE `tributo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nrocontrol` int(11) unsigned NOT NULL DEFAULT '0',
  `tributoid` int(4) unsigned NOT NULL DEFAULT '0',
  `descripcion` varchar(100) NOT NULL DEFAULT '',
  `baseimp` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `alic` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `importe` decimal(12,4) NOT NULL DEFAULT '0.0000',
  `transferido` bit(1) NOT NULL DEFAULT b'0',
  `nrelacion` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `ncontrol` (`nrocontrol`)
) ENGINE=InnoDB AUTO_INCREMENT=974 DEFAULT CHARSET=latin1;
