# Employee Hiring Service Project

This project contains a service to manage hired employees, with endpoints that allow handling the database and processing data from CSV files uploaded in the request payload. The service is structured into three main parts: Routers, Services, and Repository, following good practices for separation of concerns.

## Project Structure

The project is divided into three main parts:

- **Routers**: Defines the endpoint routes.
- **Services**: Handles all the data processing and any additional manipulation that may be needed.
- **Repository**: Responsible for database transactions.

### Models and Schemas

**Basemodels** are included to correctly manage relationships between entities, and **Schemas** are used to validate the API responses.

## Exercises

### Exercise 1

For this exercise, I thought about using a **test case**, as I had never worked with data separation by quarters. However, I discovered that SQLAlchemy already has a built-in function (`extract("quarter",....)`), which made the task much easier. The only thing I had to do was apply the correct grouping after using this function.

### Exercise 2

The approach was similar to the first exercise, but in this case, I worked with grouping only by **year**. The average calculations were performed directly in the service.

## Notes on Testing

I would have liked to add automated tests to ensure code quality, but since I received the test quite late, just a day before the deadline, I ran out of available time. Even so, I made sure the code was as **"test-driven"** as possible, ensuring it would be easy to test in the future.
