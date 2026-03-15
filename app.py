from flask import Flask, request, jsonify, render_template
import numpy as np
from legacy_logic import solve_recursive

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    if not data or 'board' not in data:
        return jsonify({'error': 'No board data provided', 'status': 'error'}), 400
    
    try:
        board = np.array(data['board'])
        if board.shape != (9, 9):
            return jsonify({'error': 'Invalid board shape. Must be 9x9.', 'status': 'error'}), 400
        
        if not np.all((board >= 0) & (board <= 9)):
             return jsonify({'error': 'Invalid board values. Must be between 0 and 9.', 'status': 'error'}), 400

        solution = solve_recursive(board)
        
        if solution is not None:
            return jsonify({
                'solution': solution.tolist(),
                'status': 'ok'
            })
        else:
            return jsonify({
                'error': 'No solution found for this puzzle',
                'status': 'error'
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
