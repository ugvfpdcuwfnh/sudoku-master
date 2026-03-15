## 1. Backend Implementation

- [ ] 1.1 Install Flask dependency (`pip install Flask numpy`)
- [ ] 1.2 Create `app.py` and import `solve_recursive` from `legacy_logic.py`
- [ ] 1.3 Implement the `/solve` POST endpoint with input validation
- [ ] 1.4 Test the `/solve` endpoint using a sample Sudoku grid

## 2. Frontend Implementation

- [ ] 2.1 Create `templates/index.html` with a 9x9 grid of input fields
- [ ] 2.2 Add CSS to style the 9x9 grid (borders for 3x3 blocks)
- [ ] 2.3 Implement JavaScript to collect grid data and call the `/solve` API
- [ ] 2.4 Implement JavaScript to update the grid with the API response

## 3. Verification

- [ ] 3.1 Run the Flask app and verify the full end-to-end flow in a browser
- [ ] 3.2 Verify error handling for invalid or unsolvable puzzles
