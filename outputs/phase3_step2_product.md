# SQL Interview Practice Workbook for Junior Data Analysts

A practical PDF ebook (single file, printable, 10–12 pages) for Junior and aspiring data analysts preparing for SQL interviews, especially in Egypt and the wider MENA region. Made by Mariam.

## Contents
1. Introduction to SQL Interview Questions
2. Basic SELECT Queries with Worked Examples
3. Filtering and Sorting with WHERE and ORDER BY
4. Grouping and Aggregations (COUNT, SUM, AVG)

## Module 1: Introduction to SQL Interview Questions

SQL interview questions test your ability to think logically and extract data efficiently. These questions are common in tech interviews across Egypt and the MENA region. Knowing the patterns helps you prepare faster and feel more confident.

1. **Identify the interview pattern**
   Look for common types: filtering, joining, grouping, aggregating, or window functions.

2. **Understand the business context**
   Ask: What data is needed? Why is this question asked? For example, “Show sales by region” means you need region and sales data.

3. **Break the question into steps**
   Write down: What table(s)? What columns? What condition? What output?

4. **Practice with a sample query**
   Use a simple dataset (like a sales table) to build a query step by step.

5. **Check your output**
   Verify: Does it match the expected result? Are all rows included? Are duplicates removed?

6. **Review common patterns**
   Memorize 5–6 frequent patterns: filtering with `WHERE`, joining tables with `JOIN`, grouping with `GROUP BY`, calculating totals with `SUM()`.

**Worked Example**
*Question:* "Show total sales per region."
*Step-by-step:*
- Table: `sales` with columns `region`, `sale_amount`
- Step 1: SELECT `region`, SUM(`sale_amount`)
- Step 2: GROUP BY `region`
- Result: Region A → 1000, Region B → 1500

**Checklist**
- [ ] Identified the pattern (e.g., grouping)
- [ ] Listed relevant tables and columns
- [ ] Wrote a clear query structure
- [ ] Applied correct syntax (e.g., GROUP BY)
- [ ] Verified output matches expected result

**Common Mistakes**
- Forgetting to use `GROUP BY` when aggregating
- Using `SELECT *` instead of only needed columns
- Misreading the business question (e.g., “per month” vs “total”)
- Not checking if data types match between tables
- Writing queries that run but don’t answer the question correctly

*Source: https://www.datacamp.com/community/tutorials/sql-interview-questions*

## Module 2: Basic SELECT Queries with Worked Examples

SELECT queries retrieve data from tables. This module teaches you how to write simple queries to pull specific columns and rows from a database.

1. Use `SELECT` followed by column names to get data.
   Example: `SELECT name, salary FROM employees;`

2. Add `FROM` to specify the table name.
   Example: `SELECT name FROM employees;`

3. Use `*` to select all columns if needed.
   Example: `SELECT * FROM employees;`

4. Add a `WHERE` clause to filter rows (optional).
   Example: `SELECT name FROM employees WHERE salary > 5000;`

5. Use `ORDER BY` to sort results.
   Example: `SELECT name FROM employees ORDER BY salary DESC;`

6. Limit results with `LIMIT`.
   Example: `SELECT name FROM employees ORDER BY salary DESC LIMIT 5;`

**Worked Example**
Table: `employees`
Columns: `name`, `salary`, `department`

Query:
```sql
SELECT name, department
FROM employees
WHERE salary > 4000
ORDER BY salary DESC
LIMIT 3;
```
Result: Shows top 3 employees earning over 4000 in salary, sorted by highest to lowest.

**Checklist**
- [ ] Write a SELECT statement to get a specific column
- [ ] Add FROM to name the table
- [ ] Use WHERE to filter rows (if needed)
- [ ] Use ORDER BY to sort results
- [ ] Use LIMIT to restrict output size
- [ ] Test with a simple table structure

**Common Mistakes**
- Forgetting the `FROM` clause
- Using `*` without knowing it returns all columns
- Missing `;` at the end of the query
- Using `ORDER BY` without a column name
- Writing `WHERE` without a condition

*Source: https://www.w3schools.com/sql/sql_select.asp*

## Module 3: Filtering and Sorting with WHERE and ORDER BY

Filtering and sorting help you find specific data and arrange it in a useful order. This module teaches how to use `WHERE` to filter rows and `ORDER BY` to sort them — essential skills for SQL interviews.

1. Start with a basic SELECT statement to retrieve data.
2. Add `WHERE` to filter rows using conditions like `column = value` or `column > value`.
3. Use `ORDER BY` to sort results — ascending (default) or descending (`DESC`).
4. Combine `WHERE` and `ORDER BY` to first filter, then sort.
5. Test your query with sample data to ensure accuracy.
6. Always verify the output matches your expected result.

**Worked Example**
Query: Find employees earning more than 5000, sorted by salary descending.
```sql
SELECT name, salary
FROM employees
WHERE salary > 5000
ORDER BY salary DESC;
```
Result: Shows only high-paid employees, listed from highest to lowest salary.

**Checklist**
- [ ] Used `WHERE` to filter rows
- [ ] Used `ORDER BY` to sort results
- [ ] Sorted in ascending or descending order
- [ ] Verified output matches expected data
- [ ] Tested with realistic sample data

**Common Mistakes**
- Forgetting to use `ORDER BY` after `WHERE`
- Using `=` instead of `>` or `<` in conditions
- Missing quotes around text values (e.g., `'John'`)
- Sorting by a column not in the SELECT list
- Using `ORDER BY` without specifying direction (use `DESC` for descending)

*Source: https://www.mysqltutorial.org/sql-order-by*

## Module 4: Grouping and Aggregations (COUNT, SUM, AVG)

**Intro**
Grouping helps you see patterns in data. Aggregations like COUNT, SUM, and AVG give you summary stats. This module shows how to group data by categories and calculate totals, averages, or counts.

**Steps**
1. Select the columns you want to group by (e.g., `department`, `region`).
2. Use `GROUP BY` after your `SELECT` statement.
3. Add aggregation functions: `COUNT(*)`, `SUM(column)`, or `AVG(column)`.
4. Choose which column to group by (e.g., `department` or `country`).
5. Run the query in your SQL environment (e.g., DB Fiddle, PostgreSQL, or SQL Server).
6. Review results: check if totals match expected patterns.

**Worked Example**
Table: `employee_salaries`
Columns: `department`, `salary`

Query:
```sql
SELECT
  department,
  COUNT(*) AS employee_count,
  AVG(salary) AS avg_salary
FROM employee_salaries
GROUP BY department;
```

Result:
- Sales: 15 employees, avg salary $6,200
- HR: 8 employees, avg salary $5,400

**Checklist**
- [ ] Selected the correct grouping column
- [ ] Used `COUNT(*)` or a specific column
- [ ] Applied `AVG()` or `SUM()` correctly
- [ ] Included only relevant columns in `SELECT`
- [ ] Verified results match expected patterns

**Common Mistakes**
- Forgetting to use `GROUP BY` after selecting aggregated columns
- Using `SUM()` on a column without grouping (e.g., total of all salaries without grouping)
- Applying `AVG()` to a non-numeric column (e.g., `department`)
- Missing parentheses in `COUNT(*)` or `AVG()` functions
- Grouping by multiple columns without including all needed data

*Source: https://www.postgresql.org/docs/current/tutorial-aggregates.html*

## A note on results

This product gives you a method and templates. Your results depend on your situation and effort; nothing here is a promise of any outcome.