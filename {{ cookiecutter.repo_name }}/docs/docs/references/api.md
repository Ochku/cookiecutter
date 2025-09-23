# API Reference — Python Usage

This document provides Python examples for interacting with the API using the `requests` library.

---

## Authentication

All requests require a bearer token in the header:

```py
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json",
}
```