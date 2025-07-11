-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: hospital_db
-- ------------------------------------------------------
-- Server version	8.4.5

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_users`
--

DROP TABLE IF EXISTS `admin_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_users`
--

LOCK TABLES `admin_users` WRITE;
/*!40000 ALTER TABLE `admin_users` DISABLE KEYS */;
INSERT INTO `admin_users` VALUES (1,'admin','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9');
/*!40000 ALTER TABLE `admin_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cashier_accounts`
--

DROP TABLE IF EXISTS `cashier_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashier_accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cashier_accounts`
--

LOCK TABLES `cashier_accounts` WRITE;
/*!40000 ALTER TABLE `cashier_accounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `cashier_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `specialization_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `specialization_id` (`specialization_id`),
  CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`specialization_id`) REFERENCES `specializations` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (4,'harika','1234567890','scrypt:32768:8:1$EbLtZUpvmfYIUj5k$7d4b48c5eb44e675a167e53befc8bb6983f83de5b92f01ee793177552fefc3d4417800b7fdb536a26db5eb579448ee5814c246d0a5fb21e2746c223a6b67b280',15),(5,'ram','1234567890','scrypt:32768:8:1$7TvcPOioZd3c7kBQ$4b725c0316b47942917ade1c71f8ee4b22c7a08338e05c0c3342b52460ca0f1108eba18777bd4625fdff49223c6e0169308ded6c668a88aa3467ce17a8d21c6a',NULL),(6,'Charan','1234567890','scrypt:32768:8:1$78ku3m6Qkq6dgqnC$2678b0bbb93e53a3f9c05abf3ab57c4ec4fbd4c330b70316d156fe9143005bb69c4bfe39faab91acd915fef4d6dd33fca00b9b67a9f6ae8a27a1257fd91650cc',18);
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `laboratory_accounts`
--

DROP TABLE IF EXISTS `laboratory_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `laboratory_accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laboratory_accounts`
--

LOCK TABLES `laboratory_accounts` WRITE;
/*!40000 ALTER TABLE `laboratory_accounts` DISABLE KEYS */;
INSERT INTO `laboratory_accounts` VALUES (4,'fgfdgfdg','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92');
/*!40000 ALTER TABLE `laboratory_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager_admins`
--

DROP TABLE IF EXISTS `manager_admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager_admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_admins`
--

LOCK TABLES `manager_admins` WRITE;
/*!40000 ALTER TABLE `manager_admins` DISABLE KEYS */;
INSERT INTO `manager_admins` VALUES (1,'manager','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9');
/*!40000 ALTER TABLE `manager_admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` text,
  `barcode` varchar(255) DEFAULT NULL,
  `registered_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `patient_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patient_id` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'charan','Male',26,'965421741','kuppam\r\n','632AA7DEAF8B','2025-07-10 22:46:00','2025-07-10 22:59:17',NULL),(2,'fdsfdf','Male',33,'1234567890','fdffef','77B805A358CC','2025-07-10 22:51:42','2025-07-10 22:59:17',NULL),(3,'qwerty','Female',22,'741852963','fsgdsgs','96B6AC48112C','2025-07-10 23:49:29','2025-07-10 23:49:29','happy9171569'),(4,'faefaef','Female',22,'2424224552','3r4343254325','195C439AE307','2025-07-10 23:53:59','2025-07-10 23:53:59','happy9171839'),(5,'cbn','Male',75,'7412365890','kuppam','190239EB98FE','2025-07-11 08:27:02','2025-07-11 08:27:02','happy843135');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharma_admins`
--

DROP TABLE IF EXISTS `pharma_admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharma_admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharma_admins`
--

LOCK TABLES `pharma_admins` WRITE;
/*!40000 ALTER TABLE `pharma_admins` DISABLE KEYS */;
INSERT INTO `pharma_admins` VALUES (1,'pharmaadmin','1c7d7f2a7668a1de0ea8f04a0ce6ff072e14781b052c51ee506a41b05d28b5cb');
/*!40000 ALTER TABLE `pharma_admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharma_audit_logs`
--

DROP TABLE IF EXISTS `pharma_audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharma_audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_username` varchar(100) DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharma_audit_logs`
--

LOCK TABLES `pharma_audit_logs` WRITE;
/*!40000 ALTER TABLE `pharma_audit_logs` DISABLE KEYS */;
INSERT INTO `pharma_audit_logs` VALUES (1,'pharmaadmin','logout','2025-07-07 16:44:04'),(2,'pharmaadmin','logout','2025-07-08 03:20:21'),(3,'pharmaadmin','logout','2025-07-08 03:26:58'),(4,'pharmaadmin','logout','2025-07-08 16:20:37'),(5,'pharmaadmin','logout','2025-07-08 16:25:34'),(6,'pharmaadmin','logout','2025-07-08 17:17:04'),(7,'pharmaadmin','logout','2025-07-09 16:12:41'),(8,'pharmaadmin','logout','2025-07-09 17:39:17');
/*!40000 ALTER TABLE `pharma_audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharma_medicines`
--

DROP TABLE IF EXISTS `pharma_medicines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharma_medicines` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `quantity` int NOT NULL,
  `expiry_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharma_medicines`
--

LOCK TABLES `pharma_medicines` WRITE;
/*!40000 ALTER TABLE `pharma_medicines` DISABLE KEYS */;
INSERT INTO `pharma_medicines` VALUES (11,'dolo',0,'2025-07-31','2025-07-08 17:15:24',70.00),(12,'amox',100,'2025-07-31','2025-07-09 15:42:01',10.00);
/*!40000 ALTER TABLE `pharma_medicines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharma_sales`
--

DROP TABLE IF EXISTS `pharma_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharma_sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `medicine_name` varchar(100) DEFAULT NULL,
  `quantity_sold` int NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `sold_by` varchar(100) DEFAULT NULL,
  `sale_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharma_sales`
--

LOCK TABLES `pharma_sales` WRITE;
/*!40000 ALTER TABLE `pharma_sales` DISABLE KEYS */;
INSERT INTO `pharma_sales` VALUES (1,'dolo',10,45.00,'pharmaadmin','2025-07-07'),(2,'dolo',1235,12.00,'pharmaadmin','2025-07-07'),(3,'dolo',10,10.00,'pharmaadmin','2025-07-07'),(4,'dolo',100,10.00,'pharmaadmin','2025-07-07'),(5,'dolo',1,1.00,'pharmaadmin','2025-07-07'),(6,'dolo',100,10.00,'pharmaadmin','2025-07-07'),(7,'syrup',5,100.00,'pharmaadmin','2025-07-07'),(8,'dolo',10,10.00,'pharmaadmin','2025-07-07'),(9,'dolo',900,30.00,'pharmaadmin','2025-07-08'),(10,'amoxyllin',1500,100.00,'pharmaadmin','2025-07-08'),(11,'dolo',10,45.00,'pharmaadmin','2025-07-08'),(12,'dolo',40,10.00,'pharmaadmin','2025-07-08');
/*!40000 ALTER TABLE `pharma_sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharmacy_staff`
--

DROP TABLE IF EXISTS `pharmacy_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharmacy_staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `password_hash` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharmacy_staff`
--

LOCK TABLES `pharmacy_staff` WRITE;
/*!40000 ALTER TABLE `pharmacy_staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `pharmacy_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receptionists`
--

DROP TABLE IF EXISTS `receptionists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receptionists` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receptionists`
--

LOCK TABLES `receptionists` WRITE;
/*!40000 ALTER TABLE `receptionists` DISABLE KEYS */;
INSERT INTO `receptionists` VALUES (1,'charan','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92');
/*!40000 ALTER TABLE `receptionists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_prices`
--

DROP TABLE IF EXISTS `service_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_prices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `service` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_prices`
--

LOCK TABLES `service_prices` WRITE;
/*!40000 ALTER TABLE `service_prices` DISABLE KEYS */;
INSERT INTO `service_prices` VALUES (1,'a',1000.00),(2,'x-ray',450.00);
/*!40000 ALTER TABLE `service_prices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `value` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'hospital_name','Happy9');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `specializations`
--

DROP TABLE IF EXISTS `specializations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `specializations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `specializations`
--

LOCK TABLES `specializations` WRITE;
/*!40000 ALTER TABLE `specializations` DISABLE KEYS */;
INSERT INTO `specializations` VALUES (15,'cardio'),(14,'ent'),(16,'eye'),(18,'hair'),(19,'lungs');
/*!40000 ALTER TABLE `specializations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-11  9:03:47
