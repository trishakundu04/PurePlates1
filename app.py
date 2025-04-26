from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the CSV into memory
DATA_FILE = 'PurePlates.csv'
df = pd.read_csv(DATA_FILE)

# Convert column names to clean format
df.columns = [col.strip().replace(" ", "_").upper() for col in df.columns]


@app.route('/foods', methods=['GET'])
def get_all_foods():
    return jsonify(df.to_dict(orient='records'))


@app.route('/food/<string:name>', methods=['GET'])
def get_food(name):
    food = df[df['FOOD_PRODUCT'].str.lower() == name.lower()]
    if not food.empty:
        return jsonify(food.to_dict(orient='records')[0])
    return jsonify({"message": "Food not found"}), 404


@app.route('/food', methods=['POST'])
def add_food():
    data = request.get_json()
    global df
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return jsonify({"message": "Food added successfully"}), 201


@app.route('/food/<string:name>', methods=['PUT'])
def update_food(name):
    global df
    index = df[df['FOOD_PRODUCT'].str.lower() == name.lower()].index
    if not index.empty:
        for key in request.json:
            df.loc[index[0], key.upper()] = request.json[key]
        df.to_csv(DATA_FILE, index=False)
        return jsonify({"message": "Food updated successfully"})
    return jsonify({"message": "Food not found"}), 404


@app.route('/food/<string:name>', methods=['DELETE'])
def delete_food(name):
    global df
    index = df[df['FOOD_PRODUCT'].str.lower() == name.lower()].index
    if not index.empty:
        df = df.drop(index)
        df.to_csv(DATA_FILE, index=False)
        return jsonify({"message": "Food deleted successfully"})
    return jsonify({"message": "Food not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)