-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Braintrainning
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Braintrainning
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Braintrainning` DEFAULT CHARACTER SET utf8 ;
USE `Braintrainning` ;

-- -----------------------------------------------------
-- Table `Braintrainning`.`Games`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Braintrainning`.`Games` ;

CREATE TABLE IF NOT EXISTS `Braintrainning`.`Games` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `exercise` VARCHAR(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`exercise` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Braintrainning`.`Players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Braintrainning`.`Players` ;

CREATE TABLE IF NOT EXISTS `Braintrainning`.`Players` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pseudonym` VARCHAR(50) NOT NULL,
  `password` VARCHAR(72) NOT NULL,
  `levelofaccess` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `pseudonym_UNIQUE` (`pseudonym` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Braintrainning`.`Games_has_Players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Braintrainning`.`Games_has_Players` ;

CREATE TABLE IF NOT EXISTS `Braintrainning`.`Games_has_Players` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  `duration` TIME NOT NULL,
  `startdate` DATETIME NOT NULL,
  `nb_ok` INT NOT NULL,
  `nb_tot` INT NOT NULL,
  INDEX `fk_Games_has_Players_Players1_idx` (`player_id` ASC) VISIBLE,
  INDEX `fk_Games_has_Players_Games_idx` (`game_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_Games_has_Players_Games`
    FOREIGN KEY (`game_id`)
    REFERENCES `Braintrainning`.`Games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Games_has_Players_Players1`
    FOREIGN KEY (`player_id`)
    REFERENCES `Braintrainning`.`Players` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
