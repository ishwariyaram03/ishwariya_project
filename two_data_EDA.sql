create database Credit_Analysis;
USE Credit_Analysis;

-- 1.Retrieve all records from the loan_data table
USE credit_analysis;

SELECT * FROM loan_data1
UNION ALL
SELECT * FROM loan_data2;

-- 2.Display all loan applications with their contract type and contract status
DESCRIBE loan_data1;
DESCRIBE loan_data2;
SELECT SK_ID_CURR, NAME_CONTRACT_TYPE, NAME_CONTRACT_STATUS FROM loan_data1;


-- 3. Retrieve all applications where the contract status is 'Approved'
SELECT * FROM loan_data1 WHERE NAME_CONTRACT_STATUS = 'Approved';

-- 4. Display all applications where the contract status is 'Refused'
SELECT * FROM loan_data1 WHERE NAME_CONTRACT_STATUS = 'Refused';

-- 5. Retrieve all applications belonging to the 'Repeater' client type
SELECT * FROM loan_data2 WHERE NAME_CLIENT_TYPE = 'Repeater';
-- 6. Calculate the total number of loan applications.
SELECT SUM(total_applications) AS total_applications
FROM (
    SELECT COUNT(*) AS total_applications FROM loan_data1
    UNION ALL
    SELECT COUNT(*) AS total_applications FROM loan_data2
) AS Loan_Data_Final;

-- 7. Calculate the total credit amount across all applications.
SELECT SUM(AMT_CREDIT) AS total_credit_amount FROM Loan_Data1;

-- 8. Calculate the average loan application amount.
SELECT avg(AMT_APPLICATION) AS avg_application_amount FROM Loan_Data1;

-- 9. Count the number of applications for each contract status.
SELECT NAME_CONTRACT_STATUS, COUNT(*) AS application_count FROM Loan_Data1 GROUP BY NAME_CONTRACT_STATUS;

-- 10. Calculate the average annuity amount for each contract type.
SELECT NAME_CONTRACT_TYPE, AVG(AMT_ANNUITY) AS avg_annuity_amount FROM Loan_Data1 GROUP BY NAME_CONTRACT_TYPE;
-- join based queries
-- 11. Retrieve loan applications where the credit amount is greater than 500,000.
SELECT * FROM Loan_Data1 WHERE AMT_CREDIT > 500000;

-- 12. Find applications where the down payment amount is greater than 50,000.
SELECT * FROM Loan_Data1 WHERE AMT_DOWN_PAYMENT > 50000;

-- 13. Count the number of applications for each client type.
select NAME_CLIENT_TYPE, COUNT(*) AS application_count FROM Loan_Data2 GROUP BY NAME_CLIENT_TYPE;

-- 14. Calculate the average credit amount for each loan contract status.
select NAME_CONTRACT_STATUS, avg(AMT_CREDIT) AS credit_amount FROM Loan_Data1 GROUP BY NAME_CONTRACT_STATUS;

-- 15. Find the top 5 product combinations with the highest number of applications.
SELECT PRODUCT_COMBINATION, COUNT(*) AS application_count FROM Loan_Data2 GROUP BY PRODUCT_COMBINATION limit 5;

-- 16. Calculate the total credit amount for approved and refused applications separately.
SELECT NAME_CONTRACT_STATUS, SUM(AMT_CREDIT) AS total_credit_amount FROM Loan_Data1 WHERE NAME_CONTRACT_STATUS IN ('Approved', 'Refused') GROUP BY NAME_CONTRACT_STATUS;

-- 17. Find the top 3 contract types with the highest average credit amount.
SELECT NAME_CONTRACT_TYPE, AVG(AMT_CREDIT) AS avg_credit_amount FROM Loan_Data1 GROUP BY NAME_CONTRACT_TYPE LIMIT 3;

-- 18. Calculate the total application amount for each payment type.
SELECT NAME_PAYMENT_TYPE, SUM(AMT_APPLICATION) AS total_application_amount FROM Loan_Data1 GROUP BY NAME_PAYMENT_TYPE;

-- 19. Identify the top 5 seller industries based on total credit amount.
SELECT
    NAME_SELLER_INDUSTRY,
    COUNT(*) AS industry_count
FROM loan_data2
WHERE NAME_SELLER_INDUSTRY IS NOT NULL
GROUP BY NAME_SELLER_INDUSTRY
LIMIT 5;
SELECT
    SUM(AMT_CREDIT) AS total_credit_amount
FROM loan_data1;


-- 20. Calculate the approval percentage for each contract type.
SELECT NAME_CONTRACT_TYPE, COUNT(*) AS total_applications, SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Approved' THEN 1 ELSE 0 END) AS approved_count, ROUND(
    SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 0) AS approval_percentage FROM Loan_Data1 GROUP BY NAME_CONTRACT_TYPE;