import plotly.graph_objs as go
from sklearn.preprocessing import minmax_scale
from plotly.express.colors import sample_colorscale
from plotly.subplots import make_subplots

def plot_portfolios(portfolios):
    names = []
    portfolio_returns = []
    portfolio_volatilities = []
    sharpe_ratios = []

    for portfolio in portfolios:
        name = portfolio.name.title()
        portfolio_return, portfolio_volatility, sharpe_ratio = portfolio.expected_returns, portfolio.volatility, portfolio.sharpe_ratio

        names.append(name)
        portfolio_returns.append(portfolio_return)
        portfolio_volatilities.append(portfolio_volatility)
        sharpe_ratios.append(sharpe_ratio)

    # Create a subplot, you might add more plots in the future
    fig = make_subplots(rows=2, cols=1, subplot_titles=('<b>Portfolio Performance</b>', '<b>Asset Weights</b>'))

    title = '<b>Portfolio Optimization Comparison</b>'

    # Create a dropdown menu
    dropdown_menu = []
    annotations = []
    dropdown_menu.append(dict(
        label='All Portfolios',
        method='update',
        args=[{'visible': [True] * len(portfolios)},
              {'title': f'{title}<br><i>All Portfolios<i>'},
              ]))

   # Create text and hovertext for the scatter plot
    text = [f'<b>{name}</b>' for name in names]
    hovertext = [f'<b>{name}</b><br><i>Expected Return:</i> {ret:.1%}<br><i>Volatility:</i> {vol:.1%}<br><b><i>Sharpe Ratio:</i></b> <b>{sr:.2f}</b>'
                for name, ret, vol, sr in zip(names, portfolio_returns, portfolio_volatilities, sharpe_ratios)]
    
    colorscale = 'Portland'  # Specify the desired colorscale
    colors = sample_colorscale(colorscale, minmax_scale(sharpe_ratios, (0,1))) # type: ignore

    for i, portfolio in enumerate(portfolios):
        # Create a scatter plot
        scatter = go.Scatter(x=portfolio_volatilities,
                            y=portfolio_returns,
                            mode='markers+text',
                            text=text,
                            hovertext=hovertext,
                            hovertemplate='%{hovertext}<extra></extra>',
                            textposition='bottom center',
                            marker=dict(
                                size=15,
                                color=sharpe_ratios,
                                colorscale=colorscale,
                                showscale=True,
                                colorbar=dict(
                                    title='Sharpe Ratio',
                                    titlefont=dict(size=14),
                                    tickformat='.2f',
                                ),
                                line=dict(
                                    color='DarkSlateGrey',
                                    width=0.5
                                ),
                            ),
                            name='Portfolios Performance')
        fig.add_trace(scatter, row=1, col=1)
        
    for i, portfolio in enumerate(portfolios):
        # Create a dropdown menu for each portfolio
        visible = [False] * len(portfolios)  # Initially, set all traces to invisible
        visible[i] = True  # Set the selected portfolio trace to visible

        dropdown_menu.append(dict(
            label=portfolio.name, 
            method='update', 
            args=[
                {'visible': visible},
                {'title': f'{title}<br><i>{portfolio.name}<i>',
                 # TODO: Dynamic annotations or Subplot titles?
                 'annotations': [go.layout.Annotation(
                                    text=hovertext[i],
                                    showarrow=False,
                                    x=1,  # X-coordinate of the annotation
                                    y=0.50,  # Y-coordinate of the annotation
                                    xref='paper',  # Reference the x-coordinate to the paper (layout) coordinates
                                    yref='paper',  # Reference the y-coordinate to the paper (layout) coordinates
                                    font=dict(color=colors[i])  # Customize the font color of the annotation
                                )]
                }
            ]))

        # Create a bar chart
        asset_weights = portfolio.clean_weights
        asset_names = list(asset_weights.keys())
        asset_values = list(asset_weights.values())

        bar_chart = go.Bar(x=asset_names, y=asset_values, 
                           marker_color=colors[i],
                           name=f'Asset Weights for {portfolio.name}')
        fig.add_trace(bar_chart, row=2, col=1)

    fig.update_layout(
        title=f'{title}<br><i>All Portfolios<i>',
        autosize=True,
        plot_bgcolor='rgb(243, 243, 243)',
        paper_bgcolor='rgb(243, 243, 243)',
        font=dict(
            family='Arial',
            size=12,
            color='black'
        ),
        showlegend=False,
        updatemenus=[dict(
            buttons=dropdown_menu,
            direction="down",
            pad={"r": 0, "t": 0},
            showactive=True,
            x=0.13,
            y=0.50,
        )]
    )

    x_range, y_range = zoom(portfolio_returns, portfolio_volatilities, 50)

    # Update the layout with the new zoomed ranges
    fig.update_layout(
        xaxis=dict(range=x_range),
        yaxis=dict(range=y_range)
    )

    # Add a grid and axis line customization for the first subplot
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray', zeroline=False, title_text='Volatility (Standard Deviation)', tickformat='.1%', tickfont=dict(size=10), row=1, col=1)
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray', zeroline=False, title_text='Expected Returns', tickformat='.1%', tickfont=dict(size=10), row=1, col=1)
    
    # Add a grid and axis line customization for the second subplot
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray', zeroline=False, title_text='Asset Names', row=2, col=1)
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray', zeroline=False, title_text='Asset Weights', tickformat='.1%', row=2, col=1)

    # Move the title to the right
    fig.update_layout(title_x=0.475, title_y=0.95)

    fig.show()

def zoom(portfolio_returns, portfolio_volatilities, zoom_percent):
    x_max = max(portfolio_volatilities)
    y_max = max(portfolio_returns)
    x_min = min(portfolio_volatilities)
    y_min = min(portfolio_returns)

    zoom_percent = zoom_percent # Adjust the zoom level here

    # Calculate the percentage values based on the data range
    x_range_percent = (x_max - x_min) * zoom_percent / 100
    y_range_percent = (y_max - y_min) * zoom_percent / 100

    # Calculate the new zoomed ranges
    x_range = [x_min - x_range_percent, x_max + x_range_percent]
    y_range = [y_min - y_range_percent, y_max + y_range_percent]
    return x_range,y_range
