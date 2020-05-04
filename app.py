from flask import Flask, render_template, request

######## Подготовка данных для FLASK
from numpy.random import default_rng
import data
tours = data.tours
departures = data.departures
main_title = data.title
main_subtitle = data.subtitle
main_description = data.description

def get_datalist(tours, tag, ids=[]):
    lst = []
    if ids == []:
        ids = list(tours.keys())
    for i in ids:
        lst.append(tours[i][tag])
    return lst

def get_departures(tours, departure):
    d = {}
    for i, t in enumerate(tours.values()):
        if t["departure"] == departure:
            d[i+1] = t
    return d


############# FLASK
app = Flask(__name__)     # объявим экземпляр фласка

@app.route('/')   # роут главной
def render_main():
    rng = default_rng()
    indices = rng.choice(range(1, len(tours) + 1), size=6, replace=False)
    return render_template('index.html',
                           departures=departures,
                           main_title=main_title,
                           main_subtitle=main_subtitle,
                           main_description=main_description,
                           titles=get_datalist(tours, "title", indices),
                           descriptions=get_datalist(tours, "description", indices),
                           pictures=get_datalist(tours, "picture", indices),
                           ids=list(indices))

@app.route('/departures/<departure>') # роут направления
def render_departures(departure):
    d = get_departures(tours, departure)
    return render_template('departure.html',
                           n=len(d),
                           main_title=main_title,
                           departure=departure,
                           departures=departures,
                           prices=get_datalist(d, "price"),
                           nights=get_datalist(d, "nights"),
                           titles=get_datalist(d, "title"),
                           descriptions=get_datalist(d, "description"),
                           pictures=get_datalist(d, "picture"),
                           ids=list(d.keys()))

@app.route('/tours/<int:id>')  # роут тура
def render_tours(id):
    ids = [id]
    return render_template('tour.html',
                           main_title=main_title,
                           departures=departures,
                           title=get_datalist(tours, "title", ids)[0],
                           country=get_datalist(tours, "country", ids)[0],
                           nights=get_datalist(tours, "nights", ids)[0],
                           description=get_datalist(tours, "description", ids)[0],
                           price=get_datalist(tours, "price", ids)[0],
                           picture=get_datalist(tours, "picture", ids)[0]
                           )

app.run(debug = True)  # запустим сервер