triggers = """
CREATE TRIGGER transactions_BEFORE_INSERT
BEFORE INSERT ON `transactions`
FOR EACH ROW
BEGIN
    DECLARE product_sum DECIMAL(10,2);
    SELECT price INTO product_sum FROM products WHERE idProduct = NEW.idProduct;
	SET NEW.sum = product_sum * NEW.amount;
END;

CREATE TRIGGER transactions_BEFORE_UPDATE
BEFORE UPDATE ON `transactions`
FOR EACH ROW
BEGIN
    SET NEW.sum = (SELECT price FROM products WHERE idProduct = NEW.idProduct) * NEW.amount;
END;

CREATE TRIGGER `full_transaction_BEFORE_DELETE`
BEFORE DELETE ON `full_transaction`
FOR EACH ROW
BEGIN
    DELETE FROM transactions WHERE idFull_transaction = OLD.idFull_transaction;
END;
"""