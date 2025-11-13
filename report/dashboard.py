from fasthtml.common import *
import matplotlib.pyplot as plt
import pandas as pd

from employee_events.employee import Employee
from employee_events.team import Team
from employee_events.query_base import QueryBase

from utils import load_model


"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):

    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    def build_component(self, entity_id, model):
        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        self.label = model.name
        # Return the output from the parent class's build_component method
        return super().build_component(entity_id, model)

    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    def component_data(self, entity_id, model):
        return model.names_and_ids()


# Create a subclass of base_components/BaseComponent
# called `Header`
class Header(BaseComponent):

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    def build_component(self, entity_id, model):
        # Using the model argument for this method
        # return a fasthtml H1 objects containing the model's name attribute
        return H1(model.name.capitalize() + " Dashboard")


# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):

    # Overwrite the parent class's `visualization` method.
    # Use the same parameters as the parent
    def visualization(self, asset_id, model):
        # Pass the `asset_id` argument to the model's `event_counts` method
        df = model.event_counts(asset_id)

        # If empty return None so the parent handles empty case
        if df is None or df.empty:
            # Create an empty figure with a message
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No event data available", ha='center', va='center')
            return fig

        # Use the pandas .fillna method to fill nulls with 0
        df = df.fillna(0)

        # Use the pandas .set_index method to set the date column as the index
        df = df.set_index('date')

        # Sort the index
        df = df.sort_index()

        # Use the .cumsum method to change the data in the dataframe to cumulative counts
        cum = df[['positive', 'negative']].cumsum()

        # Set the dataframe columns to the list ['Positive', 'Negative']
        cum.columns = ['Positive', 'Negative']

        # Initialize a pandas subplot and assign the figure and axis
        fig, ax = plt.subplots(figsize=(8, 4))

        # call the .plot method for the cumulative counts dataframe
        cum.plot(ax=ax)

        # pass the axis variable to the `.set_axis_styling` method
        # set border color and font color to black
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')

        # Set title and labels for x and y axis
        ax.set_title('Cumulative Positive vs Negative Events')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Count')

        return fig


# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
class BarChart(MatplotlibViz):
    # Create a `predictor` class attribute assigned to load_model()
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    def visualization(self, asset_id, model):
        # Using the model and asset_id arguments pass the `asset_id` to the `.model_data` method
        X = model.model_data(asset_id)

        # Using the predictor class attribute pass the data to the `predict_proba` method
        try:
            probs = self.predictor.predict_proba(X)
        except Exception:
            # If the model doesn't support predict_proba, try predict and wrap
            p = float(self.predictor.predict(X)[0])
            probs = [[1 - p, p]]

        # Index the second column of predict_proba output
        probs = pd.np.array(probs)[:, 1] if hasattr(pd, "np") else __import__("numpy").array(probs)[:, 1]

        # If the model's name attribute is "team" we visualize the mean
        if getattr(model, "name", "") == "team":
            pred = float(probs.mean())
        else:
            pred = float(probs[0]) if len(probs) > 0 else 0.0

        # Initialize a matplotlib subplot
        fig, ax = plt.subplots(figsize=(6, 2))

        # Run the following code unchanged (bar drawing)
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20, pad=20)

        # pass the axis variable to the `.set_axis_styling` method
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')


        return fig


# Create a subclass of combined_components/CombinedComponent
# called Visualizations
class Visualizations(CombinedComponent):
    # Set the children class attribute to a list containing instances of LineChart and BarChart
    children = [LineChart(), BarChart()]

    # Leave this line unchanged
    outer_div_type = Div(cls='grid')


# Create a subclass of base_components/DataTable
# called `NotesTable`
class NotesTable(DataTable):

    def component_data(self, entity_id, model):
        notes = model.notes(entity_id)

        # If the model returns a list of dicts, convert to DataFrame
        if isinstance(notes, list):
            return pd.DataFrame(notes)

        # If already a DataFrame, return as is
        return notes



class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection")
    ]


# Create a subclass of CombinedComponents called `Report`
class Report(CombinedComponent):
    # Set the children to header, filters, visualizations, and notes
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]


# Initialize a fasthtml app
app = FastHTML()

# Initialize the Report class
report = Report()


# Create a route for a get request for the root
@app.get("/")
def index():
    # Call the initialized report: pass integer 1 and Employee model instance
    content = report.call_children(1, Employee())
    return report.outer_div(content, {})


# Create a route for an employee page
@app.get("/employee/{employee_id}")
def employee_page(employee_id: str):
    eid = int(employee_id)
    content = report.call_children(eid, Employee())
    return report.outer_div(content, {})


# Create a route for a team page
@app.get("/team/{team_id}")
def team_page(team_id: str):
    tid = int(team_id)
    content = report.call_children(tid, Team())
    return report.outer_div(content, {})


# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()
