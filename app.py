# app.py
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------
# Load and clean data
# ----------------------------
df = pd.read_excel('data/sales.xlsx', sheet_name='Sales Report')
df.columns = df.columns.str.strip()

# Fix European decimal commas
for col in ['Product Price', 'Order Quantity', 'Order Total']:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

# Parse dates with explicit format to avoid ambiguity and deprecation warning
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%y')

# Filter out Cancelled orders for KPIs and most charts
df_active = df[df['Order Status'] != 'Cancelled']

# Compute KPIs
total_sales = df_active['Order Total'].sum()
total_quantity = df_active['Order Quantity'].sum()
avg_order_value = df_active['Order Total'].mean()
total_orders = len(df_active)
unique_customers = df_active['Customer ID'].nunique()

# ----------------------------
# Prepare monthly sales data (as datetime, NOT Period)
# ----------------------------
df_active['Month'] = df_active['Order Date'].dt.to_period('M').dt.start_time
monthly_sales = df_active.groupby('Month', as_index=False)['Order Total'].sum()

# ----------------------------
# Initialize Dash app
# ----------------------------
app = dash.Dash(__name__)
app.title = "Bicycle Sales Dashboard"

# ----------------------------
# App Layout
# ----------------------------
app.layout = html.Div(
    style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H1("🚴 Bicycle Sales Analysis Dashboard", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),

        # KPI Cards
        html.Div([
            html.Div([
                html.H4("Total Sales", style={'margin': '0', 'color': '#7f8c8d'}),
                html.H2(f"${total_sales:,.0f}", style={'margin': '10px 0 0', 'color': '#27ae60'})
            ], style={
                'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                'boxShadow': '0 2px 6px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1', 'margin': '0 10px'
            }),
            html.Div([
                html.H4("Total Quantity", style={'margin': '0', 'color': '#7f8c8d'}),
                html.H2(f"{total_quantity:,.0f}", style={'margin': '10px 0 0', 'color': '#2980b9'})
            ], style={
                'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                'boxShadow': '0 2px 6px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1', 'margin': '0 10px'
            }),
            html.Div([
                html.H4("Avg. Order Value", style={'margin': '0', 'color': '#7f8c8d'}),
                html.H2(f"${avg_order_value:,.2f}", style={'margin': '10px 0 0', 'color': '#8e44ad'})
            ], style={
                'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                'boxShadow': '0 2px 6px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1', 'margin': '0 10px'
            }),
            html.Div([
                html.H4("Total Orders", style={'margin': '0', 'color': '#7f8c8d'}),
                html.H2(f"{total_orders:,}", style={'margin': '10px 0 0', 'color': '#e67e22'})
            ], style={
                'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                'boxShadow': '0 2px 6px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1', 'margin': '0 10px'
            }),
            html.Div([
                html.H4("Unique Customers", style={'margin': '0', 'color': '#7f8c8d'}),
                html.H2(f"{unique_customers:,}", style={'margin': '10px 0 0', 'color': '#16a085'})
            ], style={
                'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                'boxShadow': '0 2px 6px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1', 'margin': '0 10px'
            }),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'flexWrap': 'wrap', 'marginBottom': '30px'}),

        # Row 1: Category & Region
        html.Div([
            dcc.Graph(
                figure=px.bar(
                    df_active.groupby('Product Category', as_index=False)['Order Total'].sum(),
                    x='Order Total', y='Product Category',
                    title='Sales by Product Category',
                    orientation='h',
                    color='Product Category',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    height=450
                ).update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
            ),
            dcc.Graph(
                figure=px.bar(
                    df_active.groupby('Product Region', as_index=False)['Order Total'].sum(),
                    x='Order Total', y='Product Region',
                    title='Sales by Region',
                    orientation='h',
                    color='Product Region',
                    color_discrete_sequence=px.colors.sequential.Magma,
                    height=450
                ).update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
            )
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '30px'}),

        # Row 2: Monthly Trend & Top Products
        html.Div([
            dcc.Graph(
                figure=px.line(
                    monthly_sales,
                    x='Month',
                    y='Order Total',
                    title='Monthly Sales Trend',
                    markers=True,
                    height=450
                ).update_traces(
                    line={'width': 3, 'color': '#3498db'},
                    marker={'size': 8, 'color': '#2980b9'}
                ).update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis_title='Month',
                    yaxis_title='Sales ($)'
                )
            ),
            dcc.Graph(
                figure=px.bar(
                    df_active.groupby('Product Name', as_index=False)['Order Total'].sum().nlargest(10, 'Order Total'),
                    x='Order Total', y='Product Name',
                    title='Top 10 Best-Selling Products',
                    orientation='h',
                    color='Order Total',
                    color_continuous_scale='Blues',
                    height=450
                ).update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    coloraxis_showscale=False
                )
            )
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '30px'}),

        # Row 3: Feedback & Payment/Shipping
        html.Div([
            dcc.Graph(
                figure=px.pie(
                    df_active,
                    names='Customer Feedback',
                    title='Customer Feedback Distribution',
                    color='Customer Feedback',
                    color_discrete_map={'Positive': '#27ae60', 'Neutral': '#bdc3c7', 'Negative': '#e74c3c'},
                    height=450
                ).update_traces(textinfo='percent+label')
            ),
            dcc.Graph(
                figure=go.Figure(data=[
                    go.Bar(
                        name='Payment Method',
                        x=df_active['Payment Method'].value_counts().index,
                        y=df_active['Payment Method'].value_counts().values,
                        marker_color='#3498db'
                    ),
                    go.Bar(
                        name='Shipping Method',
                        x=df_active['Shipping Method'].value_counts().index,
                        y=df_active['Shipping Method'].value_counts().values,
                        marker_color='#9b59b6'
                    )
                ]).update_layout(
                    title='Payment & Shipping Methods',
                    barmode='group',
                    height=450,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis_title='Method',
                    yaxis_title='Number of Orders'
                )
            )
        ], style={'display': 'flex', 'gap': '20px'})
    ]
)

# ----------------------------
# Run app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)