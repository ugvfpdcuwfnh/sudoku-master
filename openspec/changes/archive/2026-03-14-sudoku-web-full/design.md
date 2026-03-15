## Context

The project currently has a robust Sudoku solver in `legacy_logic.py`. We need to expose this logic via a Flask web application.

## Goals / Non-Goals

**Goals:**
- Expose `solve_recursive` via a POST `/solve` endpoint.
- Provide a responsive 9x9 grid frontend.
- Ensure seamless communication between frontend and backend using JSON.

**Non-Goals:**
- User authentication or accounts.
- Database storage for puzzles.
- Advanced Sudoku features like hints or difficulty selection.

## Decisions

- **Framework**: Flask. Chosen for its simplicity and suitability for small-scale APIs.
- **Data Format**: JSON. Standard for web APIs. The grid will be represented as a 2D array of integers.
- **API Protocol**:
    - **Endpoint**: `POST /solve`
    - **Request Body**: `{ "board": [[...], [...], ...] }` (9x9 array of integers, 0 for empty)
    - **Response Body (Success)**: `{ "solution": [[...], [...], ...], "status": "ok" }`
    - **Response Body (Error)**: `{ "error": "Message", "status": "error" }`
- **Frontend**: Vanilla HTML/JavaScript (Fetch API) to avoid build-step complexity.

## Risks / Trade-offs

- **[Risk]** Invalid input from user → **[Mitigation]** Backend validation of the 9x9 grid structure and values before solving.
- **[Risk]** Unsolvable Sudoku → **[Mitigation]** Return an error message to the frontend if `solve_recursive` returns `None`.
