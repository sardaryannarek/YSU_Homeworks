import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
data = pd.read_csv('online_classroom_data.csv')


# Helper function to clean and split ratings
def clean_skill_data(column_name):
    # Split the entries, stack them, and convert to integer for numerical operations
    cleaned_data = data[column_name].str.split(',', expand=True).stack().reset_index(drop=True).astype(int)
    return cleaned_data


# Define visualization function for skills with a subtler color palette
def plot_skill_data(skill_data, title):
    fig, ax = plt.subplots()
    palette = sns.cubehelix_palette(start=.5, rot=-.75, as_cmap=False, reverse=True, dark=0.3, light=0.8,
                                    n_colors=len(skill_data.unique()))
    sns.countplot(x=skill_data, ax=ax, palette=palette)
    ax.set_title(title)
    ax.set_xlabel('Ratings')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to make room for rotated labels
    st.pyplot(fig)


# Define pages
def page_overview():
    st.title("Overview of Student Posts")
    st.markdown(
        "Explore the different types of posts by students in the classroom. Adjust the selection to see specific post types.")
    post_types = ['helpful_post', 'nice_code_post', 'collaborative_post', 'confused_post', 'creative_post', 'bad_post',
                  'amazing_post']
    selected_post = st.selectbox("Select Post Type", post_types)

    # Plotting
    fig, ax = plt.subplots()
    sns.histplot(data[selected_post], kde=True, ax=ax, color='slateblue')
    ax.set_title(f'Distribution of {selected_post}')
    st.pyplot(fig)


def page_time_approval():
    st.title("Time Online and Approval Rates")
    st.markdown(
        "Visualize how much time students are spending online and their approval rates. Use the slider to adjust the range of online time.")
    min_time, max_time = int(data['timeonline'].min()), int(data['timeonline'].max())
    time_filter = st.slider("Filter by Time Spent Online", min_time, max_time, (min_time, max_time))
    filtered_data = data[(data['timeonline'] >= time_filter[0]) & (data['timeonline'] <= time_filter[1])]
    time_fig, time_ax = plt.subplots()
    sns.histplot(filtered_data['timeonline'], kde=False, ax=time_ax, color='teal')
    time_ax.set_title('Time Spent Online')
    st.pyplot(time_fig)
    approved_fig, approved_ax = plt.subplots()
    sns.countplot(x='Approved', data=filtered_data, ax=approved_ax, palette='viridis')
    approved_ax.set_title('Approval Rates')
    st.pyplot(approved_fig)


def page_skills():
    st.title("Skill Assessments Overview")
    st.markdown(
        "Review the distribution of skill ratings across different classroom skills. Choose a skill to visualize.")
    skills = ['sk1_classroom', 'sk2_classroom', 'sk3_classroom', 'sk4_classroom']
    selected_skill = st.selectbox("Select Skill", skills)
    cleaned_data = clean_skill_data(selected_skill)
    plot_skill_data(cleaned_data, f'Distribution of Ratings in {selected_skill}')


def page_correlation():
    st.title("Correlation Analysis")
    st.markdown("Examine the correlation between numerical variables to identify any potential relationships.")
    corr_data = data.select_dtypes(include=[np.number])  # Select only numerical columns for correlation
    corr = corr_data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='viridis')
    st.pyplot(plt)


# Main app
def main():
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Select a page to view different data visualizations:")
    page = st.sidebar.radio("Choose a page", ["Overview", "Time and Approval", "Skills", "Correlation Analysis"])

    if page == "Overview":
        page_overview()
    elif page == "Time and Approval":
        page_time_approval()
    elif page == "Skills":
        page_skills()
    elif page == "Correlation Analysis":
        page_correlation()


if __name__ == "__main__":
    main()
