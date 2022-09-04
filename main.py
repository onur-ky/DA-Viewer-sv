from flask import Flask
from flask import request
from flask import make_response
from flask_cors import CORS, cross_origin
from src.heatmap import heatmap_gen
from src.db_utils import get_db_connection
from src.coverage_csv import coverage_df_to_csv


app = Flask(__name__)
cors = CORS(app, resources={"/heatmap": {"origins": "*"}})


@app.route('/heatmap', methods = ['GET'])
@cross_origin(supports_credentials=True)
def sv_hm_table():
    if request.method == 'GET':
        pathway = request.args.get('pathway')
        group = request.args.get('group')
        
        client = get_db_connection()
        col =  client['pathways'][pathway]
        annodata = col.find_one({'group': group})
        html, css = heatmap_gen(annodata['annotation']['feature'])

    return {'html': html, 'style': css}


@app.route('/heatmap/csv', methods = ['GET'])
@cross_origin(supports_credentials=True)
def sv_hm_csv_download():
    if request.method == 'GET':
        pathway = request.args.get('pathway')
        group = request.args.get('group')

        client = get_db_connection()
        col =  client['pathways'][pathway]
        annodata = col.find_one({'group': group})
        csv_io =coverage_df_to_csv(annodata['annotation']['feature'])
        output = make_response(csv_io)
        output.headers['Content-Disposition'] = f'attachment; filename={pathway}_{group}.csv'
        output.headers["Content-type"] = "text/csv"
        return output


@app.route('/health', methods = ['GET'])
@cross_origin(supports_credentials=True)
def health():
    if request.method == 'GET':
        return {'status': 200}

def get_app():
    return app

