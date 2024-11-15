-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 12, 2024 at 06:04 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kriptografi_fp_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `encrypted_text` longtext NOT NULL,
  `private_key` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `encrypted_text`, `private_key`) VALUES
(21, 'Y3dmcG5ubm5ubm5ubm5ubm5ubm5ubm5ubg==', 'MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgNSAuM+zLLfNKufnIuxTo1tNAn+ksCX2DJhukPZqps6ehRANCAAQH/iqp1NdVVXneLsTejc3+bwacclLEopE3WvShLBk0M3gnTxNunpbIKxTHBwgKOmeLb+aP2AavuqhKk9gFNNun'),
(26, 'QlJLU0VFREFNQQpMTUVNVU1BQUtMUkVKSUFJREFBU1NEQUlSRVVBTlNLTlBHU0VST0FORU5JRFlBSk9QTkFZQURUSU1BSE5PS0VTVElHVU5HRVVSVEpOUkpBTkFBQVVGVURCTU5JSUU=', 'MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgfjtCEUlNtDGAlUDsREBZqeAbsIq9wubeW28b0ylkQ4ahRANCAAR2kAebewVWYSBlCuojdbpx+crlSz21NY/wl1wbp/KBYEMvs81gT7zkkpufRgrkB94UOWW4whpQS1XSj6KGnhvl'),
(27, 'SmFraXR1dWFrYW1rbmFsZWFrcGFubG9lZ2dlbm5haG12Z2dhbWVnbnN1cnVhaWxzbmtsZWlhYWtiOm1uYWVlaW5zbWtoaWFnYXNzbnNhdXVpZGttbGlraXlsYW5hYW5pbnZmZWdub2R0YXJvaWtta2RlYSxhY3Qpa2V5Z2RnYW5pbm51aWVncm5wc3VnbmFraWFsYW5rYWRraGhuYWEoYW5ibXQubWlhVWFzcG5uYW50ZWxhdW1udGtheSJpc2E1dGkiMnViNywsdSw5a20xYQ==', 'MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgh5ApVEdrJr/tU7FA9vAoBxIMur05UKUyzggElbvDzc6hRANCAAQZwPiXzWik1iEJhykSpcL2ICrzKEa4XleDyrvwUKUZ2bA3r2gEZ7tBarZRcdISxW4aJZmVIA1rIbXzbEDsAV4w');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  `fernetKey` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `fernetKey`) VALUES
(10, 'adhi', 'gAAAAABnMjJSVIK3JcbUsrB86QO-PmTY5Op4lJ2FKSON9xkINRbZK6KsE3Op8g_v3HLizWMsrNGwWH3sm_JYa0ZesHHoXIKFFQ==', 'JbQB0ls8BSvfPHi8gZwS8GD4DGeOc01NZMXbSTG4M2g='),
(11, 'admin', 'gAAAAABnMjO7jx5iR1S2Hv25avY0r_P2y3s4D2Kz0eOHF5HO4_Vi54WYAqAhZfs_VCayxYjOcxqEXxJzIu9dAeGWD2-5xvvtPw==', 'Zh5HI06W1LoejWjp_BHRuGUW9d_9YmQ22ZHFYWmnaFo='),
(12, 'krisna', 'gAAAAABnMjZZ5H_-hBFN8DHHX963bzIjID0lMvqPDvw5UZbCjEiWnyGcyAF2hUL5l14VcMmyggXM3FXBRyCPFePTMn3IdMgA3g==', 'zHuuNNZtnsTnntQJa11a2h5PLzgoL8Nodbd7ZH4Qqd0=');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
