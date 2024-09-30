from flask import Flask, request, send_from_directory, make_response

origin_state = [
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0],
]

ref = [
    [0,  1,  2,  3, 4, 5, 6],
    [7,  8,  9,  10, 11, 12, 13],
    [14, 15, 16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25, 26, 27],   
]

elements = [
    [
        [1, 7, 8, 14, 21],
        [0, 1, 2, 9, 10],
        [1, 8, 14, 15, 21],
        [0, 1, 8, 9, 10],
        [1, 2, 3, 7, 8],
        [0, 7, 8, 15, 22],
        [2, 3, 7, 8, 9],
        [0, 7, 14, 15, 22]
    ],
    [
        [0, 1, 2, 3, 7],
        [0, 1, 8, 15, 22],
        [3, 7, 8, 9, 10],
        [0, 7, 14, 21, 22],
        [0, 1, 7, 14, 21],
        [0, 1, 2, 3, 10],
        [1, 8, 15, 21, 22],
        [0, 7, 8, 9, 10]
    ],
    [
        [0, 1, 2, 3],
        [0, 7, 14, 21]
    ],
    [
        [0, 1, 8, 15, 16],
        [2, 7, 8, 9, 14],
        [0, 7, 8, 9, 16],
        [1, 2, 8, 14, 15]
    ],
    [
        [0, 7, 14, 15, 16],
        [0, 1, 2, 7, 14],
        [0, 1, 2, 9, 16],
        [2, 9, 14, 15, 16]
    ],
    [
        [0, 1, 2, 8, 15],
        [0, 7, 8, 9, 14],
        [1, 8, 14, 15, 16],
        [2, 7, 8, 9, 16]
    ],
    [
        [0, 2, 7, 8, 9],
        [0, 1, 7, 14, 15],
        [0, 1, 2, 7, 9],
        [0, 1, 8, 14, 15]
    ],
    [
        [0, 1, 7, 8, 14],
        [0, 1, 2, 8, 9],
        [1, 7, 8, 14, 15],
        [0, 1, 7, 8, 9],
        [0, 1, 2, 7, 8],
        [0, 1, 7, 8, 15],
        [1, 2, 7, 8, 9],
        [0, 7, 8, 14, 15]
    ],
    [
        [0, 7, 14, 15],
        [0, 1, 2, 7],
        [0, 1, 8, 15],
        [2, 7, 8, 9],
        [0, 1, 2, 9],
        [1, 8, 14, 15],
        [0, 7, 8, 9],
        [0, 1, 7, 14]
    ],
    [
        [1, 7, 8, 14],
        [0, 1, 8, 9],
        [1, 2, 7, 8],
        [0, 7, 8, 15]
    ]
]

solution = None

def canFitIn(cur_state, i, j, rotation):
    for k in rotation:
        j_offset = k % 7
        i_offset = int((k - j_offset) / 7)
        if i + i_offset > 7:
            return False
        if j + j_offset > 6:
            return False
        if cur_state[i + i_offset][j + j_offset] == 1:
            return False
    return True

def handleState(cur_state, filled_ele_rotation_indices, filled_ele_positions):
    global solution
    if solution != None:
        return
    if len(filled_ele_rotation_indices) == len(elements):
        print("found!")
        print(filled_ele_rotation_indices)
        print(filled_ele_positions)
        solution = {
            "rotation_indices": filled_ele_rotation_indices.copy(),
            "positions": filled_ele_positions.copy()
        }
        return
    cur_ele_rotations = elements[len(filled_ele_rotation_indices)]
    for rotation_index in range(0, len(cur_ele_rotations)):
        for i in range(0, 8):
            for j in range(0, 7):
                rotation = cur_ele_rotations[rotation_index]
                if canFitIn(cur_state, i, j, rotation):
                    for k in rotation:
                        j_offset = k % 7
                        i_offset = int((k - j_offset) / 7)
                        cur_state[i + i_offset][j + j_offset] = 1
                    filled_ele_rotation_indices.append(rotation_index)
                    filled_ele_positions.append(i * 7 + j)
                    handleState(cur_state, filled_ele_rotation_indices, filled_ele_positions)
                    for k in rotation:
                        j_offset = k % 7
                        i_offset = int((k - j_offset) / 7)
                        cur_state[i + i_offset][j + j_offset] = 0
                    filled_ele_rotation_indices.pop()
                    filled_ele_positions.pop()

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def register():
    global solution
    filled_indices = request.get_json()['filled_indices']
    print(filled_indices)
    solution = None
    result_rotation_indices = []
    result_positions = []
    origin_state_copy = []
    for i in origin_state:
        origin_state_copy.append(i.copy())
    for index in filled_indices:
        origin_state_copy[int((index - index % 7)/7)][index % 7] = 1
    handleState(origin_state_copy, result_rotation_indices, result_positions)
    return solution.copy()

@app.route('/init_data', methods=['GET'])
def get_init_data():
    return {
        "elements": elements,
        "origin_state": origin_state
    }

@app.route('/<file_name>', methods=['GET'])
def get_file(file_name):
    return make_response(
        send_from_directory("./front_end/dist", file_name)
    )

@app.route('/assets/<file_name>', methods=['GET'])
def get_assets_file(file_name):
    return make_response(
        send_from_directory("./front_end/dist/assets", file_name)
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7654, debug=True)
