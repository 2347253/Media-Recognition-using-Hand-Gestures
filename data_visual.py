import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    # Fill missing values in 'mpaa_rating' column with 'Not Rated'
    df['mpaa_rating'].fillna('Not Rated', inplace=True)
    
    # Remove records with missing values
    df_cleaned = df.dropna()
    return df_cleaned

def movie_comparison_chart(df, movie_title):
    # Filter data for the selected movie
    movie_data = df[df['movie_title'] == movie_title]

    # Create a DataFrame for the selected movie containing initial gross and inflated gross
    data = {'Gross Type': ['Initial Gross', 'Inflated Gross'],
            'Gross Value': [movie_data['total_gross'].values[0], movie_data['inflation_adjusted_gross'].values[0]]}
    df_movie = pd.DataFrame(data)

    # Create bar chart
    fig = px.bar(df_movie, x='Gross Type', y='Gross Value', text='Gross Value', 
                color='Gross Type',  # Color by 'Gross Type' column
                color_discrete_map={'Initial Gross': 'blue', 'Inflated Gross': 'orange'},  # Specify colors
                labels={'Gross Type': 'Gross Type', 'Gross Value': 'Gross Value ($)'},
                title=f'Comparison of Initial Gross and Inflated Gross for {movie_title}')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    st.plotly_chart(fig)

def total_gross_over_years_plot(df):
    # Ensure 'release_date' column is in datetime format
    df['release_date'] = pd.to_datetime(df['release_date'])

    # Group data by release year and calculate total gross for each year
    total_gross_by_year = df.groupby(df['release_date'].dt.year)['total_gross'].sum().reset_index()

    # Create line plot
    fig = px.line(total_gross_by_year, x='release_date', y='total_gross', title='Total Gross Over Release Years',
                  labels={'release_date': 'Release Year', 'total_gross': 'Total Gross ($)'})
    st.plotly_chart(fig)

def genre_pie_chart(df):
    # Group data by genre and calculate total gross for each genre
    genre_totals = df.groupby('genre')['total_gross'].sum().reset_index()

    # Create 3D pie chart
    fig = px.pie(genre_totals, values='total_gross', names='genre', 
                 title='Total Gross by Genre (3D Pie Chart)', 
                 hover_name='genre', 
                 hover_data={'total_gross': ':$.2f'},  
                 labels={'total_gross': 'Total Gross ($)'}, 
                 hole=0.3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)    

def main():
    st.markdown("<h3>Total Gross Values on Disney Movies (1937 - 2016) 🏰🌠</h3>", unsafe_allow_html=True)

    file_path = 'disney_movies_total_gross.csv'  
    df = load_data(file_path)

    # Preprocess data
    df_processed = preprocess_data(df)
    st.markdown("---")

    # Display preprocessed dataset
    st.write("Preprocessed Dataset")
    st.write(df_processed)

    # Display line plot of total gross over release years
    st.markdown("<h4>Line Plot of Total Gross Over Release Years</h4>", unsafe_allow_html=True)
    total_gross_over_years_plot(df_processed)

    # Select movie for comparison
    st.markdown("---")
    st.markdown("<h4>Select a Movie for Comparison</h4>", unsafe_allow_html=True)
    selected_movie = st.selectbox("Select Movie:", df_processed['movie_title'].unique())

    # Display bar chart for selected movie comparison
    st.markdown(f"<h4>Comparison of Initial Gross and Inflated Gross for {selected_movie}</h4>", unsafe_allow_html=True)
    movie_comparison_chart(df_processed, selected_movie)

    # Display 3D pie chart for total gross by genre
    st.markdown("---")
    st.markdown("<h4>3D Pie Chart of Total Gross by Genre</h4>", unsafe_allow_html=True)
    genre_pie_chart(df_processed)

if __name__ == "__main__":
    main()
