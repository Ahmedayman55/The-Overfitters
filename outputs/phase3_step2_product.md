# SQL Interview Practice Workbook for Junior Data Analysts

A practical PDF (printable, single-page per question) for Junior and aspiring data analysts preparing for SQL interviews, especially in Egypt and the wider MENA region. Made by Mariam.

## Contents
1. Introduction to SQL Interview Questions
2. Basic SELECT Queries with Filtering
3. Grouping and Aggregations (GROUP BY, COUNT, SUM)
4. Joining Tables (INNER JOIN)

## Module 1: Introduction to SQL Interview Questions

SQL interview questions test your ability to write clear, efficient queries. In Egypt and the wider MENA region, interviews often focus on basic syntax, filtering, aggregation, and joining tables. This module helps you recognize common question types and how to approach them step by step.

1. **Identify the question type**
   Look for keywords: “filter”, “count”, “group by”, “join”, “order by”. This tells you which SQL concept to use.

2. **Understand the data structure**
   Sketch a simple table layout. Know what columns exist and what they represent.

3. **Break the question into steps**
   Write down each action: select columns → filter rows → group data → order results.

4. **Write the query in small parts**
   Start with a `SELECT` statement. Add `WHERE` to filter. Then add `GROUP BY` or `JOIN` as needed.

5. **Test your query with sample data**
   Plug in a few real values. Does it return the expected output?

6. **Review for clarity and correctness**
   Ask: Is the query readable? Does it match the question exactly?

**Worked Example**
*Question:* "List the number of orders per customer, only for customers who placed more than 1 order."
- Step 1: Identify type → aggregation + filtering
- Step 2: Table: `orders` with columns `customer_id`, `order_id`
- Step 3: Steps: count orders → group by `customer_id` → filter groups with count > 1
- Step 4: Query:
  ```sql
  SELECT customer_id, COUNT(*) AS order_count
  FROM orders
  GROUP BY customer_id
  HAVING COUNT(*) > 1;
  ```
- Step 5: Test with 3 customers: 1 has 1 order, 2 have 2 orders → only 2 customers return.
- Step 6: Query is clear and matches the question.

**Checklist**
- [ ] Identified the question type
- [ ] Sketched the table structure
- [ ] Broke the question into steps
- [ ] Wrote the query in small parts
- [ ] Tested with sample data
- [ ] Reviewed for clarity and correctness

**Common Mistakes**
- Using `WHERE` instead of `HAVING` when filtering groups
- Forgetting to group by a column when aggregating
- Writing queries that return too many or too few rows
- Assuming all interview questions are complex — most start simple
- Skipping the step of testing with sample data

*Source: https://www.datacamp.com/community/tutorials/sql-interview-questions*

## Module 2: Basic SELECT Queries with Filtering

**Intro**
This module teaches you how to write simple SQL queries that extract specific data from a table and filter only the rows you need. You’ll learn to use `SELECT`, `WHERE`, and basic comparison operators to find relevant records—key skills for any SQL interview.

**Steps**
1. Start with a table containing data (e.g., `employees` with columns: `name`, `age`, `department`, `salary`).
2. Use `SELECT` to pick specific columns (e.g., `SELECT name, age`).
3. Add `WHERE` to filter rows (e.g., `WHERE age > 25`).
4. Use comparison operators: `=`, `>`, `<`, `>=`, `<=`, `!=`.
5. Combine conditions with `AND` or `OR` (e.g., `WHERE age > 25 AND department = 'Sales'`).
6. Test your query with sample data to verify it returns only the expected rows.

**Worked Example**
Table: `employees`
Data:
| name     | age | department | salary |
|----------|-----|------------|--------|
| Ali      | 28  | Sales      | 5000   |
| Sara     | 32  | HR         | 4500   |
| Omar     | 24  | IT         | 6000   |

Query:
```sql
SELECT name, age
FROM employees
WHERE age > 25 AND department = 'Sales';
```

Result:
| name | age |
|------|-----|
| Ali  | 28  |

**Checklist**
- [ ] Used `SELECT` to pick needed columns
- [ ] Used `WHERE` to filter rows
- [ ] Applied a valid comparison operator (e.g., `>`, `=`, `!=`)
- [ ] Tested the query with sample data
- [ ] Used `AND` or `OR` only when needed and correctly
- [ ] Checked that output matches expected results

**Common Mistakes**
- Forgetting to use `WHERE` when filtering
- Using `=` for "not equal" (should use `!=`)
- Mixing up `AND` and `OR` logic (e.g., filtering for both "age > 25" and "department = 'HR'")
- Selecting all columns with `SELECT *` when only specific ones are needed
- Not testing the query with real sample data

*Source: https://www.w3schools.com/sql/sql_select_where.asp*

## Module 3: Grouping and Aggregations (GROUP BY, COUNT, SUM)

**Intro**
Grouping helps you see patterns in data. Use `GROUP BY` to split data into groups and functions like `COUNT()`, `SUM()` to summarize each group. This is key in SQL interviews—especially when analyzing sales, user activity, or logs.

**Steps**
1. Start with a table that has a grouping column (e.g., `region`, `product`, `date`).
2. Use `GROUP BY` on that column to create groups.
3. Add `COUNT(*)` to count rows in each group.
4. Add `SUM(column)` to total values (e.g., sales, revenue) per group.
5. Use `ORDER BY` to sort results—usually by count or sum.
6. Check your output: are all groups present? Are totals correct?

**Worked Example**
Table: `sales` with columns `region`, `amount`
Query:
```sql
SELECT
  region,
  COUNT(*) AS order_count,
  SUM(amount) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;
```
Result:
- North: 120 orders, $12,000
- South: 85 orders, $9,500
- East: 150 orders, $18,000

This shows which region has the most sales and most orders.

**Checklist**
- [ ] Grouping column is clearly defined
- [ ] Used `GROUP BY` on the grouping column
- [ ] Included `COUNT(*)` for row count
- [ ] Included `SUM(column)` for numeric totals
- [ ] Ordered results by a meaningful column (e.g., sum or count)
- [ ] Verified all groups match expected data

**Common Mistakes**
- Forgetting to use `GROUP BY` when summarizing data
- Using `SUM()` on a non-numeric column (e.g., `product_name`)
- Missing `ORDER BY`—results may be random
- Not checking if all groups are present in the output
- Using `COUNT(column)` instead of `COUNT(*)` when counting all rows

*Source: https://www.postgresql.org/docs/current/functions-aggregate.html*

## Module 4: Joining Tables (INNER JOIN)

When working with databases, data is often spread across multiple tables. For example, a users table might have names and emails, while an orders table has order details. To see which users placed orders, you combine the tables using a join. An INNER JOIN returns only the rows where there’s a match in both tables.

**Steps to use INNER JOIN:**

1. Identify the two tables you want to combine (e.g., `users` and `orders`).
2. Find the common column (e.g., `user_id`) that links the tables.
3. Use the `INNER JOIN` keyword in your query: `SELECT ... FROM users INNER JOIN orders ON users.user_id = orders.user_id`.
4. Specify which columns you want to display (e.g., `users.name`, `orders.order_date`).
5. Run the query in your SQL environment (e.g., PostgreSQL, MySQL, or SQL Server).
6. Check the results: only rows with matching `user_id` in both tables should appear.

**Worked Example:**
Table: `users`
| user_id | name     | email           |
|---------|----------|------------------|
| 1       | Ahmed    | ahmed@email.com  |
| 2       | Sara     | sara@email.com   |

Table: `orders`
| order_id | user_id | order_date   |
|----------|---------|--------------|
| 101      | 1       | 2024-03-01   |
| 102      | 2       | 2024-03-05   |

Query:
```sql
SELECT u.name, o.order_date
FROM users u
INNER JOIN orders o
ON u.user_id = o.user_id;
```

Result:
| name   | order_date   |
|--------|--------------|
| Ahmed  | 2024-03-01   |
| Sara   | 2024-03-05   |

*No row for user 3 (no order) — INNER JOIN only shows matches.*

**Checklist**
- [ ] Identify two tables to join
- [ ] Find the linking column (e.g., user_id)
- [ ] Use `INNER JOIN` with `ON` clause
- [ ] Select only needed columns
- [ ] Verify results show only matching rows

**Common Mistakes**
- Using `LEFT JOIN` when you need only matching records
- Forgetting to specify the correct column names in the `ON` clause
- Missing the `FROM` and `SELECT` parts of the query
- Assuming all rows from both tables will appear in the result
- Not checking if the join column exists in both tables

*Source: https://www.postgresql.org/docs/current/sql-join.html*

## A note on results

This product gives you a method and templates. Your results depend on your situation and effort; nothing here is a promise of any outcome.