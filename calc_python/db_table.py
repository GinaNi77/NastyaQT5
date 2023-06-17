script = """
DROP SCHEMA IF EXISTS `canc` ;

CREATE SCHEMA IF NOT EXISTS `canc` DEFAULT CHARACTER SET utf8mb3 ;
USE `canc` ;

DROP TABLE IF EXISTS `canc`.`customers` ;

CREATE TABLE IF NOT EXISTS `canc`.`customers` (
  `idCustomer` INT NOT NULL AUTO_INCREMENT,
  `nameCustomer` VARCHAR(100) NOT NULL,
  `surnameCustomer` VARCHAR(100) NOT NULL,
  `address` VARCHAR(100) NULL DEFAULT NULL,
  `phone` VARCHAR(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idCustomer`));

DROP TABLE IF EXISTS `canc`.`products` ;

CREATE TABLE IF NOT EXISTS `canc`.`products` (
  `idProduct` INT NOT NULL AUTO_INCREMENT,
  `nameProduct` VARCHAR(100) NOT NULL,
  `descriptionProduct` VARCHAR(255) NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idProduct`));

DROP TABLE IF EXISTS `canc`.`sales` ;

CREATE TABLE IF NOT EXISTS `canc`.`sales` (
  `idSale` INT NOT NULL AUTO_INCREMENT,
  `sale` INT NOT NULL,
  PRIMARY KEY (`idSale`));

INSERT INTO `canc`.`sales` (`sale`) VALUES ('5');
INSERT INTO `canc`.`sales` (`sale`) VALUES ('10');
INSERT INTO `canc`.`sales` (`sale`) VALUES ('15');
INSERT INTO `canc`.`sales` (`sale`) VALUES ('25');

DROP TABLE IF EXISTS `canc`.`full_transaction` ;

CREATE TABLE IF NOT EXISTS `canc`.`full_transaction` (
  `idFull_transaction` INT NOT NULL AUTO_INCREMENT,
  `idCustomer` INT NOT NULL,
  `date` DATE NOT NULL,
  `full_transaction_sum` DECIMAL(10,2) NULL,
  PRIMARY KEY (`idFull_transaction`),
  
  CONSTRAINT `idCustomer`
    FOREIGN KEY (`idCustomer`)
    REFERENCES `canc`.`customers` (`idCustomer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
DROP TABLE IF EXISTS `canc`.`transactions` ;

CREATE TABLE IF NOT EXISTS `canc`.`transactions` (
  `idTransaction` INT NOT NULL AUTO_INCREMENT,
  `idFull_transaction` INT NOT NULL,
  `idProduct` INT NOT NULL,
  `amount` INT NOT NULL,
  `sum` DECIMAL(10,2) NULL DEFAULT NULL,
  `idSale` INT NULL,
  `sum_with_sale` DECIMAL(10,2) NULL,
  PRIMARY KEY (`idTransaction`),
  
  CONSTRAINT `idProduct`
    FOREIGN KEY (`idProduct`)
    REFERENCES `canc`.`products` (`idProduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,

  CONSTRAINT `idSale`
    FOREIGN KEY (`idSale`)
    REFERENCES `canc`.`sales` (`idSale`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,

  CONSTRAINT `idFull_transaction`
    FOREIGN KEY (`idFull_transaction`)
    REFERENCES `canc`.`full_transaction` (`idFull_transaction`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

"""