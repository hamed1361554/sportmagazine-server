-- MySQL dump 10.13  Distrib 5.6.24, for Win64 (x86_64)
--
-- Host: localhost    Database: sportmagazine
-- ------------------------------------------------------
-- Server version	5.6.27-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `spinvoiceitems`
--

DROP TABLE IF EXISTS `spinvoiceitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spinvoiceitems` (
  `INVITMID` varchar(36) NOT NULL,
  `INVITMINVOICEID` varchar(36) NOT NULL,
  `INVITMPRODUCTID` varchar(36) NOT NULL,
  `INVITMPRICE` decimal(15,2) NOT NULL,
  `INVITMQNTY` int(2) NOT NULL,
  `INVITMCOLOR` varchar(36) NOT NULL,
  PRIMARY KEY (`INVITMID`),
  KEY `itminv_spinvoices_fk_idx` (`INVITMINVOICEID`),
  KEY `itminv_spproducts_fk_idx` (`INVITMPRODUCTID`),
  KEY `itminv_spproductcolors_fk_idx` (`INVITMCOLOR`),
  CONSTRAINT `itminv_spinvoices_fk` FOREIGN KEY (`INVITMINVOICEID`) REFERENCES `spinvoices` (`INVOICEID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `itminv_spproductcolors_fk` FOREIGN KEY (`INVITMCOLOR`) REFERENCES `spproductcolors` (`PRDCTCLRID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `itminv_spproducts_fk` FOREIGN KEY (`INVITMPRODUCTID`) REFERENCES `spproducts` (`PRODUCTID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spinvoiceitems`
--

LOCK TABLES `spinvoiceitems` WRITE;
/*!40000 ALTER TABLE `spinvoiceitems` DISABLE KEYS */;
/*!40000 ALTER TABLE `spinvoiceitems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spinvoices`
--

DROP TABLE IF EXISTS `spinvoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spinvoices` (
  `INVOICEID` varchar(36) NOT NULL,
  `INVOICEDATE` datetime NOT NULL,
  `INVOICESTATE` int(1) NOT NULL,
  `INVOICECONSUMERID` varchar(36) NOT NULL,
  PRIMARY KEY (`INVOICEID`),
  KEY `spusers_fk_idx` (`INVOICECONSUMERID`),
  CONSTRAINT `spusers_fk` FOREIGN KEY (`INVOICECONSUMERID`) REFERENCES `spusers` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spinvoices`
--

LOCK TABLES `spinvoices` WRITE;
/*!40000 ALTER TABLE `spinvoices` DISABLE KEYS */;
/*!40000 ALTER TABLE `spinvoices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spproductbrands`
--

DROP TABLE IF EXISTS `spproductbrands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spproductbrands` (
  `PRDCTBRANDID` varchar(36) NOT NULL,
  `PRDCTBRANDPRODUCTID` varchar(36) NOT NULL,
  `PRDCTBRAND` varchar(45) NOT NULL,
  PRIMARY KEY (`PRDCTBRANDID`),
  KEY `brands_prdct_fk_idx` (`PRDCTBRANDPRODUCTID`),
  CONSTRAINT `brands_prdct_fk` FOREIGN KEY (`PRDCTBRANDPRODUCTID`) REFERENCES `spproducts` (`PRODUCTID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spproductbrands`
--

LOCK TABLES `spproductbrands` WRITE;
/*!40000 ALTER TABLE `spproductbrands` DISABLE KEYS */;
/*!40000 ALTER TABLE `spproductbrands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spproductcolors`
--

DROP TABLE IF EXISTS `spproductcolors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spproductcolors` (
  `PRDCTCLRID` varchar(36) NOT NULL,
  `PRDCTCLRPRODUCTID` varchar(36) NOT NULL,
  `PRDCTCLRHEX` varchar(10) NOT NULL,
  PRIMARY KEY (`PRDCTCLRID`),
  KEY `spproducts_fk_idx` (`PRDCTCLRPRODUCTID`),
  CONSTRAINT `spproducts_fk` FOREIGN KEY (`PRDCTCLRPRODUCTID`) REFERENCES `spproducts` (`PRODUCTID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spproductcolors`
--

LOCK TABLES `spproductcolors` WRITE;
/*!40000 ALTER TABLE `spproductcolors` DISABLE KEYS */;
/*!40000 ALTER TABLE `spproductcolors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spproducthist`
--

DROP TABLE IF EXISTS `spproducthist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spproducthist` (
  `PRDCTHISTID` varchar(36) NOT NULL,
  `PRDCTID` varchar(36) NOT NULL,
  `PRDCTHISTNAME` varchar(255) DEFAULT NULL,
  `PRDCTHISTPRICE` decimal(15,2) DEFAULT NULL,
  `PRDCTHISTCATEGORY` int(2) DEFAULT NULL,
  `PRDCTHISTIMAGE` blob,
  `PRDCTHISTSTATE` int(1) DEFAULT NULL,
  `PRDCTHISTUNIQNAME` varchar(512) DEFAULT NULL,
  `PRDCTHISTEDITDATE` datetime NOT NULL,
  `PRDCTHISTCOLORS` varchar(512) DEFAULT NULL,
  `PRDCTHISTSIZES` varchar(512) DEFAULT NULL,
  `PRDCTHISTBRANDS` varchar(512) DEFAULT NULL,
  `PRDCTHISTCNTR` int(6) DEFAULT NULL,
  `PRDCTHISTAGECAT` int(1) DEFAULT NULL,
  `PRDCTHISTGNDR` int(1) DEFAULT NULL,
  `PRDCTHISTCMNT` varchar(255) DEFAULT NULL,
  `PRDCTHISTEDITORID` varchar(36) NOT NULL,
  PRIMARY KEY (`PRDCTHISTID`),
  KEY `prodcthist_prdct_fk_idx` (`PRDCTID`),
  KEY `prodcthist_user_fk_idx` (`PRDCTHISTEDITORID`),
  CONSTRAINT `prodcthist_prdct_fk` FOREIGN KEY (`PRDCTID`) REFERENCES `spproducts` (`PRODUCTID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `prodcthist_user_fk` FOREIGN KEY (`PRDCTHISTEDITORID`) REFERENCES `spusers` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spproducthist`
--

LOCK TABLES `spproducthist` WRITE;
/*!40000 ALTER TABLE `spproducthist` DISABLE KEYS */;
/*!40000 ALTER TABLE `spproducthist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spproducts`
--

DROP TABLE IF EXISTS `spproducts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spproducts` (
  `PRODUCTID` varchar(36) NOT NULL,
  `PRODUCTNAME` varchar(255) NOT NULL,
  `PRODUCTPRICE` decimal(15,2) NOT NULL,
  `PRODUCTCATEGORY` int(2) NOT NULL,
  `PRODUCTIMAGE` blob,
  `PRODUCTSTATE` int(1) NOT NULL DEFAULT '1',
  `PRODUCTUNIQNAME` varchar(512) NOT NULL,
  `PRODUCTPRODUCERID` varchar(36) NOT NULL,
  `PRODUCTCREATIONDATE` datetime NOT NULL,
  `PRODUCTCNTR` int(6) NOT NULL DEFAULT '0',
  `PRODUCTAGECAT` int(1) NOT NULL,
  `PRODUCTGNDR` int(1) NOT NULL,
  `PRODUCTCMNT` varchar(255) DEFAULT NULL,
  `PRODUCTWHOLESALETYPE` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`PRODUCTID`),
  KEY `prdcts_spusers_fk_idx` (`PRODUCTPRODUCERID`),
  CONSTRAINT `prdcts_spusers_fk` FOREIGN KEY (`PRODUCTPRODUCERID`) REFERENCES `spusers` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spproducts`
--

LOCK TABLES `spproducts` WRITE;
/*!40000 ALTER TABLE `spproducts` DISABLE KEYS */;
/*!40000 ALTER TABLE `spproducts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spproductsizes`
--

DROP TABLE IF EXISTS `spproductsizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spproductsizes` (
  `PRDCTSIZEID` varchar(36) NOT NULL,
  `PRDCTSIZEPRODUCTID` varchar(36) NOT NULL,
  `PRDCTSIZE` varchar(10) NOT NULL,
  PRIMARY KEY (`PRDCTSIZEID`),
  KEY `sizes_prdtc_fk_idx` (`PRDCTSIZEPRODUCTID`),
  CONSTRAINT `sizes_prdtc_fk` FOREIGN KEY (`PRDCTSIZEPRODUCTID`) REFERENCES `spproducts` (`PRODUCTID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spproductsizes`
--

LOCK TABLES `spproductsizes` WRITE;
/*!40000 ALTER TABLE `spproductsizes` DISABLE KEYS */;
/*!40000 ALTER TABLE `spproductsizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spuseractions`
--

DROP TABLE IF EXISTS `spuseractions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spuseractions` (
  `ID` varchar(36) NOT NULL,
  `USERID` varchar(36) NOT NULL,
  `USERACTION` int(1) NOT NULL,
  `ACTIONDATE` datetime NOT NULL,
  `ACTIONDATA` varchar(255) DEFAULT NULL,
  `ACTIONSTATE` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  KEY `FK_USERS_idx` (`USERID`),
  CONSTRAINT `FK_USERS` FOREIGN KEY (`USERID`) REFERENCES `spusers` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spuseractions`
--

LOCK TABLES `spuseractions` WRITE;
/*!40000 ALTER TABLE `spuseractions` DISABLE KEYS */;
INSERT INTO `spuseractions` VALUES ('6be72b8d-5ec3-4bfb-ae88-c60fbd541753','cdf29b8c-5667-423d-ab60-f39ba118c371',0,'2016-10-12 20:25:44','e8b2e2a64df83b0c9e38eaebc26d93c593d2cafc774718e165827848769a6389ae0fad811c3f514f0337ca442202dae5462f2e51d62e2c7d8f8327477f7678f799f5b3a88d3ff378',3);
/*!40000 ALTER TABLE `spuseractions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spuserhist`
--

DROP TABLE IF EXISTS `spuserhist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spuserhist` (
  `ID` varchar(36) NOT NULL,
  `USHISTDATE` datetime NOT NULL,
  `USHISTCLNTIP` varchar(15) DEFAULT NULL,
  `USHISTSTATUS` int(1) NOT NULL,
  `USHISTMSG` varchar(255) DEFAULT NULL,
  `USERID` varchar(36) NOT NULL,
  `USHISTMOBILE` varchar(15) DEFAULT NULL,
  `USHISTPHONE` varchar(15) DEFAULT NULL,
  `USHISTADDRESS` varchar(255) DEFAULT NULL,
  `USHISTWORKADDRESS` varchar(255) DEFAULT NULL,
  `USHISTNATIONALCODE` int(10) DEFAULT NULL,
  `USHISTEMAIL` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_SPUSERS_idx` (`USERID`),
  CONSTRAINT `FK_SPUSERS` FOREIGN KEY (`USERID`) REFERENCES `spusers` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spuserhist`
--

LOCK TABLES `spuserhist` WRITE;
/*!40000 ALTER TABLE `spuserhist` DISABLE KEYS */;
INSERT INTO `spuserhist` VALUES ('005ca603-37e2-4ec6-b953-41d8b4fe00a8','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('006a419e-6fec-41cd-aa10-a4746fe838f3','2016-10-12 00:00:00',NULL,4,'User [admin] with ticket [b246b0b7-84a2-4127-92f4-24318efd8b27] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('02a17414-65fc-4dd6-83db-09bf77a58ddd','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('0551ed41-9d4f-4594-991f-b130faa511ef','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [cb01f741-b90a-4026-82af-5060942ca4e5]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('06f3feb9-8740-444f-89b2-065b821239a7','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('0aa98c2a-3c58-4dfd-9ff4-644ab8f8e6d7','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [10030811-1df4-4bb4-b3ea-257a5b490516]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('0b2ccb17-aa21-491c-8ce2-e1b868709b29','2016-10-14 05:15:11',NULL,2,'User [admin] logged in with ticket [86dc3473-a1cc-4c31-95f2-12cab1614f75]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('0c7abbc4-ab35-4d53-9458-82d544ae059e','2016-10-12 20:26:28',NULL,2,'User [admin] logged in with ticket [ed5bf7ad-30ae-47c2-b182-111ff7239311]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('1081b6d3-571f-44dd-ad36-808ea24a1cbe','2016-10-14 05:19:57',NULL,2,'User [admin] logged in with ticket [70e3ea67-cdd5-4931-9090-5742629ab3a3]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('11e4cda2-8bfe-4e52-bf7c-5c465a6fcb89','2016-10-12 00:00:00',NULL,4,'User [admin] with ticket [935a9aaf-6ff2-44f7-9873-6d48db175660] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('134dbb84-1212-4f3b-a7da-07bb2d6fc553','2016-10-12 20:34:14',NULL,2,'User [hamed] logged in with ticket [6bf6e959-c0ed-4e92-8ca9-5c8ec86d24a8]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('136bc7c6-304b-47a7-a65a-c156dd209b89','2016-09-30 00:00:00',NULL,3,'User [101ec5c5-403a-4e17-91bb-b04d0ed67705] not found.','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('140f4d79-3cf9-4284-a8b0-e1ebd08a01c5','2016-10-14 04:48:20',NULL,2,'User [admin] logged in with ticket [1724d80a-09b1-4c78-855f-b97c15f0250b]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('193f94d1-3b09-4a0e-955a-402081909d77','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('1a8c8ef0-5632-4e6c-9530-95b9061c4159','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [528a8089-31f4-4e6c-a741-d68b0c466985]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('1b28ee16-5572-4270-b8a3-6da17fd82faa','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [132456]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('1b2afde8-9d8b-4544-9260-709a11711c3f','2016-10-12 20:11:25',NULL,4,'User [admin] with ticket [9be444e8-b8a0-4989-bb1a-bdab7cc34fde] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('1cc8f1e8-6f33-452f-84cd-3954198a6c7c','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('2a48dc9a-fa1e-4773-98ca-0f8fc52df086','2016-10-12 20:25:55',NULL,4,'User [admin] with ticket [e8e78431-3961-4304-9b65-7be8db4c92fe] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('2b8543ac-e36d-409c-aa01-2cb40540594b','2016-10-12 20:30:46',NULL,4,'User [admin] with ticket [4ae2248f-da2b-4068-8551-89044355e5a7] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('2ba98206-65a3-41db-8b52-99dfc4928c23','2016-10-12 20:32:26',NULL,2,'User [admin] logged in with ticket [f24b8db5-f5d7-420f-901c-c0b699b8131e]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('2e2761c8-ca00-4310-aa08-b23406966470','2016-09-30 00:00:00',NULL,4,'User [admin] with ticket [7abf7617-f076-45c0-9a96-107a707e3780] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('2f1a852b-71e8-4237-bf96-917253010b90','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [e62e45e9-a7fb-4684-98b8-2e637efd63ea]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('31766879-5fb9-495d-a34a-32a796b6a9e5','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('336931cc-3ce1-4aff-a7b5-99c752edb7f1','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [32529917-c3f1-4ecf-9ad9-5892437ac4e4]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('34f09e21-b203-4fc9-9518-79835988877f','2016-10-12 20:14:07',NULL,4,'User [admin] with ticket [a161da07-e69b-4ae0-8a89-b3a43ee896c6] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('37167a63-03e8-4792-9354-7a539be66ac2','2016-10-12 20:25:59',NULL,4,'User [admin] with ticket [ba17fbc9-d748-46ea-9a90-82cf70b09554] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('3bafbbe2-e861-4e60-b05d-958c4fbfdf0e','2016-10-12 20:31:54',NULL,4,'User [admin] with ticket [984939cf-f00b-4515-aa30-6ef14146d202] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('3d890205-e678-415d-9624-dc2716d3b234','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('3f888d2e-58cd-4799-9e92-1fc7a1574249','2016-10-12 20:25:57',NULL,2,'User [admin] logged in with ticket [61ad1425-2cfa-496c-be8c-74c5c892fc86]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('48a60910-51d4-4065-9d9f-a589dd0fb760','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [935a9aaf-6ff2-44f7-9873-6d48db175660]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('4bcd4b6a-683c-4e4a-8730-4c9e9ee80ab9','2016-10-12 20:14:08',NULL,2,'User [admin] logged in with ticket [7763db84-180e-414e-a060-75654d59d18b]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('4e6384da-a0e6-49f0-8829-53589fe5f0de','2016-10-12 20:12:31',NULL,2,'User [admin] logged in with ticket [4d58f5bc-d8e0-4425-b305-d1fc740ade3d]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('5312c249-74f0-48b9-ab64-2409a7cdec48','2016-10-12 20:25:57',NULL,2,'User [admin] logged in with ticket [9f1f4ad9-fcb9-4f50-aae9-980e263cf3c6]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('55320d31-5dcd-468a-9b2b-133ed7a9b52d','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [92692be9-f112-456f-a202-6f66330bc605]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('58e5437c-5767-4b06-82ce-a534755702a1','2016-10-12 20:14:04',NULL,4,'User [admin] with ticket [d9313b1c-ced6-404d-a6b6-bcd75c965190] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('593a129f-814a-4163-ad99-e580b9f6409e','2016-10-12 20:13:59',NULL,4,'User [admin] with ticket [9e46983b-803a-4731-ae9c-c80bb10db00f] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('611366bb-a9bf-4601-b4ed-65806a9c0d9b','2016-10-13 14:41:12',NULL,2,'User [hamed] logged in with ticket [83c0108d-48a7-4fb6-a523-62f48a0ea643]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('61df59c7-c4cf-4cd5-8338-ecc9d13688e4','2016-10-14 04:40:01',NULL,2,'User [admin] logged in with ticket [3d138306-41c9-4e12-9256-8671b259dbb3]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('631ba9cb-7a00-40d0-b802-6a18fd7e2429','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [427f9d6b-240a-4f10-a6c7-6d43257dca6b]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('65278c28-08d2-432c-99a5-ae82ad97205e','2016-10-12 20:14:02',NULL,4,'User [admin] with ticket [ca7c80e0-189a-4445-a37f-d7e8fc46c309] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('663e643d-c107-4c18-b0ad-93746929fba8','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [11f1738e-8922-4626-b514-0fd0cd8dfb8e]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('67efa4b1-f4b0-42bb-8a88-54e7f1510e48','2016-10-12 20:14:00',NULL,2,'User [admin] logged in with ticket [b7ff9510-cb5f-468a-ba19-a5881d4bed66]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('69da6438-fba4-493e-807d-66822232aeaa','2016-10-12 20:13:46',NULL,2,'User [admin] logged in with ticket [e47280e3-5eca-434a-839f-137b1a70e2d2]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('6a2c6bbf-a590-42a0-8b88-d614553753d5','2016-10-14 04:34:11',NULL,2,'User [admin] logged in with ticket [a4c091d7-cade-49d8-918d-94e7106e1845]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('6aa887be-b85c-4f03-b37a-a1a9e736d6bd','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('6c0dfae0-32a9-4801-a9c5-91f65a7682b8','2016-10-12 20:14:07',NULL,2,'User [admin] logged in with ticket [a161da07-e69b-4ae0-8a89-b3a43ee896c6]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('6c4e983f-0ce2-4b2c-b0aa-63d499c05fd5','2016-10-12 20:25:57',NULL,4,'User [admin] with ticket [61ad1425-2cfa-496c-be8c-74c5c892fc86] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('6c97e241-0c83-4ab4-a2e6-ef66d610770b','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [75430e48-1532-4549-9c8b-565bafed7698]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('708c80fe-fe50-4e76-91fc-b09a9d13b645','2016-10-12 20:30:39',NULL,2,'User [admin] logged in with ticket [4ae2248f-da2b-4068-8551-89044355e5a7]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('7347dd91-884a-4694-9e7c-00374804ec36','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('763e9cff-32d0-457b-85cc-b6bfc611987f','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [4a93f5ce-4c53-43b6-9ac8-916f4121b717]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('77b812e0-34d7-475e-9885-51afa97faf24','2016-10-12 00:00:00',NULL,4,'User [admin] with ticket [c421d335-33e7-4426-8594-93191df44182] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('78fe1dbd-b95a-4f91-aeb0-9a53e95f5b57','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('7dc70ebe-8d0c-49b4-968a-c1991b8d16e0','2016-10-07 00:00:00',NULL,3,'User [hamed] is inactive.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('7e574d42-609e-49df-a200-b6e8931fec98','2016-10-12 20:13:59',NULL,2,'User [admin] logged in with ticket [9e46983b-803a-4731-ae9c-c80bb10db00f]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('800dd347-4551-47c8-a34b-856073739c4e','2016-10-12 20:25:58',NULL,4,'User [admin] with ticket [7a8b742f-ee59-45ea-a4a8-929064028507] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('8142b66c-9863-4601-9611-732e1066dba5','2016-10-12 00:00:00',NULL,4,'User [admin] with ticket [c394c75b-9ae9-41a2-8c6b-f6c2e68524f6] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('8310eb00-3f1d-4756-8478-2884dbfde6ed','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('831dbbfd-64b1-46d6-beec-d1f9a01b531d','2016-10-12 20:25:45',NULL,4,'User [admin] with ticket [d27029ac-a5ae-46ed-9ebf-2cb2b1274729] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('836d76b2-7bfb-445e-b7e7-34d49dbde805','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('83d46fc4-804d-4328-adde-3136f52cab25','2016-10-12 20:18:08',NULL,2,'User [admin] logged in with ticket [5dd167bd-3c4a-4114-844c-d0932aeb17fd]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('853d4f44-95a6-46ce-8d03-ad74c6db0b12','2016-10-12 20:32:31',NULL,2,'User [admin] logged in with ticket [2722f2f6-4fe3-4466-9c3c-84d2601bd02e]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('86781aca-3b1a-4572-8f59-4191e37b6f67','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('88a4264f-9a99-43e7-b6d4-a0e14f9d558c','2016-10-12 20:14:06',NULL,4,'User [admin] with ticket [bf5af43a-0d67-4023-8a2b-5a4afdc6793d] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('89414df2-6661-4ba4-b7e3-727610ff49e6','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [cdd8e0fa-934d-4446-ba42-ab035576b0e3]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('8c3727c9-9237-477a-a748-13e6497f6ab9','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('8e49f7e3-396f-4e58-8582-4217f00171cb','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('927c40f5-22b2-4d1a-991f-014edd8feec5','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('94574f0b-e9d9-4738-a45d-7674bdfaede2','2016-10-12 20:29:27',NULL,2,'User [admin] logged in with ticket [a8a02f2b-c08d-4270-a669-a40c3427201e]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('95613591-9d7f-4810-ae70-1faea2b841d4','2016-10-12 20:25:45',NULL,2,'User [admin] logged in with ticket [d27029ac-a5ae-46ed-9ebf-2cb2b1274729]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('960ef840-3559-47da-b859-984e0c50f507','2016-10-14 05:11:30',NULL,2,'User [admin] logged in with ticket [8f644c78-edc7-4277-9d6a-b60830809870]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('97114c1f-c700-47c6-a54b-155a42539d66','2016-10-12 20:20:30',NULL,2,'User [admin] logged in with ticket [7393632c-48aa-4da9-af21-d333c792fbf7]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('97cf3daa-c407-4355-a810-09bf8065c209','2016-10-12 20:14:08',NULL,4,'User [admin] with ticket [7763db84-180e-414e-a060-75654d59d18b] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('98f4b2ef-756a-42ca-a8c2-535bc972099e','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [7abf7617-f076-45c0-9a96-107a707e3780]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('9af9f526-b1e7-42dd-aae6-7789639c45bb','2016-10-12 20:13:51',NULL,4,'User [admin] with ticket [e47280e3-5eca-434a-839f-137b1a70e2d2] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('9cf0a46a-e1cb-434f-9f1a-ff01321fb484','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('9d346661-cf3c-4c69-80c5-8eb3cf2a4116','2016-10-12 20:25:55',NULL,2,'User [admin] logged in with ticket [e8e78431-3961-4304-9b65-7be8db4c92fe]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('9d963fa8-a180-4a39-a672-684e6ff73f6a','2016-10-12 20:14:03',NULL,2,'User [admin] logged in with ticket [ab2ddc07-0ac2-446a-8657-aafb5ea62cdf]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('9e567ee6-c1fc-4e4f-80a4-1835740c3c62','2016-10-12 20:14:04',NULL,2,'User [admin] logged in with ticket [d9313b1c-ced6-404d-a6b6-bcd75c965190]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('9f239cf2-0089-4040-96ca-20d4733f52cb','2016-10-12 20:14:03',NULL,4,'User [admin] with ticket [ab2ddc07-0ac2-446a-8657-aafb5ea62cdf] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('a0df8c4e-716b-418f-b4f5-c226af7bdf86','2016-10-12 20:25:59',NULL,2,'User [admin] logged in with ticket [3f0adcac-b05c-4c59-b13e-0aecda3b55ba]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('a4396e3f-87d1-44b5-b794-769442f21949','2016-10-14 05:21:47',NULL,2,'User [admin] logged in with ticket [fbb4ec4e-9066-4e4c-908c-f174b6941d2f]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('a7e7bbae-e691-471a-8be9-cc346088bd18','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [e15c440f-e354-431e-8047-5f3f794e71d4]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('ab0325e0-c6a6-4c3a-927e-e93fbc0afc71','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [0e9435b2-750a-4e1e-ae70-566882426f05]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('acfd5307-223f-4449-8086-cbb879100728','2016-10-12 20:11:02',NULL,2,'User [admin] logged in with ticket [9be444e8-b8a0-4989-bb1a-bdab7cc34fde]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('ad12224e-9580-4fe1-880d-411ec6540042','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [c394c75b-9ae9-41a2-8c6b-f6c2e68524f6]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('adcafe86-503f-4316-accb-19fcf101a839','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [b246b0b7-84a2-4127-92f4-24318efd8b27]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('aed12704-7b31-4d62-91ce-cc717d444c03','2016-10-12 20:25:59',NULL,4,'User [admin] with ticket [3f0adcac-b05c-4c59-b13e-0aecda3b55ba] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('b0b5e026-5df4-43a2-b0ea-bb211f6e0a71','2016-10-14 05:22:42',NULL,2,'User [admin] logged in with ticket [4d85b6fb-21b2-4c41-a9cc-b0057c48acc2]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('b3b723b2-c878-4bf7-8576-a3622d12445a','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('b3f7df6d-5de6-4951-a6e5-ba0c82563478','2016-10-12 20:25:57',NULL,4,'User [admin] with ticket [9f1f4ad9-fcb9-4f50-aae9-980e263cf3c6] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('b6a409ea-3022-4905-a9c9-339fecf6cd00','2016-10-12 00:00:00',NULL,4,'User [admin] with ticket [cb01f741-b90a-4026-82af-5060942ca4e5] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('b6e8ed60-542b-40e5-9790-d840194e651f','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [a442979d-f961-401c-8f1f-093249c9ecfa]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('b73e1b27-7837-4d4c-8544-ce167ca46090','2016-10-12 20:31:54',NULL,2,'User [admin] logged in with ticket [984939cf-f00b-4515-aa30-6ef14146d202]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('b7f33c81-55f4-4ba7-b9a9-353017af5725','2016-10-12 20:14:06',NULL,2,'User [admin] logged in with ticket [bf5af43a-0d67-4023-8a2b-5a4afdc6793d]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('bae13bf8-4b55-40cd-a6bb-b553b26fa51c','2016-10-12 20:34:01',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('bf18e75b-90df-4ce1-a4d2-444099a7565d','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [132]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('c00a7db9-2928-45ac-bbf7-bf29076e9bdd','2016-10-12 20:13:58',NULL,2,'User [admin] logged in with ticket [ed011a3e-1b97-4415-9a3b-b68ed1fba887]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('c29ccff0-c961-4dd4-8b1f-113940c13755','2016-10-12 20:33:59',NULL,8,'User [hamed] entered wrong password [23456]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('c3b43fe2-9ce4-4f12-b6df-a2e18c0660b8','2016-10-12 20:25:59',NULL,2,'User [admin] logged in with ticket [ba17fbc9-d748-46ea-9a90-82cf70b09554]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('c527597d-5079-4cbf-be7d-beda3b312923','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [b01c2402-9ecc-44d6-bcd5-cfdd75cd0515]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('c6248246-343d-4111-be65-5599f0d656ee','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [c421d335-33e7-4426-8594-93191df44182]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('c6fa241a-efa3-4a08-94c1-08c02d212b4b','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [3fc92682-6682-427e-b122-8707d52bf118]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('caa2f6b6-d530-4a73-bc75-df6e993fe7f4','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('cb1df946-58e0-4d24-9485-58be015a7ea9','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [132]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('ce001427-7135-4b56-96d0-ea7a3e061867','2016-10-14 04:26:28',NULL,2,'User [admin] logged in with ticket [676f59ad-55c7-44ca-9c58-07eefa542b8e]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('d57c634f-b120-4d6d-b103-a4becc91b385','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('d5bb0732-43d9-4458-8d0b-3c4a7731d595','2016-10-12 20:13:58',NULL,4,'User [admin] with ticket [ed011a3e-1b97-4415-9a3b-b68ed1fba887] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('d5f66d07-3366-47b5-8342-b268546fe982','2016-10-12 00:00:00',NULL,4,'User [admin] with ticket [10030811-1df4-4bb4-b3ea-257a5b490516] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('d7d452b9-3038-4832-85f6-4d7400b298b4','2016-10-12 20:14:02',NULL,2,'User [admin] logged in with ticket [ca7c80e0-189a-4445-a37f-d7e8fc46c309]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('d86a2928-9697-4100-8193-c4359ad38e14','2016-10-12 00:00:00',NULL,2,'User [admin] logged in with ticket [a73f55e2-3172-4eef-b044-09e8cdcd04d8]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('da10cade-7605-4d84-8630-181a02444cc5','2016-10-12 20:13:54',NULL,2,'User [admin] logged in with ticket [17ce750e-5a22-4966-b420-7b806c679666]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('dac78df1-58be-412a-9491-d7581b352031','2016-10-12 20:13:03',NULL,4,'User [admin] with ticket [4d58f5bc-d8e0-4425-b305-d1fc740ade3d] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('db8b459b-4845-4526-b30f-bfe0ececbb04','2016-10-12 20:06:11',NULL,4,'User [admin] with ticket [f24d52a4-3ea9-4584-9e0d-0407bbfce6e1] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('dc5d25a5-a42c-4839-8267-c15c7353fc54','2016-10-07 00:00:00',NULL,3,'User [hamed] is inactive.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('debaf164-bbd8-41db-9175-420b07d0de07','2016-10-12 20:25:58',NULL,2,'User [admin] logged in with ticket [7a8b742f-ee59-45ea-a4a8-929064028507]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('e953e018-2d70-4e0b-a0b5-3d43fb9c18a9','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('eaacb1da-9ebb-483d-ae9b-321a7333c08a','2016-10-12 20:14:00',NULL,4,'User [admin] with ticket [b7ff9510-cb5f-468a-ba19-a5881d4bed66] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('eb4128e3-5526-4f9a-ae4f-02984b28f52d','2016-10-07 00:00:00',NULL,3,'User or password is invalid.','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('f2991030-48f5-43a4-8ec0-4f7fb70c742d','2016-10-12 20:26:52',NULL,4,'User [admin] with ticket [ed5bf7ad-30ae-47c2-b182-111ff7239311] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('f7d085ae-0a05-43f1-993a-7297f14255ca','2016-10-12 20:06:02',NULL,2,'User [admin] logged in with ticket [f24d52a4-3ea9-4584-9e0d-0407bbfce6e1]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('f83ce3b8-ba55-4f3d-9160-8a41923517bf','2016-10-07 00:00:00',NULL,8,'User [hamed] entered wrong password [123]','cdf29b8c-5667-423d-ab60-f39ba118c371',NULL,NULL,NULL,NULL,NULL,NULL),('f8c04e71-b6c7-4beb-b45e-364540d2daba','2016-09-30 00:00:00',NULL,3,'User [<built-in function id>] not found.','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('fbc56518-3283-480c-82d2-42266efa9f39','2016-10-12 20:13:54',NULL,4,'User [admin] with ticket [17ce750e-5a22-4966-b420-7b806c679666] logged out','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL),('fcb8c5dc-72fd-4a29-b645-229bb54cf71f','2016-09-30 00:00:00',NULL,2,'User [admin] logged in with ticket [ee398ad4-19a3-4626-ba6f-9224276cbc08]','101ec5c5-403a-4e17-91bb-b04d0ed67705',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `spuserhist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spusers`
--

DROP TABLE IF EXISTS `spusers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spusers` (
  `ID` varchar(36) NOT NULL,
  `USERID` varchar(50) NOT NULL,
  `USERNAME` varchar(100) DEFAULT NULL,
  `USERPSWD` varchar(255) DEFAULT NULL,
  `USERSTATE` int(1) NOT NULL,
  `USERLASTLOGIN` datetime NOT NULL,
  `USERTYPE` int(1) NOT NULL DEFAULT '0',
  `USERMOBILE` varchar(15) DEFAULT NULL,
  `USEREMAIL` varchar(25) DEFAULT NULL,
  `USERADDRESS` varchar(255) DEFAULT NULL,
  `USERWORKADDRESS` varchar(255) DEFAULT NULL,
  `USERPHONE` varchar(15) DEFAULT NULL,
  `USERPRODUCTIONTYPE` int(1) NOT NULL DEFAULT '0',
  `USERNATIONALCODE` int(10) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `USERID_UNIQUE` (`USERID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spusers`
--

LOCK TABLES `spusers` WRITE;
/*!40000 ALTER TABLE `spusers` DISABLE KEYS */;
INSERT INTO `spusers` VALUES ('101ec5c5-403a-4e17-91bb-b04d0ed67705','admin','ادمین سیستم','5ab582402c9e02cc43144ac1cc4200eb601ddda7c5dd3fbf616d2866933dbccbc37b8fb0690c0e0835237ea829157c8789439f13d1863c951e57ca8ed09135995314f30f80d45e06',1,'2016-09-09 00:00:00',2,NULL,NULL,NULL,NULL,NULL,0,NULL),('cdf29b8c-5667-423d-ab60-f39ba118c371','hamed','حامد ذکری','7847f1ee8898f725ab3370c424083718d0d7a99887806dc0b216ebf98a23f5e588ee516fa7c250f5d9d752780385dd5adeb8c410c9891020556417915fb8a1ab8be4cecfbe755759',1,'0001-01-01 00:00:00',0,NULL,NULL,NULL,NULL,NULL,0,NULL);
/*!40000 ALTER TABLE `spusers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-03 22:48:34
