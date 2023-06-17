procedures = """
CREATE PROCEDURE CalculateDiscountedSumProcedure()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE transId INT;
    DECLARE saleId INT;
    DECLARE saleAmount DECIMAL(10, 2);

    DECLARE cur CURSOR FOR SELECT idTransaction, idSale FROM transactions;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO transId, saleId;
        IF done THEN
            LEAVE read_loop;
        END IF;

        IF saleId IS NOT NULL THEN
            SELECT sale INTO saleAmount FROM sales WHERE idSale = saleId;

            UPDATE transactions
            SET sum_with_sale = sum - sum*(saleAmount / 100)
            WHERE idTransaction = transId;
        END IF;
    END LOOP;

    CLOSE cur;
END;


CREATE PROCEDURE CalculateFullTransactionSum()
BEGIN
    SET SQL_SAFE_UPDATES = 0;
    UPDATE full_transaction AS ft
    SET ft.full_transaction_sum = (
        SELECT SUM(
            CASE
                WHEN t.sum_with_sale IS NOT NULL THEN t.sum_with_sale
                ELSE t.sum
            END
        )
        FROM transactions AS t
        WHERE t.idFull_transaction = ft.idFull_transaction
    )
    WHERE ft.idFull_transaction IS NOT NULL;
SET SQL_SAFE_UPDATES = 1;
END;


CREATE PROCEDURE update_sales()
BEGIN
    DECLARE transId, transAmount INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT idTransaction, amount FROM transactions;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO transId, transAmount;
        IF done THEN
            LEAVE read_loop;
        END IF;

        UPDATE transactions
        SET idSale =
            CASE
                WHEN transAmount > 40 THEN 4
                WHEN transAmount > 25 THEN 3
                WHEN transAmount > 15 THEN 2
                WHEN transAmount > 5 THEN 1
                ELSE NULL
            END
        WHERE idTransaction = transId;
    END LOOP;

    CLOSE cur;
END;
"""