-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Vært: mariadb
-- Genereringstid: 06. 03 2026 kl. 15:01:51
-- Serverversion: 10.6.20-MariaDB-ubu2004
-- PHP-version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `travel_destinations`
--

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `destinations`
--

CREATE TABLE `destinations` (
  `destination_id` int(11) NOT NULL,
  `destination_name` varchar(200) NOT NULL,
  `destination_desc` text NOT NULL,
  `destination_country` varchar(200) NOT NULL,
  `destination_rating` int(20) NOT NULL DEFAULT 0,
  `destination_uts` int(200) NOT NULL,
  `destination_author` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `destinations`
--

INSERT INTO `destinations` (`destination_id`, `destination_name`, `destination_desc`, `destination_country`, `destination_rating`, `destination_uts`, `destination_author`) VALUES
(1, 'Malaga', 'A perfect paradise beach!', 'Spain', 0, 1772710559, 1),
(3, 'Legoland', 'fgfgdg123', 'Denmark', 0, 1772715401, 5),
(4, 'Cape Town', 'very scary wildlifeaaaa', 'Australia', 0, 1772718340, 5),
(5, 'new destination', 'beer', 'Germany', 0, 1772720421, 6),
(6, 'Milan', 'Wonderful', 'Italy', 0, 1772723808, 5),
(7, 'Rhodos', 'Great for summer vacation', 'Greece', 0, 1772805255, 7),
(8, 'Amsterdam', 'Wonderful architecture, rich history', 'Netherlands', 0, 1772807579, 7);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `users`
--

CREATE TABLE `users` (
  `user_id` int(200) NOT NULL,
  `user_username` varchar(200) NOT NULL,
  `user_password` varchar(200) NOT NULL,
  `user_email` varchar(200) NOT NULL,
  `user_reg` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `users`
--

INSERT INTO `users` (`user_id`, `user_username`, `user_password`, `user_email`, `user_reg`) VALUES
(1, 'asdsdasd', 'scrypt:32768:8:1$WPLWnodOKmM8DkQB$369c0910532777d59282211e9876a703627f1c575c643f198f05e8ab32db4d801160686b32df2a01bda924cfc899e179192b07eac299d6224d85b5eea44b360c', 'user@mail.com', '2026-03-03 16:05:53'),
(2, 'assdds', 'scrypt:32768:8:1$9Qy4j2jNbh6kZroA$4266000fce10fd1d97c7efb2edbebf2e863498156b3ff6b94f6c1388a726d051d0fdb704aeaf1758a52ac0c8de85eb06f05cdab39966ba6ffa4655721f4b7190', 'user@gmsil.com', '2026-03-03 16:10:02'),
(3, 'assdds1', 'scrypt:32768:8:1$5Z3LdByI6PlkwDKz$7ec6d42c4727fcc45fba46a99ebe731469cbf0c8f9ada9fda1ee3d9877a6f087ad6bb051ddaed4b2663b41f7208f2f95a9b59475d471d3154c1bf1506ff7c1cc', 'some@box.com', '2026-03-03 16:11:05'),
(4, 'abracadabra', 'scrypt:32768:8:1$qSBPhXMb2zeq3PJ0$5add74d8f88842c379f1c2fb90f99af4490ca43d08194c580093398c7dd397e55b1826a0a4b022c1af1479d5eceeda6e0cf874cf29db65e94dcb637e75eb3715', 'mailbox@mail.com', '2026-03-04 11:34:40'),
(5, 'asdasd', 'scrypt:32768:8:1$HVody5PaTvYO5TC4$e256674ff175fa87d4e0cffbfc17c7ab31c4f2c358003e6cebd84ed48f413678857d22c833b11ac904d9b9fa0c32eb8a26019a599314883100e3a73f25844bf1', 'user321@mail.com', '2026-03-04 13:16:11'),
(6, 'ivann', 'scrypt:32768:8:1$rWQdAoi0qrYAa5DA$b812ebcbbc4532ee130c48b8d1d42fd132d79c51e64c333c2d656ad7c426bca2859c7306e7a4d71f005ce7e76860d0b2b416e728e64b04331fab0c80aa834d9e', 'ivan@mail.com', '2026-03-05 14:18:03'),
(7, 'testuser', 'scrypt:32768:8:1$TSBlZAyB42WIa7gt$23e81dc326ebc72dcdcdd4138b9137856f269444dd7ffc5817ef3a868ef2de59e1b1b15453b5e8b3e115262750ab787d4bfa1b08f1032884b59e947cc565e5bc', 'email@mailbox.com', '2026-03-06 13:53:02');

--
-- Begrænsninger for dumpede tabeller
--

--
-- Indeks for tabel `destinations`
--
ALTER TABLE `destinations`
  ADD PRIMARY KEY (`destination_id`);

--
-- Indeks for tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- Brug ikke AUTO_INCREMENT for slettede tabeller
--

--
-- Tilføj AUTO_INCREMENT i tabel `destinations`
--
ALTER TABLE `destinations`
  MODIFY `destination_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Tilføj AUTO_INCREMENT i tabel `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
