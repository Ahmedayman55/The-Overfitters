# SQL Interview Practice Workbook for Junior Data Analysts

A practical PDF for Junior and aspiring data analysts preparing for SQL interviews, especially in Egypt and the wider MENA region. Made by Mariam.

## Contents
1. Introduction to SQL Interview Questions
2. Basic Queries: SELECT, WHERE, GROUP BY
3. Joining Tables: INNER JOIN and LEFT JOIN
4. Aggregation and Filtering: COUNT, SUM, HAVING

## Module 1: Introduction to SQL Interview Questions

# Introduction to SQL Interview Questions

SQL interviews often follow predictable patterns. This module helps you recognize common question types and how to approach them step by step.

1. **Identify the question type**
   Look for keywords like “count,” “group by,” “join,” “filter,” or “order by.” These signal the pattern (e.g., filtering, aggregation, joining tables).

2. **Understand the goal**
   Ask: “What exactly is being asked?” For example, “Show the top 5 customers by total spending” means you need to calculate total spending and rank customers.

3. **Break it into steps**
   Write down:
   - Which tables are involved?
   - What data do you need from each?
   - What operations (filter, join, group) are needed?

4. **Write the query in small parts**
   Start with a simple SELECT. Add filters (WHERE), joins (JOIN), and grouping (GROUP BY) one at a time. Test each part.

5. **Verify correctness**
   Run the query with sample data. Check:
   - Are the right columns returned?
   - Is the data filtered correctly?
   - Does the output match the expected structure?

6. **Practice with real examples**
   Use the example below to see how this works in practice.

**Worked Example**
*Question:* “List the top 3 customers by total order value.”
- Step 1: Identify tables — `customers` and `orders`.
- Step 2: Goal — sum order value per customer, rank top 3.
- Step 3: Query:
```sql
SELECT c.customer_name, SUM(o.order_value) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC
LIMIT 3;
```

**Checklist**
- [ ] Identified the question type
- [ ] Defined the goal clearly
- [ ] Listed involved tables and columns
- [ ] Wrote a step-by-step query
- [ ] Tested with sample data
- [ ] Verified output matches expectations

**Common Mistakes**
- Assuming all questions require JOINs (some only need SELECT and WHERE)
- Forgetting to GROUP BY when aggregating
- Using LIMIT without ORDER BY
- Misreading the question — e.g., “top 3” vs. “all customers with over $100 spent”

*Source: https://www.datacamp.com/community/tutorials/sql-interview-questions*

## Module 2: Basic Queries: SELECT, WHERE, GROUP BY

# Module 2: Basic Queries – SELECT, WHERE, GROUP BY

This module builds confidence with core SQL syntax using real-world examples. You’ll learn how to extract data, filter rows, and group results—skills needed in most SQL interviews.

1. **Write a SELECT statement** to list specific columns (e.g., `name`, `salary`) from a table like `employees`.
2. **Use WHERE** to filter rows. For example, add `WHERE department = 'Sales'` to only show sales employees.
3. **Add GROUP BY** to group rows by a column (e.g., `department`) and see counts or sums.
4. **Combine WHERE and GROUP BY** to filter before grouping (e.g., only group employees earning over 5000).
5. **Test your query** with sample data from the workbook’s provided tables.
6. **Review output** to ensure the data matches your expectations.

**Worked Example**
Table: `employees`
| name | department | salary |
|------|------------|--------|
| Ali  | Sales      | 5000   |
| Sam  | Sales      | 6000   |
| Fatima| HR         | 4500   |
| Omar | Sales      | 7000   |

Query:
```sql
SELECT department, COUNT(*) AS employee_count
FROM employees
WHERE salary > 5000
GROUP BY department;
```

Output:
| department | employee_count |
|-----------|----------------|
| Sales     | 2              |

Only Sales employees earning over 5000 are grouped. HR is excluded due to salary filter.

**Checklist**
- [ ] Wrote a SELECT statement with at least two columns
- [ ] Used WHERE to filter rows based on a condition
- [ ] Used GROUP BY to group data by a column
- [ ] Combined WHERE and GROUP BY in one query
- [ ] Tested query with sample data
- [ ] Verified output matches expected results

**Common Mistakes**
- Forgetting to use parentheses around conditions in WHERE
- Using GROUP BY on a column not in SELECT (e.g., selecting `name` without grouping by `department`)
- Applying WHERE after GROUP BY when filtering should happen first
- Misreading the output—double-check if filtered rows are correctly grouped

*Source: [https://www.postgresql.org/docs/current/tutorial-queries.html](https://www.postgresql.org/docs/current/tutorial-queries.html)*

## Module 3: Joining Tables: INNER JOIN and LEFT JOIN

# Module 3: Joining Tables – INNER JOIN and LEFT JOIN

**Intro**
In SQL interviews, joining tables is a common task. You’ll often need to combine data from multiple tables—like orders and customers—to answer real questions. This module teaches you how to use INNER JOIN and LEFT JOIN with practical examples from typical interview scenarios in Egypt and the wider MENA region.

**Steps**
1. Identify the tables involved and the question you’re trying to answer (e.g., “Show all orders with customer names”).
2. Determine which columns are common between tables (e.g., `customer_id`).
3. Choose the correct join type:
   - Use INNER JOIN to show only records where both tables have matching values.
   - Use LEFT JOIN to show all records from the left table, even if there’s no match in the right table.
4. Write the JOIN clause: `FROM table1 JOIN table2 ON table1.id = table2.id`.
5. Add a WHERE clause if needed to filter results (e.g., `WHERE order_date > '2023-01-01'`).
6. Test your query with sample data to ensure it returns the expected rows.

**Worked Example**
*Tables: `orders` (order_id, customer_id, order_date) and `customers` (customer_id, name, city)*
*Question: List all orders with customer names. If a customer has no order, still show their name.*
✅ Use LEFT JOIN:
```sql
SELECT o.order_id, c.name, o.order_date
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;
```
This shows all orders and all customers—even those without orders.

**Checklist**
- [ ] Identify tables and question
- [ ] Find common column (e.g., customer_id)
- [ ] Choose INNER or LEFT JOIN based on need
- [ ] Write JOIN clause with correct ON condition
- [ ] Add WHERE clause if filtering
- [ ] Test with sample data

**Common Mistakes**
- Using INNER JOIN when you need all records from one table.
- Forgetting to specify the ON condition in JOIN.
- Mixing up which table is on the left or right.
- Using WHERE before JOIN, which can exclude valid matches.

*Source: https://www.postgresql.org/docs/current/tutorial-join.html*

## Module 4: Aggregation and Filtering: COUNT, SUM, HAVING

# Module 4: Aggregation and Filtering – COUNT, SUM, HAVING

**Intro**
This module teaches how to group data and filter results using SQL’s `COUNT`, `SUM`, and `HAVING` clauses. You’ll solve real problems like counting orders by region or finding high-value customers. These skills are common in SQL interviews, especially in Egypt and the wider MENA region where data-driven roles are growing.

**Steps**
1. Use `GROUP BY` to group rows by a column (e.g., region, product category).
2. Apply `COUNT(*)` or `COUNT(column)` to count rows or non-null values in each group.
3. Use `SUM(column)` to calculate totals (e.g., total sales per region).
4. Use `HAVING` to filter groups—only show groups that meet a condition (e.g., total sales > 1000).
5. Avoid using `WHERE` after `GROUP BY`—it filters before grouping.
6. Always check your output: does it match the expected pattern?

**Worked Example**
Table: `sales` (columns: region, product, sales_amount)
Query:
```sql
SELECT region, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY region
HAVING SUM(sales_amount) > 5000;
```
Result: Shows only regions where total sales exceed 5000.

**Checklist**
- [ ] Group data using `GROUP BY`
- [ ] Use `COUNT(*)` or `COUNT(column)` to count rows
- [ ] Use `SUM(column)` to calculate totals per group
- [ ] Apply `HAVING` to filter groups, not rows
- [ ] Verify results match expected output
- [ ] Test with sample data before final submission

**Common Mistakes**
- Using `WHERE` to filter groups—this filters before grouping, not after.
- Forgetting to use `HAVING` when filtering grouped results.
- Counting `NULL` values incorrectly—use `COUNT(column)` only for non-nulls.
- Misapplying `SUM()` to count rows—`SUM()` adds numbers, not rows.
- Not verifying results with sample data.

*Source: [https://www.postgresql.org/docs/current/tutorial-aggregation.html](https://www.postgresql.org/docs/current/tutorial-aggregation.html)*

## A note on results

This product gives you a method and templates. Your results depend on your situation and effort; nothing here is a promise of any outcome.