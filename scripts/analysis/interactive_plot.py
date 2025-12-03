"""
Interactive Visualization Script
Creates interactive bar plots for nutrient consumption by country and year
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Set up paths
PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def load_integrated_data():
    """Load integrated nutrition data"""
    integrated_path = PROCESSED_DATA_DIR / "integrated_nutrition_data.csv"
    
    if not integrated_path.exists():
        print(f"Error: Integrated dataset not found at {integrated_path}")
        print("Please run integrate_datasets.py first to create the integrated dataset.")
        return None
    
    try:
        df = pd.read_csv(integrated_path, low_memory=False)
        print(f"Loaded {len(df):,} rows from integrated dataset")
        return df
    except Exception as e:
        print(f"Error loading integrated dataset: {e}")
        return None


def create_interactive_plot(df, country=None, nutrient_type=None):
    """Create interactive bar plot for nutrient consumption"""
    
    if df is None:
        print("No data available for plotting")
        return None
    
    # Filter data
    filtered_df = df.copy()
    
    if country:
        filtered_df = filtered_df[filtered_df['Country'] == country]
    
    if nutrient_type:
        filtered_df = filtered_df[filtered_df['Nutrient_Type'] == nutrient_type]
    
    if len(filtered_df) == 0:
        print("No data available for the selected filters")
        return None
    
    # Group by year and calculate average consumption
    if 'Year' in filtered_df.columns and 'Consumption_Value' in filtered_df.columns:
        plot_df = filtered_df.groupby(['Year', 'Nutrient_Type', 'Country']).agg({
            'Consumption_Value': 'mean'
        }).reset_index()
        
        # Create interactive bar plot
        fig = px.bar(
            plot_df,
            x='Year',
            y='Consumption_Value',
            color='Nutrient_Type',
            facet_col='Country' if country is None else None,
            title=f'Nutrient Consumption Over Time{" - " + country if country else ""}',
            labels={
                'Consumption_Value': 'Consumption Value',
                'Year': 'Year',
                'Nutrient_Type': 'Nutrient Type'
            },
            hover_data=['Country', 'Nutrient_Type', 'Year', 'Consumption_Value']
        )
        
        fig.update_layout(
            height=600,
            showlegend=True,
            xaxis_title="Year",
            yaxis_title="Consumption Value"
        )
        
        return fig
    else:
        print("Required columns (Year, Consumption_Value) not found in dataset")
        return None


def create_simple_plot(df):
    """Create a simple interactive plot with sample data"""
    
    if df is None:
        print("No data available for plotting")
        return None
    
    # Get available countries and nutrients
    if 'Country' in df.columns:
        countries = sorted(df['Country'].unique())[:10]  # First 10 countries
    else:
        countries = []
    
    if 'Nutrient_Type' in df.columns:
        nutrients = df['Nutrient_Type'].unique()
    else:
        nutrients = []
    
    if len(countries) == 0 or len(nutrients) == 0:
        print("Insufficient data for plotting")
        return None
    
    # Filter for first country and first nutrient
    sample_country = countries[0]
    sample_nutrient = nutrients[0] if len(nutrients) > 0 else None
    
    filtered_df = df[df['Country'] == sample_country].copy()
    if sample_nutrient:
        filtered_df = filtered_df[filtered_df['Nutrient_Type'] == sample_nutrient]
    
    if 'Year' in filtered_df.columns and 'Consumption_Value' in filtered_df.columns:
        # Group by year
        plot_df = filtered_df.groupby('Year')['Consumption_Value'].mean().reset_index()
        
        # Create interactive bar plot
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=plot_df['Year'],
            y=plot_df['Consumption_Value'],
            name=sample_nutrient if sample_nutrient else 'Consumption',
            marker_color='steelblue',
            hovertemplate='<b>Year:</b> %{x}<br>' +
                         '<b>Consumption:</b> %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Nutrient Consumption Over Time - {sample_country}',
            xaxis_title='Year',
            yaxis_title='Consumption Value',
            height=500,
            showlegend=True
        )
        
        return fig
    else:
        print("Required columns not found")
        return None


def save_plot(fig, output_path):
    """Save plot to HTML file"""
    if fig is None:
        print("No figure to save")
        return
    
    try:
        fig.write_html(str(output_path))
        print(f"Plot saved to {output_path}")
    except Exception as e:
        print(f"Error saving plot: {e}")


def main():
    """Main function for interactive visualization"""
    print("=" * 60)
    print("Interactive Visualization")
    print("=" * 60)
    
    # Load data
    df = load_integrated_data()
    
    if df is None:
        print("\nCannot create visualization without data.")
        print("Please run integrate_datasets.py first.")
        return
    
    # Display available options
    print("\nAvailable options:")
    if 'Country' in df.columns:
        countries = sorted(df['Country'].unique())
        print(f"  Countries: {len(countries)} available")
        print(f"  Sample: {', '.join(countries[:5])}...")
    
    if 'Nutrient_Type' in df.columns:
        nutrients = df['Nutrient_Type'].unique()
        print(f"  Nutrient types: {len(nutrients)} available")
        print(f"  Types: {', '.join(nutrients)}")
    
    # Create sample plot
    print("\nCreating sample interactive plot...")
    fig = create_simple_plot(df)
    
    if fig is not None:
        # Save plot
        output_dir = PROJECT_ROOT / "reports" / "figures"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "interactive_nutrition_plot.html"
        save_plot(fig, output_path)
        
        # Show plot (if running in interactive environment)
        try:
            fig.show()
        except Exception:
            print("\nNote: To view the plot interactively, open the HTML file in a web browser.")
            print(f"File location: {output_path}")
    
    print("\n" + "=" * 60)
    print("Visualization Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

