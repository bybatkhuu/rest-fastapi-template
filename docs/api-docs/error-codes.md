---
title: "Error Codes"
---

# 🚨 Error Codes

This document provides a comprehensive list of REST API error codes implemented in the application. Each error code includes details such as its unique code, name, HTTP status code, message, and description. It helps in identifying and debugging issues effectively while interacting with the API.

## Notes

- **Code**: A unique identifier for the error.
- **Name**: A descriptive name for the error.
- **HTTP Status Code**: The corresponding HTTP status code.
- **Message**: A short message explaining the error.
- **Description**: A detailed explanation of the error.

## List of Error Codes

| **Code**      | **Name**                  | **HTTP Status Code** | **Message**                  | **Description**                              |
|---------------|---------------------------|-----------------------|------------------------------|----------------------------------------------|
| `400_00000`   | BAD_REQUEST               | 400                   | Bad Request!                | The server could not understand the request.|
| `401_00000`   | UNAUTHORIZED              | 401                   | Unauthorized!               | Authentication is required and has failed.  |
| `401_01000`   | TOKEN_EXPIRED             | 401                   | Token has expired!          | Authentication is required and has failed.  |
| `401_01001`   | TOKEN_INVALID             | 401                   | Token is invalid!           | Authentication is required and has failed.  |
| `403_00000`   | FORBIDDEN                 | 403                   | Forbidden!                  | The server refuses to authorize the request.|
| `403_00001`   | NOT_VERIFIED              | 403                   | Not verified!               | The server refuses to authorize the request.|
| `403_01000`   | TOKEN_NOT_EXPIRED         | 403                   | Token has not expired!      | The server refuses to authorize the request.|
| `404_00000`   | NOT_FOUND                 | 404                   | Not Found!                  | The requested resource could not be found.  |
| `405_00000`   | METHOD_NOT_ALLOWED        | 405                   | Method Not Allowed!         | The HTTP method is not allowed.             |
| `406_00000`   | NOT_ACCEPTABLE            | 406                   | Not Acceptable!             | The request is not acceptable.              |
| `408_00000`   | REQUEST_TIMEOUT           | 408                   | Request Timeout!            | The server timed out waiting for the request.|
| `409_00000`   | CONFLICT                  | 409                   | Conflict!                   | The request could not be processed due to a conflict.|
| `413_00000`   | REQUEST_ENTITY_TOO_LARGE  | 413                   | Payload Too Large!          | The request payload is too large.           |
| `414_00000`   | REQUEST_URI_TOO_LONG      | 414                   | URI Too Long!               | The requested URI is too long.              |
| `415_00000`   | UNSUPPORTED_MEDIA_TYPE    | 415                   | Unsupported Media Type!     | The request media type is unsupported.      |
| `422_00000`   | UNPROCESSABLE_ENTITY      | 422                   | Unprocessable Entity!       | The server cannot process the request.      |
| `423_00000`   | LOCKED                    | 423                   | Locked!                     | The requested resource is locked.           |
| `429_00000`   | TOO_MANY_REQUESTS         | 429                   | Too Many Requests!          | The user has sent too many requests.        |
| `500_00000`   | INTERNAL_SERVER_ERROR     | 500                   | Internal Server Error!      | A generic server error occurred.            |
| `500_10000`   | DB_ERROR                  | 500                   | Internal Server Error!      | A database error occurred.                  |
| `500_10001`   | DB_PK_ERROR               | 500                   | Internal Server Error!      | A database primary key error occurred.      |
| `500_10002`   | DB_UQ_ERROR               | 500                   | Internal Server Error!      | A database unique key error occurred.       |
| `500_20000`   | SMTP_ERROR                | 500                   | Internal Server Error!      | An SMTP-related error occurred.             |
| `503_00000`   | SERVICE_UNAVAILABLE       | 503                   | Service Unavailable!        | The server is currently unavailable.        |
| `503_10000`   | DB_CONNECT_ERROR          | 503                   | Service Unavailable!        | Failed to connect to the database.          |
| `503_20000`   | SMTP_CONNECT_ERROR        | 503                   | Service Unavailable!        | Failed to connect to the SMTP server.       |
