from wsgiref import simple_server
from flask import Flask, request, render_template, send_file
from flask import Response
import os
import pandas as pd
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('homepage.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.method == 'POST':
            f = request.files['file']
            df = pd.read_excel(f, engine='openpyxl')
            df.drop(['Unnamed: 0'], axis=1, inplace=True)
            df.to_csv(r'Prediction_Batch_files\fraudDetection_021119920_010220.csv', index = None, header=True)
            path = "Prediction_Batch_files"
            pred_val = pred_validation(path)  # object initialization
            pred_val.prediction_validation() #calling the prediction_validation function
            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path = pred.predictionFromModel()

            return render_template('result.html')

    except ValueError:
        return Response("Error1 Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error2 Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error3 Occurred! %s" %e)


@app.route('/download')
def downloadResult():
    p = 'Prediction_Output_File/Predictions.csv'
    return send_file(p, as_attachment=True)

# @app.route("/train", methods=['POST'])
# @cross_origin()
# def trainRouteClient():
#
#     try:
#         if request.json['folderPath'] is not None:
#             f = request.files['file']
#             df = pd.read_excel(f, engine='openpyxl')
#             df.drop(['Unnamed: 0'], axis=1, inplace=True)
#             df.to_csv(r'Prediction_Batch_files\fraudDetection_021119920_010220.csv', index=None, header=True)
#             path = "Prediction_Batch_files"
#             train_valObj = train_validation(path) #object initialization
#
#             train_valObj.train_validation()#calling the training_validation function
#
#
#             trainModelObj = trainModel() #object initialization
#             trainModelObj.trainingModel() #training the model for the files in the table
#
#
#     except ValueError:
#
#         return Response("Error Occurred! %s" % ValueError)
#
#     except KeyError:
#
#         return Response("Error Occurred! %s" % KeyError)
#
#     except Exception as e:
#
#         return Response("Error Occurred! %s" % e)
#     return Response("Training successfull!!")

port = int(os.getenv("PORT",5001))
if __name__ == "__main__":
    app.run(port=port)
