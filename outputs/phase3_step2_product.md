# SQL Interview Practice Workbook for Junior Data Analysts

A practical PDF (printable and digital) for Junior and aspiring data analysts preparing for SQL interviews, especially in Egypt and the wider MENA region. Made by Mariam.

## Contents
1. Introduction to SQL Interview Questions
2. Basic SELECT Queries with Examples
3. Filtering and Sorting with WHERE and ORDER BY
4. Grouping and Aggregations with GROUP BY and COUNT

## Module 1: Introduction to SQL Interview Questions

SQL interview questions test your ability to write clear, efficient queries. These questions are common in tech companies, especially in Egypt and the wider MENA region, where data roles are growing fast. This module helps you understand what to expect and how to prepare.

1. **Review basic SQL concepts**
   Learn about tables, columns, SELECT, WHERE, JOINs, and GROUP BY. Use free online resources or beginner SQL tutorials.

2. **Study common question types**
   Focus on: filtering data (WHERE), sorting (ORDER BY), aggregations (COUNT, SUM), and joining tables (INNER JOIN).

3. **Practice with simple examples**
   Try writing queries on sample datasets. Use a tool like DB Fiddle or SQLite online.

4. **Check your answers against solutions**
   Compare your output with provided answers. Look for errors in syntax or logic.

5. **Track your progress**
   Keep a log of questions you’ve solved and which ones you found hard.

6. **Review one real interview question**
   Study a sample question from a junior data analyst role in Egypt or the MENA region.

**Worked Example**
*Question:* Find the number of orders placed in each month.
*Answer:*
```sql
SELECT
  EXTRACT(MONTH FROM order_date) AS month,
  COUNT(*) AS order_count
FROM orders
GROUP BY EXTRACT(MONTH FROM order_date)
ORDER BY month;
```

**Checklist**
- [ ] Reviewed basic SQL concepts
- [ ] Studied filtering, sorting, and joining
- [ ] Practiced one query on a sample dataset
- [ ] Checked answer against solution
- [ ] Logged the question and difficulty
- [ ] Reviewed a real interview example

**Common Mistakes**
- Using incorrect syntax (e.g., missing parentheses or semicolon)
- Forgetting to GROUP BY when aggregating
- Misunderstanding date functions like EXTRACT(MONTH FROM)
- Skipping the ORDER BY clause when required
- Not testing the query on sample data before submission

## Module 2: Basic SELECT Queries with Examples

**Intro**
This module teaches you how to write simple SQL queries to pull data from tables. You’ll learn the basics of the SELECT statement—what it does and how to use it to get specific columns from a table.

**Steps**
1. Start with a table name (e.g., `employees`).
2. Use `SELECT` followed by the column name(s) you want (e.g., `SELECT name, salary`).
3. Add `FROM` and the table name (e.g., `FROM employees`).
4. Run the query in your SQL environment (e.g., SQLFiddle, DB Fiddle, or a local tool).
5. Check if the output shows the correct data.
6. Try adding a WHERE clause to filter rows (e.g., `WHERE department = 'Sales'`).

**Worked Example**
Table: `employees`
Columns: `name`, `department`, `salary`
Query:
```sql
SELECT name, department
FROM employees
WHERE department = 'Engineering';
```
Output:
- Ahmed, Engineering
- Sara, Engineering

**Checklist**
- [ ] Write a SELECT statement with at least one column
- [ ] Add FROM followed by a table name
- [ ] Test the query in a SQL tool
- [ ] Verify output matches expected data
- [ ] Add a WHERE clause to filter rows (optional)

**Common Mistakes**
- Forgetting the `FROM` clause → query won’t run
- Using incorrect column names → wrong data appears
- Missing quotes around text values (e.g., `WHERE department = 'Sales'`)
- Using `SELECT *` without knowing what data you need
- Running the query without checking the table structure first

*Source: [SQLZoo - Basic SELECT](https://sqlzoo.net/sqlexamples/)*

## Module 3: Filtering and Sorting with WHERE and ORDER BY

**Intro**
Filtering and sorting help you find specific data and arrange it in a useful order. This module teaches how to use `WHERE` to filter rows and `ORDER BY` to sort them — key skills for SQL interviews.

**Steps**
1. Start with a table (like `orders`).
2. Use `WHERE` to filter rows. Example: `WHERE order_date > '2023-01-01'`.
3. Add `ORDER BY` to sort results. Example: `ORDER BY order_date DESC`.
4. Combine both: `SELECT * FROM orders WHERE order_date > '2023-01-01' ORDER BY order_date DESC`.
5. Test with real data — check if results match your expectations.
6. Try different filters and sorts (e.g., `WHERE amount > 100 ORDER BY amount ASC`).

**Worked Example**
Table: `sales` with columns `date`, `product`, `amount`.
Query:
```sql
SELECT *
FROM sales
WHERE product = 'Laptop'
ORDER BY amount DESC;
```
Result: Shows all laptop sales, sorted from highest to lowest amount.

**Checklist**
- [ ] Used `WHERE` to filter a specific condition
- [ ] Used `ORDER BY` to sort results (ASC or DESC)
- [ ] Tested query on sample data
- [ ] Applied filter and sort in one query
- [ ] Checked that results match expected output

**Common Mistakes**
- Forgetting to use parentheses when combining conditions (e.g., `WHERE price > 100 AND quantity > 5`)
- Using `ORDER BY` without a column name (e.g., `ORDER BY` alone)
- Misplacing `WHERE` or `ORDER BY` — they must come after `SELECT` and before `FROM`
- Sorting by a column that doesn’t exist in the table
- Using `ASC` or `DESC` without specifying which column to sort by

*Source: [SQLZoo - Filtering and Sorting](https://sqlzoo.net/solution/where)*

## Module 4: Grouping and Aggregations with GROUP BY and COUNT

Grouping helps you summarize data by categories. For example, you might count how many orders came from each city. This is key in real-world data analysis.

1. Use `GROUP BY` to split data into groups based on a column (like city or department).
2. Add aggregate functions like `COUNT(*)` to count rows in each group.
3. Choose the right column to group by—only one column per group unless using multiple columns.
4. Always include the grouping column in your SELECT list if it’s not in the GROUP BY.
5. Use `ORDER BY` to sort results, so you can see the most frequent groups first.
6. Test your query with a small dataset to verify it returns expected counts.

**Worked Example**
You have a table `orders` with columns: `city`, `order_id`.
Query:
```sql
SELECT city, COUNT(*) AS order_count
FROM orders
GROUP BY city
ORDER BY order_count DESC;
```
Result:
- Cairo: 120 orders
- Alexandria: 45 orders
- Giza: 30 orders

This shows which cities have the most orders.

**Checklist**
- [ ] Use `GROUP BY` with a relevant column (e.g., city, department)
- [ ] Include `COUNT(*)` or `COUNT(column)` in the SELECT
- [ ] Add `ORDER BY` to sort results
- [ ] Verify the output matches expected group counts
- [ ] Test with a small dataset first

**Common Mistakes**
- Forgetting to include the grouping column in the SELECT
- Using `COUNT(*)` on a column that has NULLs (it counts NULLs as zero)
- Grouping by multiple columns without including all in SELECT
- Not verifying the result matches real-world expectations

*Source: [How to Group Data in SQL – Stack Overflow](https://stackoverflow.com/questions/15941082/group-by-in-sql)*

## A note on results

This product gives you a method and templates. Your results depend on your situation and effort; nothing here is a promise of any outcome.