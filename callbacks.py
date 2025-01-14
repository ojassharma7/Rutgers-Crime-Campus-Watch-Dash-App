import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash import html

# Define callback to update the density map and top crimes chart
def update_figures(df, crime_type, status, start_date, end_date, mapbox_access_token):
    # Filter the DataFrame based on selected criteria
    filtered_df = df.copy()
    if crime_type:
        filtered_df = filtered_df[filtered_df['Nature'].isin(crime_type)]
    if status and status != 'All':
        filtered_df = filtered_df[filtered_df['Disposition'] == status]
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Report Date'] >= start_date) & (filtered_df['Report Date'] <= end_date)]
    
    # Group by area name and calculate the count of crimes in each area
    area_counts = filtered_df.groupby(['General Location']).size().reset_index(name='Crime Count')
    total_crimes = area_counts['Crime Count'].sum()
    
    # Calculate the percentage of crimes in each area
    area_counts['Percentage'] = (area_counts['Crime Count'] / total_crimes) * 100
    
    # Merge area counts with the filtered DataFrame to get the area information for each data point
    merged_df = pd.merge(filtered_df, area_counts, on='General Location', how='left')
    
    # Create custom hover text with area name, crime count, and percentage of crimes
    hover_text = merged_df.apply(lambda row: f"{row['General Location']}<br>" \
                                              f"Crime Count: {row['Crime Count']}<br>" \
                                              f"Percentage: {row['Percentage']:.2f}%", axis=1)
    
    # Create the density map using Plotly Express
    density_fig = px.density_mapbox(merged_df, lat='latitude', lon='longitude', radius=10,
                                     center=dict(lat=40.5, lon=-74.45), zoom=11,
                                     mapbox_style="dark", custom_data=['Nature', 'Disposition', 'Report Date', 'General Location', 'Crime Count', 'Percentage'],
                                     color_continuous_scale='Reds', hover_name='General Location', hover_data=['Nature', 'Disposition', 'Report Date'],
                                     )
    
    density_fig.update_traces(hovertemplate='<b>%{customdata[3]}</b><br>' \
                                             'Nature: %{customdata[0]}<br>' \
                                             'Disposition: %{customdata[1]}<br>' \
                                             'Report Date: %{customdata[2]}<br>' \
                                             'Crime Count: %{customdata[4]}<br>' \
                                             'Percentage: %{customdata[5]:.2f}%'
                              )
    
    density_fig.update_layout(
        mapbox_accesstoken=mapbox_access_token,
        margin=dict(l=0, r=0, t=5, b=0),  # Adjust margins
        paper_bgcolor='#1E1E1E',  # Background color
        font=dict(color='#FFFFFF')  # Font color
    )
    
    # Create the top crimes chart
    top_crimes_df = filtered_df['Nature'].value_counts().reset_index().head(12)
    top_crimes_df.columns = ['Crime Type', 'Count']
    top_crimes_fig = px.bar(top_crimes_df, x='Crime Type', y='Count', color='Count', labels={'Count': 'Crime Count'}, color_continuous_scale='Reds')
    top_crimes_fig.update_layout(
        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',
        font=dict(color='#FFFFFF'),
        xaxis=dict(title='Crime Type'),
        yaxis=dict(title='Crime Count'),
        coloraxis_showscale=False
    )
    
    return density_fig, top_crimes_fig
# Define callback to display data summary statistics
def display_data_summary(df, crime_type, status, start_date, end_date):
    # Filter the DataFrame based on selected criteria
    filtered_df = df.copy()
    if crime_type:
        filtered_df = filtered_df[filtered_df['Nature'].isin(crime_type)]  # Filter using isin for multi-select
    if status and status != 'All':
        filtered_df = filtered_df[filtered_df['Disposition'] == status]
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Report Date'] >= start_date) & (filtered_df['Report Date'] <= end_date)]
    
    # Calculate total number of crimes
    total_crimes = len(filtered_df)
    
    # Calculate average crime rate per day
    if start_date and end_date:
        num_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
        avg_crime_rate = total_crimes / num_days
    else:
        avg_crime_rate = 0

    # Calculate most frequent crime type
    most_frequent_crime = filtered_df['Nature'].mode().iloc[0] if not filtered_df.empty else "N/A"

    # Create a text summary
    area_wise_text = f"Data Summary Statistics:\n\nTotal Crimes: {total_crimes}\nAverage Crime Rate per Day: {avg_crime_rate:.2f}\nMost Frequent Crime Type: {most_frequent_crime}"
    
    # Return the text summary
    return html.Pre(area_wise_text, style={'color': 'white', 'font-size': '15px', 'width': '100%'})
