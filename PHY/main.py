import flask
from flask.wrappers import Response
from API import API
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io

# build the base application
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# flask template

global picture
picture = Figure()


@app.route('/calculate', methods=['POST'])
def calculate():
    if flask.request.method == 'POST':
        # data initailization
        a = None
        print(flask.request.json)
        params = flask.request.form
        
        drag_coefficient = 0.47 if params.get('drag_coefficient') == '' or params.get('drag_coefficient') is None else float(params.get('drag_coefficient'))
        projectile_radius = 0.05 if params.get('projectile_radius') == '' or params.get('projectile_radius') is None else float(params.get('projectile_radius'))
        mass = 0.2 if params.get('mass') == '' or params.get('mass') is None else float(params.get('mass'))
        air_density = 1.28 if params.get('air_density') == '' or params.get('air_density') is None else float(params.get('air_density'))
        gravity_acceleration = 9.81 if params.get('gravity_acceleration') == '' or params.get('gravity_acceleration') is None else float(params.get('gravity_acceleration'))
        initial_speed = 50 if params.get('initial_speed') == '' or params.get('initial_speed') is None else float(params.get('initial_speed'))      
        launch_angle = 65 if params.get('launch_angle') == '' or params.get('launch_angle') is None else float(params.get('launch_angle'))
        clear_rander = False if params.get('clear_rander') == '' or params.get('clear_rander') is None else bool(flask.request.form.getlist('clear_rander')[0] == 'on')
        
        print(flask.request.form.getlist('clear_rander'))
        
        a = API(drag_coefficient,
                        projectile_radius,
                        mass,
                        air_density,
                        gravity_acceleration,
                        initial_speed,
                        launch_angle,
                        clear_rander)
  
        max_height = a.get_MaxHeight()
        max_length = a.get_length()
        timestamp = a.getTime2Ground()
        getTime2HeightPoints = a.getTime2HeightPoints()

        
        print('Maximum height, zmax = {:.2f} m'.format(a.get_MaxHeight()))
        print('Range to target, xmax = {:.2f} m'.format(a.get_length()))
        print('Time to target = {:.2f} s'.format(a.getTime2Ground()))
        print('Time to highest point = {:.2f} s'.format(
            a.getTime2HeightPoints()))

        global picture
        picture = a.getFig()

        return flask.render_template('cala.html', max_length = max_length, max_height = max_height, timestamp = timestamp, getTime2HeightPoints = getTime2HeightPoints)
    else:
        return Response("Http request error", status=403)


@app.route('/plot.png')
def plot_png():
    global picture
    output = io.BytesIO()
    plt.savefig(output, format='png')
    return Response(output.getvalue(), mimetype="image/png")

@app.route('/')
def index():
    plt.close()
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
