# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
In the final project, you will need to modify this file to implement your project.
"""
# built-in imports
import io
import pickle

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from werkzeug.wrappers.response import Response as WerkzeugResponse

# internal imports
import codeapp.models as models
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    # Get the data list
    data_list = get_data_list()
    # Calculate the statistics
    stats = calculate_statistics(data_list)
    # Render the home.html template with the stats
    return render_template("home.html", stats=stats)


@bp.get("/image")
def image() -> Response:
    # creating the plot
    fig = Figure()

    # TODO: populate the plot in this part of the code

    ################ START -  THIS PART MUST NOT BE CHANGED BY STUDENTS ################
    # create a string buffer to hold the final code for the plot
    output = io.StringIO()
    fig.savefig(output, format="svg")
    # output.seek(0)
    final_figure = prepare_figure(output.getvalue())
    return FlaskResponse(final_figure, mimetype="image/svg+xml")


@bp.get("/data")  # data route
def data() -> Response:
    # Get the data list
    data_list = get_data_list()
    # Convert the list of objects to a list of dictionaries
    data_dict_list = [item.__dict__ for item in data_list]
    # Render the data.html template with the data
    return render_template("data.html", data=data_dict_list)


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


################################## web service routes ##################################


@bp.get("/json-dataset")
def get_json_dataset() -> Response:
    # Get the data list
    data_list = get_data_list()
    # Convert the list of objects to a list of dictionaries
    data_dict_list = [item.__dict__ for item in data_list]
    # Return the list as a JSON response
    return jsonify(data_dict_list)


@bp.get("/json-stats")
def get_json_stats() -> Response:
    # Get the data list
    data_list = get_data_list()
    # Calculate the statistics
    stats = calculate_statistics(data_list)
    # Return the statistics as a JSON response
    return jsonify(stats)
