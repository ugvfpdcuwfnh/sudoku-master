## ADDED Requirements

### Requirement: Solve Sudoku via API
The system SHALL provide a POST endpoint at `/solve` that accepts a 9x9 Sudoku grid and returns the solved grid.

#### Scenario: Successful solve
- **WHEN** a valid 9x9 JSON array is POSTed to `/solve`
- **THEN** the system returns a 200 OK response with the solved 9x9 grid in the response body

#### Scenario: Unsolvable puzzle
- **WHEN** a valid but unsolvable 9x9 JSON array is POSTed to `/solve`
- **THEN** the system returns an error message indicating no solution was found

#### Scenario: Invalid input format
- **WHEN** an invalid data structure (not 9x9) is POSTed to `/solve`
- **THEN** the system returns a 400 Bad Request error
