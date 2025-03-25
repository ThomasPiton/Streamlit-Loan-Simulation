import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd

# Seed for reproducibility
np.random.seed(42)

# Enhanced Data Generation
def generate_comprehensive_dataset():
    # Time series data
    x = np.linspace(0, 10, 200)
    
    # Multiple wave functions
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.tan(x)
    y4 = x**2
    
    # Categorical and numerical data
    categories = ['A', 'B', 'C', 'D']
    df = pd.DataFrame({
        'x': x,
        'Sine Wave': y1,
        'Cosine Wave': y2,
        'Tangent Wave': y3,
        'Quadratic': y4,
        'Category': np.random.choice(categories, len(x)),
        'Random Values': np.random.randn(len(x))
    })
    
    return df

# Create comprehensive dataset
df = generate_comprehensive_dataset()

# Advanced Visualization Functions
def create_interactive_line_chart():
    fig = go.Figure()
    
    # Add multiple traces with advanced styling
    traces = [
        ('Sine Wave', df['Sine Wave'], '#1E90FF'),
        ('Cosine Wave', df['Cosine Wave'], '#32CD32'),
        ('Tangent Wave', df['Tangent Wave'], '#FF4500'),
        ('Quadratic', df['Quadratic'], '#9400D3')
    ]
    
    for name, data, color in traces:
        fig.add_trace(go.Scatter(
            x=df['x'], 
            y=data, 
            mode='lines+markers', 
            name=name,
            line=dict(color=color, width=3),
            marker=dict(size=5, symbol='circle')
        ))
    
    fig.update_layout(
        title='Advanced Multi-Function Line Chart',
        xaxis_title='X Axis',
        yaxis_title='Y Values',
        hovermode='closest',
        template='plotly_white'
    )
    
    return fig

def create_advanced_bar_chart():
    # Grouped bar chart with error bars
    category_means = df.groupby('Category')['Random Values'].agg(['mean', 'std'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=category_means.index,
        y=category_means['mean'],
        error_y=dict(
            type='data', 
            array=category_means['std'],
            visible=True
        ),
        marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FDCB6E']
    ))
    
    fig.update_layout(
        title='Category Distribution with Error Bars',
        xaxis_title='Categories',
        yaxis_title='Mean Value',
        template='plotly_white'
    )
    
    return fig

def create_advanced_pie_chart():
    # Pie chart of category distribution
    category_counts = df['Category'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=category_counts.index, 
        values=category_counts.values,
        hole=0.3,  # Donut chart
        marker=dict(
            colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FDCB6E'],
            line=dict(color='#FFFFFF', width=2)
        )
    )])
    
    fig.update_layout(
        title='Category Distribution',
        template='plotly_white'
    )
    
    return fig

def create_advanced_heatmap():
    # Correlation heatmap
    correlation_matrix = df[['Sine Wave', 'Cosine Wave', 'Tangent Wave', 'Quadratic']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu_r',
        zmin=-1, 
        zmax=1
    ))
    
    fig.update_layout(
        title='Correlation Heatmap',
        template='plotly_white'
    )
    
    return fig

def create_advanced_scatter_plot():
    # 3D Scatter plot with color and size variation
    fig = go.Figure(data=[go.Scatter3d(
        x=df['Sine Wave'],
        y=df['Cosine Wave'],
        z=df['Quadratic'],
        mode='markers',
        marker=dict(
            size=5,
            color=df['Tangent Wave'],  # color by Tangent Wave
            colorscale='Viridis',
            opacity=0.8
        ),
        text=df['Category']  # hover text
    )])
    
    fig.update_layout(
        title='3D Scatter Plot with Multivariate Analysis',
        scene=dict(
            xaxis_title='Sine Wave',
            yaxis_title='Cosine Wave',
            zaxis_title='Quadratic'
        ),
        template='plotly_white'
    )
    
    return fig

def create_distribution_plot():
    # Violin plot of distributions
    fig = go.Figure()
    
    for column in ['Sine Wave', 'Cosine Wave', 'Tangent Wave', 'Quadratic']:
        fig.add_trace(go.Violin(
            x=[column] * len(df),
            y=df[column],
            name=column,
            box_visible=True,
            meanline_visible=True
        ))
    
    fig.update_layout(
        title='Distribution of Different Functions',
        xaxis_title='Function Type',
        yaxis_title='Value',
        template='plotly_white'
    )
    
    return fig

def generate_df():
    return pd.DataFrame({
    "x": np.linspace(0, 10, 100),
    "y1": np.sin(np.linspace(0, 10, 100)),
    "y2": np.cos(np.linspace(0, 10, 100)),
    "category": ["A", "B", "C", "D"] * 25})

# Advanced Line Chart
def create_line_chart():
    df = generate_df()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["x"], y=df["y1"], mode='lines+markers', name='Sine Wave', line=dict(width=3, color='#1E90FF')))
    fig.add_trace(go.Scatter(x=df["x"], y=df["y2"], mode='lines+markers', name='Cosine Wave', line=dict(width=3, color='#32CD32')))
    fig.update_layout(title='Advanced Line Chart', xaxis_title='X Axis', yaxis_title='Y Values', template='plotly_dark')
    return fig

# Advanced Bar Chart
def create_bar_chart():
    df = generate_df()
    category_means = df.groupby('category')['y1'].mean()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=category_means.index, y=category_means.values, marker=dict(color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FDCB6E'])))
    fig.update_layout(title='Category Distribution', xaxis_title='Categories', yaxis_title='Mean Value', template='plotly_dark')
    return fig

# Advanced Pie Chart
def create_pie_chart():
    df = generate_df()
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=["A", "B", "C", "D"], values=[10, 20, 30, 40], hole=0.4))
    fig.update_layout(title='Advanced Pie Chart', template='plotly_dark')
    return fig

# Advanced Heatmap
def create_heatmap():
    df = generate_df()
    heatmap_data = np.random.rand(10, 10)
    fig = go.Figure(data=go.Heatmap(z=heatmap_data, colorscale='Viridis'))
    fig.update_layout(title='Advanced Heatmap', template='plotly_dark')
    return fig

# Advanced Scatter Plot
def create_scatter_plot():
    df = generate_df()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["x"], y=df["y1"], mode='markers', marker=dict(size=12, color=df["y1"], colorscale='Plasma', showscale=True)))
    fig.update_layout(title='Advanced Scatter Plot', xaxis_title='X Axis', yaxis_title='Y Values', template='plotly_dark')
    return fig

# Advanced Candlestick Chart
def create_candlestick_chart():
    df = generate_df()
    stock_data = px.data.stocks()
    fig = go.Figure(data=[go.Candlestick(x=stock_data['date'], open=stock_data['GOOG'] - 10, high=stock_data['GOOG'] + 10, low=stock_data['GOOG'] - 20, close=stock_data['GOOG'])])
    fig.update_layout(title='Advanced Candlestick Chart', template='plotly_dark')
    return fig

def create_treemap():
    treemap_data = px.data.tips()
    fig = px.treemap(treemap_data, path=['day', 'sex'], values='total_bill', color='total_bill', color_continuous_scale='Blues')
    fig.update_layout(title='Advanced Treemap', template='plotly_dark')
    return fig

def create_3d_surface():
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
    fig.update_layout(title='Advanced 3D Surface Plot', scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Values'
    ), template='plotly_dark')

    return fig

def create_crypto_treemap():
    # Sample data similar to crypto market capitalization
    crypto_data = {
        "Coin": ["Bitcoin", "Ethereum", "Binance Coin", "Cardano", "Solana", "XRP", "Polkadot", "Dogecoin", "Chainlink"],
        "Market Cap": [800_000_000_000, 400_000_000_000, 100_000_000_000, 50_000_000_000, 45_000_000_000, 40_000_000_000, 30_000_000_000, 25_000_000_000, 10_000_000_000],
        "Volume (24h)": [30_000_000_000, 20_000_000_000, 5_000_000_000, 2_000_000_000, 1_500_000_000, 1_200_000_000, 1_000_000_000, 900_000_000, 700_000_000],
        "Category": ["Top 10", "Top 10", "Top 10", "Top 10", "Top 10", "Top 10", "Top 10", "Top 10", "Top 10"]
    }
    
    df = pd.DataFrame(crypto_data)
    
    # Treemap with Market Cap as values, using Volume for color intensity
    fig = px.treemap(df, path=['Category', 'Coin'], values='Market Cap', color='Volume (24h)', 
                     color_continuous_scale='Viridis', hover_data=['Market Cap', 'Volume (24h)'])
    
    fig.update_layout(
        title='Crypto Market Treemap',
        template='plotly_dark',
        font=dict(size=14),
        margin=dict(t=50, l=25, r=25, b=25)
    )
    
    return fig

def create_line_chart2():
    df = generate_df()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["x"], y=df["y1"], mode='lines+markers', name='Sine Wave', line=dict(width=3, color='#1E90FF')))
    fig.add_trace(go.Scatter(x=df["x"], y=df["y2"], mode='lines+markers', name='Cosine Wave', line=dict(width=3, color='#32CD32')))
    fig.update_layout(
        title='Advanced Line Chart',
        xaxis_title='X Axis',
        yaxis_title='Y Values',
        template='plotly_dark',
        height=250,  # Reduced height for better space usage
        width=1000,
        margin=dict(t=20, b=20, l=20, r=20),  # Minimized margins
        font=dict(size=10),  # Smaller font size for labels
        showlegend=True,  # Enable legend for clarity
        autosize=True,  # Adjust automatically based on content
    )
    return fig





# Main Streamlit App
def main():
    st.title('Plotly - Advanced Visualization Dashboard')
    
    # Create tabs
    tabs = st.tabs([
        "Line Chart",
        "Bar Chart", 
        "Pie Chart", 
        "Correlation Heatmap", 
        "3D Scatter Plot", 
        "Distribution Analysis",
        "Line Chart 2",
        "Bar Chart 2",
        "Pie Chart 2",
        "Heatmap 2",
        "scatter plot 2",
        "candlestick chart 2", 
        "Treemap",
        "3D Surface",
        "Crypto Tream Map",
    ])
    
    # Populate tabs with visualizations
    with tabs[0]:
        st.plotly_chart(create_interactive_line_chart(), use_container_width=True)
    
    with tabs[1]:
        st.plotly_chart(create_advanced_bar_chart(), use_container_width=True)
    
    with tabs[2]:
        st.plotly_chart(create_advanced_pie_chart(), use_container_width=True)
    
    with tabs[3]:
        st.plotly_chart(create_advanced_heatmap(), use_container_width=True)
    
    with tabs[4]:
        st.plotly_chart(create_advanced_scatter_plot(), use_container_width=True)
    
    with tabs[5]:
        st.plotly_chart(create_distribution_plot(), use_container_width=True)
        
    with tabs[6]:
        st.plotly_chart(create_line_chart(), use_container_width=True)
        
    with tabs[7]:
        st.plotly_chart(create_bar_chart(), use_container_width=True)
        
    with tabs[8]:
        st.plotly_chart(create_pie_chart(), use_container_width=True)
        
    with tabs[9]:
        st.plotly_chart(create_heatmap(), use_container_width=True)
        
    with tabs[10]:
        st.plotly_chart(create_scatter_plot(), use_container_width=True)
        
    with tabs[11]:
        st.plotly_chart(create_candlestick_chart(), use_container_width=True)
        
    with tabs[12]:
        st.plotly_chart(create_treemap(), use_container_width=True)
        
    with tabs[13]:
        st.plotly_chart(create_3d_surface(), use_container_width=True)
        
    with tabs[14]:
        st.plotly_chart(create_crypto_treemap(), use_container_width=True)
        
    col1, col2, col3, col4, col5 = st.columns(5)

    # Display 5 charts horizontally
    with col1:
        st.plotly_chart(create_line_chart2(), use_container_width=False, key="chart_1")
    with col2:
        st.plotly_chart(create_line_chart2(), use_container_width=False,key="chart_2")
    with col3:
        st.plotly_chart(create_line_chart2(), use_container_width=False,key="chart_3")
    with col4:
        st.plotly_chart(create_line_chart2(), use_container_width=False,key="chart_4")
    with col5:
        st.plotly_chart(create_line_chart2(), use_container_width=False , key="chart_5")
        
    col1, col2, col3 = st.columns(3)

    # Display 5 charts horizontally
    with col1:
        st.plotly_chart(create_line_chart2(), use_container_width=True, autosize=True, key="chart_6")
        st.plotly_chart(create_line_chart2(), use_container_width=True, autosize=True, key="chart_7")
        st.plotly_chart(create_line_chart2(), use_container_width=True, autosize=True, key="chart_8")
    with col2:
        st.plotly_chart(create_line_chart2(), use_container_width=True, autosize=True, key="chart_9")
        st.plotly_chart(create_line_chart2(), use_container_width=True, autosize=True, key="chart_10")
        st.plotly_chart(create_line_chart2(), use_container_width=True, autosize=True, key="chart_11")
    with col3:
        st.plotly_chart(create_line_chart2(), use_container_width=True, autosize=True, key="chart_12")
        st.plotly_chart(create_line_chart2(), use_container_width=True, autosize=True, key="chart_13")
        st.plotly_chart(create_line_chart2(), use_container_width=True, autosize=True, key="chart_14")
  
        
main()
