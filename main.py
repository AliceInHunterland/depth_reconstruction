import os

import elevation
from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask import send_file
from raster2xyz.raster2xyz import Raster2xyz

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")


@app.route("/target")
def target():
    lat1 = request.args.get('Lat1')
    lat2 = request.args.get('Lat2')
    lon1 = request.args.get('Lon1')
    lon2 = request.args.get('Lon2')
    bounds = ';'.join([lat1, lon1, lat2, lon2])

    return render_template('loading.html', my_data=bounds)


@app.route("/processing")
def processing():
    data = "No data was passed"
    if request.args.to_dict(flat=False)['data'][0]:
        data = str(request.args.to_dict(flat=False)['data'][0])
    print(data)
    if data == "No data was passed":
        return redirect(url_for('home'))
    data = data.split(';')
    data = [float(x) for x in data]
    bound = tuple(data)
    elevation.clip(bounds=bound, output=os.path.join(os.path.abspath(os.getcwd()), 'bounding.tif'))
    input_raster = os.path.join(os.path.abspath(os.getcwd()), 'bounding.tif')
    output_csv = os.path.join(os.path.abspath(os.getcwd()), 'bounding.csv')

    rtxyz = Raster2xyz()
    rtxyz.translate(input_raster, output_csv)

    return render_template('success.html', passed_data=data)


@app.route('/download')
def download():
    path = os.path.join(os.path.abspath(os.getcwd()), 'bounding.csv')
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    # app.run(debug=True, port=5000)#, ssl_context='adhoc')
    app.run(host='0.0.0.0', debug=True, port=5000)
