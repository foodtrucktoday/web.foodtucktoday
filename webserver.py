#  Copyright (c) 2020 Romain ODET
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import *

from model import Model

# Create flask application
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/index.html', methods=['GET', 'POST'])  # / is the URL
@app.route('/accueil/', methods=['GET', 'POST'])  # / is the URL
@app.route('/', methods=['GET', 'POST'])  # / is the URL
def index():
    with Model() as model:
        foodtruck = model.GetFoodtruckToday()  # call the sql request

    return render_template('index.html', foodtruck=foodtruck)  # display the result


@app.route('/day/', methods=['GET', 'POST'])  # / is the URL
def Day():
    with Model() as model:
        foodtruck = model.GetFoodtruckToday()  # call the sql request
    return render_template('day_result.html', foodtruck=foodtruck)  # display the result


@app.route('/day/<id>/', methods=['GET', 'POST'])  # / is the URL
def Day_Selector(id):
    with Model() as model:
        foodtruck = model.GetFoodtruckDay(id)  # call the sql request

    return render_template('day_result.html', foodtruck=foodtruck)  # display the result


@app.route('/places/<id>/', methods=['GET', 'POST'])  # / is the URL
def Places_Selector(id):
    with Model() as model:
        place = model.getPlace(id)
        print(place)
        foodtruck = model.GetFoodtruckPlace(id)  # call the sql request

    return render_template('place_result.html', foodtruck=foodtruck, place=place)  # display the result


@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')


# main application
if __name__ == '__main__':
    # under windows, there is a bug in a module which prevents the usage of debug=True
    # the bug should be fixed within days or weeks, but in the meantime do not enable debug
    app.run()
