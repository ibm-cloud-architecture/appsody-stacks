from flask import Flask, redirect
from flasgger import Swagger
from server import app
from server.routes.prometheus import track_requests

# The python-flask stack includes the flask extension flasgger, which will build
# and publish your swagger ui and specification at the /apidocs url. Here we set up
# the basic swagger attributes, which you should modify to match you application.
# See: https://github.com/rochacbruno-archive/flasgger
swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "IBM GSE Cplex solve expose as Flask end point",
    "description": "API for solve, plus health/monitoring",
    "contact": {
      "responsibleOrganization": "IBM",
      "responsibleDeveloper": "Jerome Boyer",
      "email": "boyerje@us.ibm.com",
      "url": "https://ibm-cloud-architecture.github.com/refarch-eda",
    },
    "version": "0.1"
  },
  "schemes": [
    "http"
  ],
}
swagger = Swagger(app, template=swagger_template)

# The python-flask stack includes the prometheus metrics engine. You can ensure your endpoints
# are included in these metrics by enclosing them in the @track_requests wrapper.
@app.route('/solve')
@track_requests


@app.route('/optimize', methods=['POST'])
def optimize():
    # To include an endpoint in the swagger ui and specification, we include a docstring that
    # defines the attributes of this endpoint.
    """A hello message
    Example endpoint returning a hello message
    ---
    responses:
      200:
        description: A successful reply
        examples:
          text/plain: Hello from Appsody!
    """
    # initialize the optimizer and load reference data
    optimizer = VaccineOrderOptimizer(start_date=date(2020, 7, 6), debug=False)
    optimizer.load_data_csv("TC001")

    # Read json and convert to orders dataframe
    orders = pd.DataFrame(request.get_json(force=True))
    orders['RDD'] = pd.to_datetime(orders['RDD'], format='%m/%d/%Y')
    optimizer.optimize(orders)
    
    # post optimiztion
    print("\n  ".join(optimizer.log_msgs))
    return optimizer.get_sol_json()
 

# It is considered bad form to return an error for '/', so let's redirect to the apidocs
@app.route('/')
def index():
    return redirect('/apidocs')

# If you have additional modules that contain your API endpoints, for instance
# using Blueprints, then ensure that you use relative imports, e.g.:
# from .mymodule import myblueprint
