from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
import os, csv
import joblib
import pandas as pd
from collections import Counter

app = Flask(__name__)

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



kmeans = joblib.load('models/kmeans.pkl')
kmodes = joblib.load('models/kmodes.pkl')
rand_for = joblib.load('models/attack_detector.pkl')
xgb_clf = joblib.load('models/xgb_attack_detector.pkl')


label_map = {
    0: "Clean",
    1: "Label Flipping",
    2: "Add noise",
    3: "Shuffle Features",
    4: "Backdoor Data",
}

required_columns = ['having_IPhaving_IP_Address ', 'URLURL_Length ', 'Shortining_Service ',
       'having_At_Symbol ', 'double_slash_redirecting ', 'Prefix_Suffix ',
       'having_Sub_Domain ', 'SSLfinal_State ', 'Domain_registeration_length ',
       'Favicon ', 'port ', 'HTTPS_token ', 'Request_URL ', 'URL_of_Anchor ',
       'Links_in_tags ', 'SFH ', 'Submitting_to_email ', 'Abnormal_URL ',
       'Redirect ', 'on_mouseover ', 'RightClick ', 'popUpWidnow ', 'Iframe ',
       'age_of_domain ', 'DNSRecord ', 'web_traffic ', 'Page_Rank ',
       'Google_Index ', 'Links_pointing_to_page ', 'Statistical_report ',
       'Result']  

def analyze_predictions(predictions, label_map):
     # Count frequencies
    counts = Counter(predictions)
    total = len(predictions)

    # Convert to percentages and map to labels
    results = {}
    for label, count in counts.items():
        attack_name = label_map.get(label, f"Unknown({label})")
        results[attack_name] = round((count / total) * 100, 2)

    # Find majority attack type
    majority_attack = max(results, key=results.get)


    for attack, pct in results.items():
       print(f"{attack}: {pct}%")

    print(f"\nDataset classified as: {majority_attack}")
    
    return results, majority_attack



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part in request'}), 400

    files = request.files.getlist('files[]')
    saved_files = []
    all_file_results = []

    for file in files:
        if file.filename == '':
            continue

        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        saved_files.append(file.filename)

        # Read the dataset
        new_data = pd.read_csv(filepath)


        if all(col in new_data.columns for col in required_columns):
            selected_models = ['KMeans', 'KMode', 'RandomForest', 'XGBoost']
        else:
            selected_models = ['KMeans', 'KMode']

        # Run selected models
        model_predictions = {}

        if 'KMeans' in selected_models:
            model_predictions['KMeans'] = kmeans.predict(new_data)
        if 'KMode' in selected_models:
            model_predictions['KMode'] = kmodes.fit_predict(new_data)
        if 'RandomForest' in selected_models:
            model_predictions['RandomForest'] = rand_for.predict(new_data)
        if 'XGBoost' in selected_models:
            model_predictions['XGBoost'] = xgb_clf.predict(new_data)

        # Analyze and summarize model results
        all_model_results = {}
        all_pred_labels = []

        for model_name, predictions in model_predictions.items():
            results, majority = analyze_predictions(predictions, label_map)
            all_model_results[model_name] = {
                'results': results,
                'final_classification': majority
            }
            all_pred_labels.append(majority)

        # Determine overall classification
        final_classification = Counter(all_pred_labels).most_common(1)[0][0]

        # Merge and return results
       # merged_results = {model: data['results'] for model, data in all_model_results.items()}
        merged_results = {
            model: {
                "results": data["results"],
                "final_classification": data["final_classification"]
             }
            for model, data in all_model_results.items()
        }

        all_file_results.append({
            "file": file.filename,
            "results": merged_results,
            "final_classification": final_classification
        })

    return make_response(jsonify({
        'files': saved_files,
        'all_results': all_file_results,
    }), 200)




@app.route('/save-text', methods=['POST'])
def save_text():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    separator = data.get('separator')
    columns = data.get('columns')
    rows = data.get('data')

    if not separator or not columns or not rows:
        return jsonify({'error': 'Missing separator, columns, or data'}), 400

    # Validate row lengths
    for i, row in enumerate(rows):
        if len(row) != len(columns):
            return jsonify({'error': f'Row {i+1} has {len(row)} values but expected {len(columns)}'}), 400

    try:
        # Convert rows to DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Save CSV for record
        csv_filename = 'text_data.csv'
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        df.to_csv(csv_path, index=False)

        # Select models based on required columns
        if all(col in df.columns for col in required_columns):
            selected_models = ['KMeans', 'KMode', 'RandomForest', 'XGBoost']
        else:
            selected_models = ['KMeans', 'KMode']

        # Run models
        model_predictions = {}
        if 'KMeans' in selected_models:
            model_predictions['KMeans'] = kmeans.predict(df)
        if 'KMode' in selected_models:
            model_predictions['KMode'] = kmodes.fit_predict(df)
        if 'RandomForest' in selected_models:
            model_predictions['RandomForest'] = rand_for.predict(df)
        if 'XGBoost' in selected_models:
            model_predictions['XGBoost'] = xgb_clf.predict(df)

        # Analyze results
        all_model_results = {}
        all_pred_labels = []
        for model_name, predictions in model_predictions.items():
            results, majority = analyze_predictions(predictions, label_map)
            all_model_results[model_name] = {
                'results': results,
                'final_classification': majority
            }
            all_pred_labels.append(majority)

        final_classification = Counter(all_pred_labels).most_common(1)[0][0]
        #merged_results = {model: data['results'] for model, data in all_model_results.items()}
        merged_results = {
            model: {
                "results": data["results"],
                "final_classification": data["final_classification"]
            }
            for model, data in all_model_results.items()
        }

        return jsonify({
            'files': csv_filename,
            'results': merged_results,
            'final_classification': final_classification
        })

    except Exception as e:
        return jsonify({'error': f'Failed to save and analyze text: {str(e)}'}), 500

    

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)