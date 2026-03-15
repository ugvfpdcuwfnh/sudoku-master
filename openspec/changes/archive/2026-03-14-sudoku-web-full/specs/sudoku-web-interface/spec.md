## ADDED Requirements

### Requirement: Interactive 9x9 Grid
The system SHALL display a 9x9 grid of input fields where users can enter Sudoku numbers (1-9 or empty).

#### Scenario: Grid initialization
- **WHEN** the user loads the index page
- **THEN** a 9x9 grid of empty input fields is displayed

### Requirement: Solve Button
The system SHALL provide a "Solve" button that triggers the solving process.

#### Scenario: Clicking solve
- **WHEN** the user enters numbers and clicks "Solve"
- **THEN** the grid data is sent to the backend and the results are updated in the grid fields
