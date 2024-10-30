# Cookie Extraction and Storage Logic with SQLAlchemy

This repository provides **cookie extraction logic** to handle HTTP request and response headers containing `Set-Cookie` and `Cookie`. The extracted cookies are stored in a database using SQLAlchemy ORM models, along with related attributes and scan item IDs. This project primarily showcases **cookie extraction logic**, and some referenced models are **not available** in this repository for public view due to proprietary constraints.

---

## Purpose

The goal of this project is to:

- **Extract cookies** from `Set-Cookie` and `Cookie` headers.
- **Store extracted cookies** with related attributes into a SQLAlchemy-managed database.
- Demonstrate how **dynamic attributes** from cookies can be saved and queried.
- Serve as a **reference** for similar implementations, with models and additional logic kept private for security and compliance reasons.

---

## Code Summary

### Key Components

1. **Cookie Extraction Logic**:
   - **`get_cookies_custom()`**: Extracts cookies using simple string splitting logic.
   - **`get_cookie()`**: Extracts cookies using `http.cookies.SimpleCookie` to parse cookie headers dynamically.

2. **Database Operations**:
   - **`get_or_create_request_cookie_attribute()`**: Checks if an attribute exists for request cookies and creates it if not.
   - **`get_or_create_response_cookie_attribute()`**: Checks if an attribute exists for response cookies and creates it if not.
   - **`get_scan_request_cookies()`**: Stores request cookies in the database.
   - **`get_scan_response_cookies()`**: Stores response cookies in the database.

3. **ORM Models**:
   - **`ScanRequestCookie`**: Stores request cookies and links to related attributes and scan items.
   - **`ScanResponseCookie`**: Stores response cookies with similar relationships.
   - **`ScanResponseCookieAttribute`**: Stores attribute names associated with response cookies.

---

## Usage

### 1. Install Dependencies
Ensure you have Python 3.8+ installed. Install SQLAlchemy:

```bash
pip install sqlalchemy
