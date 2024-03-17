import dash
from dash import dcc, html, Input, Output
import numpy as np
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Real Estate Analysis Dashboard"),
    html.Div([
        html.Div([
            html.P(["The logic behind this app has been developed in 2 hours. The dashboard has been created with ChatGPT. It runs 10k Monte Carlo simulations to show the mean return of buy-vs-rent in CH. ", html.A("See the code", href="https://colab.research.google.com/drive/1s-47ZyorxBbOf_d2IdwigapsMHkOQnnK?usp=drive_link"), " to understand how it works. This server is slow. I suggest to download the code and run it locally"]),
            html.Label("Flat cost / annual rent"),
            dcc.Slider(id='rent-to-cost-slider', min=10, max=60, step=5, value=40),

            html.Label("Cost of Maintenance (%)"),
            dcc.Slider(id='percentage-of-maintenance-slider', min=0.005, max=0.05, step=0.005, value=0.01),

            html.Label("Duration of the simulation (yr)"),
            dcc.Slider(id='simulation-duration-slider', min=30, max=70, step=5, value=50),

            html.Label("Downpayment (%)"),
            dcc.Slider(id='downpayment-slider', min=0.05, max=1.0, step=0.05, value=0.2),

            html.Label("Debt never paid back (%)"),
            dcc.Slider(id='percentage-never-paid-slider', min=0.0, max=1.0, step=0.05, value=0.65),

            html.Label("Debt paid back (%)"),
            dcc.Slider(id='percentage-paid-slider', min=0.0, max=1.0, step=0.05, value=0.15),

            html.Label("Duration of Paid Debt (yr)"),
            dcc.Slider(id='duration-slider', min=10, max=30, step=5, value=15),

            html.Label("Fixed Interest Rate (%)"),
            dcc.Slider(id='interest-slider', min=0.01, max=0.05, step=0.005, value=0.02),

            html.H3("Gaussian distribution for return of flat value"),
            html.Label("Mean Return"),
            dcc.Slider(id='flat-mean-slider', min=0.01, max=0.05, step=0.005, value=0.02),

            html.Label("Sigma"),
            dcc.Slider(id='flat-sigma-slider', min=0.005, max=0.03, step=0.005, value=0.01),

            html.H3("Model for the return of the stock market (double Gaussian distribution)"),
            html.Label("Good Year Probability"),
            dcc.Slider(id='good-year-prob-slider', min=0.0, max=1.0, step=0.1, value=0.8),

            html.Label("Good Year Mean Return"),
            dcc.Slider(id='good-year-mean-slider', min=0.03, max=0.15, step=0.01, value=0.1),

            html.Label("Good Year Sigma"),
            dcc.Slider(id='good-year-sigma-slider', min=0.01, max=0.05, step=0.005, value=0.02),

            html.Label("Bad Year Mean Return"),
            dcc.Slider(id='bad-year-mean-slider', min=-0.15, max=-0.01, step=0.01, value=-0.08),

            html.Label("Bad Year Sigma"),
            dcc.Slider(id='bad-year-sigma-slider', min=0.01, max=0.05, step=0.005, value=0.02),
        ], style={"width": "40%"}),
        html.Div([
            # Plots
            dcc.Graph(id='plot1'),
            dcc.Graph(id='plot2')
        ], style={"width": "60%"})
    ], style={'display': 'flex', "width": '100%'})
])

# Define callback to update plots
@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure')],
    [Input('rent-to-cost-slider', 'value'),
     Input('percentage-of-maintenance-slider', 'value'),
     Input('simulation-duration-slider', 'value'),
     Input('downpayment-slider', 'value'),
     Input('percentage-never-paid-slider', 'value'),
     Input('percentage-paid-slider', 'value'),
     Input('duration-slider', 'value'),
     Input('interest-slider', 'value'),
     Input('flat-mean-slider', 'value'),
     Input('flat-sigma-slider', 'value'),
     Input('good-year-prob-slider', 'value'),
     Input('good-year-mean-slider', 'value'),
     Input('good-year-sigma-slider', 'value'),
     Input('bad-year-mean-slider', 'value'),
     Input('bad-year-sigma-slider', 'value')])
def update_plots(rent_to_cost, percentage_of_maintenance, simulation_duration,
                 downpayment, percentage_never_paid, percentage_paid, duration,
                 interest, flat_mean, flat_sigma, good_year_prob, good_year_mean,
                 good_year_sigma, bad_year_mean, bad_year_sigma):
    # Update plots based on slider values
    # Use the provided code to generate data and plots
    # Replace constants with slider values
    # Return updated figures for both plots

    # Use the provided code to generate data and plots
    # Replace constants with slider values
    # Return updated figures for both plots

    def calculate_paid_cost(i, value, year, durations=15):
    # French system
        return (year < duration) * value * i / (1 - 1/((1 + i)**duration))

    def calculate_never_paid_cost(i, value):
        return i*value

    def simulate_return_stock_market(gyp, gym, gys, bym, bys, years, simulations):

        is_good_year = np.random.rand(simulations, years) < gyp
        good_year_return = np.random.randn(simulations, years) * gys + gym
        bad_year_return = np.random.randn(simulations, years) * bys + bym

        return is_good_year * good_year_return + (1 - is_good_year) * bad_year_return

    def simulate_house_return(m, s, years, simulations):
        return np.random.randn(simulations, years) * s + m

    # Replace constants with slider values
    COST_OF_FLAT = 1000000
    NUM_OF_SIMULATIONS = 10000

    # Update parameters with slider values
    RENT_TO_COST = rent_to_cost
    PERCENTAGE_OF_MAINT = percentage_of_maintenance
    SIMULATION_DURATION = simulation_duration
    OUT_OF_POCKET = downpayment
    NEVER_PAID = percentage_never_paid
    PAID = percentage_paid
    DURATION = duration
    INTEREST = interest
    FLAT_MEAN = flat_mean
    FLAT_SIGMA = flat_sigma
    GOOD_YEAR_PROBABILITY = good_year_prob
    GOOD_YEAR_MEAN = good_year_mean
    GOOD_YEAR_SIGMA = good_year_sigma
    BAD_YEAR_MEAN = bad_year_mean
    BAD_YEAR_SIGMA = bad_year_sigma

    flat_value = COST_OF_FLAT * (1 + np.random.randn(NUM_OF_SIMULATIONS, SIMULATION_DURATION) * FLAT_SIGMA + FLAT_MEAN).cumprod(axis=1)
    rent_cost = flat_value / RENT_TO_COST
    paid_loan_repayment = np.ones((NUM_OF_SIMULATIONS, SIMULATION_DURATION)) * (calculate_paid_cost(INTEREST, COST_OF_FLAT * PAID, np.arange(SIMULATION_DURATION), DURATION))
    loan_cost = np.ones((NUM_OF_SIMULATIONS, SIMULATION_DURATION)) * calculate_never_paid_cost(INTEREST, COST_OF_FLAT * NEVER_PAID) + paid_loan_repayment
    paid_loan_remaining = (paid_loan_repayment[:, 0] * DURATION).reshape(-1, 1) - paid_loan_repayment.cumsum(axis=1)
    maint_cost = flat_value * PERCENTAGE_OF_MAINT
    rent_vs_buy_annual = loan_cost + maint_cost - rent_cost
    stocks_return = (simulate_return_stock_market(GOOD_YEAR_PROBABILITY, GOOD_YEAR_MEAN, GOOD_YEAR_SIGMA, BAD_YEAR_MEAN, BAD_YEAR_SIGMA, SIMULATION_DURATION, NUM_OF_SIMULATIONS) + 1).cumprod(axis=1)
    value_init_dep = COST_OF_FLAT * stocks_return * OUT_OF_POCKET

    # Too lazy to vectorize this
    value_annual_diff = np.ones((NUM_OF_SIMULATIONS, SIMULATION_DURATION))
    for i in range(NUM_OF_SIMULATIONS):
        value_annual_diff[i, :] = ((np.tril(np.ones((SIMULATION_DURATION, SIMULATION_DURATION)) * stocks_return[i, :].reshape(-1, 1)) / stocks_return[i, :]) * rent_vs_buy_annual[i, :]).sum(axis=1)

    buy_minus_rent = flat_value - NEVER_PAID * COST_OF_FLAT - paid_loan_remaining - value_init_dep - value_annual_diff

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=np.arange(SIMULATION_DURATION), y=rent_cost.mean(axis=0), mode='lines', name='Rent', line=dict(color='red')))
    fig1.add_trace(go.Scatter(x=np.arange(SIMULATION_DURATION), y=maint_cost.mean(axis=0), mode='lines', name='Maintenance', line=dict(color='blue')))
    fig1.add_trace(go.Scatter(x=np.arange(SIMULATION_DURATION), y=loan_cost.mean(axis=0), mode='lines', name='Loan', line=dict(color='purple')))
    fig1.add_trace(go.Scatter(x=np.arange(SIMULATION_DURATION), y=rent_vs_buy_annual.mean(axis=0), mode='lines', name='Owning minus Renting', line=dict(color='green')))
    fig1.update_layout(title="Costs Over Time",
                       xaxis_title="Years",
                       yaxis_title="CHF")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=np.arange(SIMULATION_DURATION), y=flat_value.mean(axis=0), mode='lines', name='Flat Value', line=dict(color='red')))
    fig2.add_trace(go.Scatter(x=np.arange(SIMULATION_DURATION), y=(NEVER_PAID * COST_OF_FLAT + paid_loan_remaining.mean(axis=0)), mode='lines', name='Total Debt', line=dict(color='blue')))
    fig2.add_trace(go.Scatter(x=np.arange(SIMULATION_DURATION), y=value_init_dep.mean(axis=0), mode='lines', name='Return if Downpayment Invested', line=dict(color='purple')))
    fig2.add_trace(go.Scatter(x=np.arange(SIMULATION_DURATION), y=value_annual_diff.mean(axis=0), mode='lines', name='Return on Difference in Case of Rent', line=dict(color='green')))
    fig2.add_trace(go.Scatter(x=np.arange(SIMULATION_DURATION), y=buy_minus_rent.mean(axis=0), mode='lines', name='Owning minus Renting', line=dict(color='orange')))
    fig2.update_layout(title="Returns Over Time",
                       xaxis_title="Years",
                       yaxis_title="CHF (millions)")

    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
