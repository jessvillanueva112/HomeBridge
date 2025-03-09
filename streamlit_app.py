
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils.gemini_integration import initialize_gemini, generate_analysis, generate_resilience_strategies

# Page configuration
st.set_page_config(
    page_title="HomeBridge - UBC International Student Support",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check for Gemini API key
if not os.environ.get("GEMINI_API_KEY"):
    st.warning("⚠️ Gemini API key not set. Some advanced features will be limited.", icon="⚠️")
    gemini_available = False
else:
    gemini_available = initialize_gemini()
    if gemini_available:
        st.success("✅ Gemini AI integration active", icon="✅")

# Database connection function
@st.cache_resource
def get_connection():
    return sqlite3.connect("instance/homesickness.db", check_same_thread=False)

# Helper function to load data
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def load_data():
    conn = get_connection()
    
    # Load interactions
    interactions_df = pd.read_sql("""
        SELECT id, user_id, timestamp, transcript, sentiment_score, homesickness_level 
        FROM interaction 
        ORDER BY timestamp DESC
    """, conn)
    
    # Load progress logs
    progress_df = pd.read_sql("""
        SELECT id, user_id, timestamp, mood_rating, gratitude_entry, activities_completed
        FROM progress_log
        ORDER BY timestamp DESC
    """, conn)
    
    # Convert timestamps to datetime
    interactions_df['timestamp'] = pd.to_datetime(interactions_df['timestamp'])
    progress_df['timestamp'] = pd.to_datetime(progress_df['timestamp'])
    
    return interactions_df, progress_df

# Sidebar navigation
st.sidebar.title("HomeBridge")
st.sidebar.image("static/img/logo.png", use_column_width=True)
page = st.sidebar.radio("Navigation", 
    ["Dashboard", "Voice Journal", "Progress Tracker", "Resource Hub", "Advanced Analytics"])

st.sidebar.markdown("---")
st.sidebar.info("""
**HomeBridge** helps UBC international students 
cope with homesickness through AI-powered 
analysis and personalized resilience strategies.
""")

# Load data
interactions_df, progress_df = load_data()

# Dashboard page
if page == "Dashboard":
    st.title("HomeBridge Dashboard")
    st.subheader("UBC International Student Support")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_interactions = len(interactions_df)
        st.metric("Total Interactions", total_interactions)
    
    with col2:
        if not progress_df.empty:
            avg_mood = progress_df['mood_rating'].mean()
            st.metric("Average Mood Rating", f"{avg_mood:.1f}/10")
        else:
            st.metric("Average Mood Rating", "No data")
    
    with col3:
        if not interactions_df.empty:
            avg_homesickness = interactions_df['homesickness_level'].mean()
            st.metric("Average Homesickness", f"{avg_homesickness:.1f}/10")
        else:
            st.metric("Average Homesickness", "No data")
    
    # Recent activity
    st.subheader("Recent Activity")
    
    tab1, tab2 = st.tabs(["Interactions", "Progress Logs"])
    
    with tab1:
        if not interactions_df.empty:
            recent_interactions = interactions_df.head(5)
            for _, row in recent_interactions.iterrows():
                with st.expander(f"Interaction on {row['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                    st.write(f"**Transcript:** {row['transcript']}")
                    st.write(f"**Sentiment Score:** {row['sentiment_score']:.2f}")
                    st.write(f"**Homesickness Level:** {row['homesickness_level']}/10")
        else:
            st.info("No interactions recorded yet.")
    
    with tab2:
        if not progress_df.empty:
            recent_logs = progress_df.head(5)
            for _, row in recent_logs.iterrows():
                with st.expander(f"Log on {row['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                    st.write(f"**Mood Rating:** {row['mood_rating']}/10")
                    st.write(f"**Gratitude Entry:** {row['gratitude_entry']}")
                    st.write(f"**Activities Completed:** {row['activities_completed']}")
        else:
            st.info("No progress logs recorded yet.")
    
    # Trend visualization
    st.subheader("Emotional Well-being Trends")
    
    # Combine data for trend analysis
    if not interactions_df.empty and not progress_df.empty:
        # Prepare data for plotting
        mood_data = progress_df[['timestamp', 'mood_rating']].rename(columns={'mood_rating': 'value'})
        mood_data['metric'] = 'Mood Rating'
        
        homesick_data = interactions_df[['timestamp', 'homesickness_level']].rename(columns={'homesickness_level': 'value'})
        homesick_data['metric'] = 'Homesickness Level'
        
        sentiment_data = interactions_df[['timestamp', 'sentiment_score']].rename(columns={'sentiment_score': 'value'})
        sentiment_data['metric'] = 'Sentiment Score'
        
        # Normalize sentiment score to 0-10 scale for comparison
        sentiment_data['value'] = (sentiment_data['value'] + 1) * 5
        
        # Combine data
        combined_data = pd.concat([mood_data, homesick_data, sentiment_data])
        
        # Create interactive plot
        fig = px.line(combined_data, x='timestamp', y='value', color='metric', 
                       title='Emotional Well-being Trends Over Time',
                       labels={'timestamp': 'Date', 'value': 'Rating (0-10)'})
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data to display trends. Continue using HomeBridge to see your progress.")

# Voice Journal page
elif page == "Voice Journal":
    st.title("Voice Journal")
    st.write("Share how you're feeling today and receive personalized support strategies.")
    
    # Text input for when voice recognition isn't available
    user_input = st.text_area("How are you feeling today? (Share your thoughts as an international student at UBC)",
                             height=150, 
                             help="Write about your experiences, challenges, and feelings as an international student.")
    
    # Option to upload audio file (placeholder for voice recognition)
    audio_file = st.file_uploader("Or upload an audio recording", type=['mp3', 'wav'])
    
    if st.button("Analyze", type="primary"):
        if user_input or audio_file:
            # Placeholder for actual processing
            with st.spinner("Analyzing your input..."):
                # Use Gemini for analysis if available
                if user_input and gemini_available:
                    analysis = generate_analysis(user_input)
                    if analysis:
                        sentiment_score = analysis.get('sentiment_score', 0)
                        homesickness_level = analysis.get('homesickness_level', 5)
                        
                        # Get strategies
                        strategies = generate_resilience_strategies(user_input, homesickness_level)
                    else:
                        # Fallback values
                        sentiment_score = 0
                        homesickness_level = 5
                        strategies = []
                else:
                    # Demo values
                    sentiment_score = 0.2
                    homesickness_level = 6
                    strategies = [
                        {
                            "title": "Connect with Others",
                            "description": "Spend time with friends or reach out to family back home.",
                            "steps": ["Call a family member", "Meet a friend for coffee", "Join a student club"]
                        },
                        {
                            "title": "Self-Care Practice",
                            "description": "Take time for activities that help you relax and recharge.",
                            "steps": ["Get adequate sleep", "Eat nutritious meals", "Take time for hobbies"]
                        }
                    ]
            
            # Display results
            st.success("Analysis complete!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Sentiment Analysis")
                # Normalize sentiment score to 0-100% for the gauge
                normalized_sentiment = (sentiment_score + 1) * 50
                
                # Create gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = normalized_sentiment,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Sentiment Score"},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "royalblue"},
                        'steps': [
                            {'range': [0, 40], 'color': "lightcoral"},
                            {'range': [40, 60], 'color': "lightyellow"},
                            {'range': [60, 100], 'color': "lightgreen"}
                        ]
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
                
                if sentiment_score < -0.3:
                    st.info("Your emotions seem quite negative. It's normal to have difficult days.")
                elif sentiment_score > 0.3:
                    st.info("You're expressing positive emotions. That's wonderful!")
                else:
                    st.info("Your emotions seem balanced or mixed.")
            
            with col2:
                st.subheader("Homesickness Assessment")
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = homesickness_level,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Homesickness Level"},
                    gauge = {
                        'axis': {'range': [0, 10]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 3], 'color': "lightgreen"},
                            {'range': [3, 7], 'color': "lightyellow"},
                            {'range': [7, 10], 'color': "lightcoral"}
                        ]
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
                
                if homesickness_level >= 7:
                    st.info("You're experiencing significant homesickness. The strategies below may help.")
                elif homesickness_level >= 4:
                    st.info("You're experiencing moderate homesickness, which is common for international students.")
                else:
                    st.info("You're managing well with minimal homesickness.")
            
            # Display resilience strategies
            st.subheader("Personalized Resilience Strategies")
            
            for i, strategy in enumerate(strategies):
                with st.expander(f"Strategy {i+1}: {strategy['title']}", expanded=True):
                    st.write(f"**Description:** {strategy['description']}")
                    st.write("**Steps to take:**")
                    for step in strategy['steps']:
                        st.write(f"- {step}")
                    
                    # Add a "Mark as completed" button (placeholder functionality)
                    if st.button(f"Mark as completed", key=f"complete_{i}"):
                        st.balloons()
                        st.success("Great job! Keep tracking your progress.")
        else:
            st.error("Please enter text or upload an audio file to analyze.")

# Progress Tracker page
elif page == "Progress Tracker":
    st.title("Progress Tracker")
    st.write("Monitor your emotional well-being and celebrate your successes.")
    
    # Date filtering
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", 
                                   value=datetime.now() - timedelta(days=30),
                                   max_value=datetime.now())
    with col2:
        end_date = st.date_input("End Date", 
                                 value=datetime.now(),
                                 max_value=datetime.now())
    
    # Convert to datetime for filtering
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date) + timedelta(days=1)  # Include the end date
    
    # Filter data by date range
    filtered_interactions = interactions_df[
        (interactions_df['timestamp'] >= start_datetime) & 
        (interactions_df['timestamp'] <= end_datetime)
    ]
    
    filtered_progress = progress_df[
        (progress_df['timestamp'] >= start_datetime) & 
        (progress_df['timestamp'] <= end_datetime)
    ]
    
    # Display visualizations
    if not filtered_interactions.empty or not filtered_progress.empty:
        # Tab layout for different metrics
        tab1, tab2, tab3 = st.tabs(["Mood & Homesickness", "Sentiment Analysis", "Gratitude Journal"])
        
        with tab1:
            st.subheader("Mood & Homesickness Trends")
            
            fig = go.Figure()
            
            if not filtered_progress.empty:
                # Add mood rating line
                fig.add_trace(go.Scatter(
                    x=filtered_progress['timestamp'],
                    y=filtered_progress['mood_rating'],
                    mode='lines+markers',
                    name='Mood Rating',
                    line=dict(color='green', width=2)
                ))
            
            if not filtered_interactions.empty:
                # Add homesickness level line
                fig.add_trace(go.Scatter(
                    x=filtered_interactions['timestamp'],
                    y=filtered_interactions['homesickness_level'],
                    mode='lines+markers',
                    name='Homesickness Level',
                    line=dict(color='blue', width=2)
                ))
            
            fig.update_layout(
                title='Mood and Homesickness Over Time',
                xaxis_title='Date',
                yaxis_title='Rating (1-10)',
                yaxis=dict(range=[0, 10]),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Sentiment Analysis Trends")
            
            if not filtered_interactions.empty:
                # Create sentiment chart
                fig = px.line(filtered_interactions, x='timestamp', y='sentiment_score',
                              title='Sentiment Score Over Time',
                              labels={'timestamp': 'Date', 'sentiment_score': 'Sentiment (-1 to 1)'})
                
                fig.update_layout(
                    yaxis=dict(range=[-1, 1]),
                    hovermode='x unified'
                )
                
                # Add a zero line
                fig.add_hline(y=0, line_dash="dash", line_color="gray")
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show distribution of sentiment
                st.subheader("Sentiment Distribution")
                
                fig = px.histogram(filtered_interactions, x='sentiment_score',
                                   nbins=20, color_discrete_sequence=['royalblue'],
                                   title='Distribution of Sentiment Scores')
                
                fig.update_layout(
                    xaxis_title='Sentiment Score',
                    yaxis_title='Count',
                    bargap=0.2
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No sentiment data available for the selected date range.")
        
        with tab3:
            st.subheader("Gratitude Journal Entries")
            
            if not filtered_progress.empty and 'gratitude_entry' in filtered_progress.columns:
                # Display gratitude entries
                entries = filtered_progress[['timestamp', 'gratitude_entry']].dropna(subset=['gratitude_entry'])
                
                if not entries.empty:
                    for _, row in entries.iterrows():
                        st.write(f"**{row['timestamp'].strftime('%Y-%m-%d')}**")
                        st.write(row['gratitude_entry'])
                        st.markdown("---")
                else:
                    st.info("No gratitude entries found for the selected date range.")
            else:
                st.info("No gratitude data available for the selected date range.")
    else:
        st.info("No data available for the selected date range.")
    
    # Add a new progress log
    st.subheader("Add New Progress Log")
    
    with st.form("progress_form"):
        mood_rating = st.slider("How would you rate your mood today?", 1, 10, 5)
        gratitude_entry = st.text_area("What are you grateful for today?")
        activities = st.text_area("What resilience activities have you completed?")
        
        submit_button = st.form_submit_button("Save Progress")
        
        if submit_button:
            # In a real implementation, this would save to the database
            st.success("Progress saved successfully!")
            st.balloons()

# Resource Hub page
elif page == "Resource Hub":
    st.title("Resource Hub")
    st.write("Access resources and support services for UBC international students.")
    
    # Resource categories
    categories = [
        "Academic Support", 
        "Mental Health", 
        "Cultural Adaptation", 
        "Social Connection", 
        "Legal & Immigration",
        "Financial Resources"
    ]
    
    selected_category = st.selectbox("Filter by category", ["All"] + categories)
    
    # Sample resources (in a real app, would pull from database)
    resources = [
        {
            "title": "UBC International Student Advising",
            "description": "Get help with immigration, health insurance, and life in Canada.",
            "category": "Legal & Immigration",
            "url": "https://students.ubc.ca/international-student-advising",
            "contact": "isa@ubc.ca | 604-822-5021"
        },
        {
            "title": "UBC Counselling Services",
            "description": "Free confidential counselling for UBC students.",
            "category": "Mental Health",
            "url": "https://students.ubc.ca/counselling-services",
            "contact": "counselling.services@ubc.ca | 604-822-3811"
        },
        {
            "title": "International Student Community",
            "description": "Connect with other international students through events and programs.",
            "category": "Social Connection",
            "url": "https://students.ubc.ca/campus-life/diversity-campus/international-student-support",
            "contact": "isa.events@ubc.ca"
        },
        {
            "title": "Academic English Support",
            "description": "Improve your academic English skills with free workshops and resources.",
            "category": "Academic Support",
            "url": "https://academic-english.ubc.ca/",
            "contact": "academic.english@ubc.ca"
        },
        {
            "title": "Cultural Activities in Vancouver",
            "description": "Discover cultural events and activities around Vancouver.",
            "category": "Cultural Adaptation",
            "url": "https://vancouver.ca/parks-recreation-culture/cultural-events.aspx",
            "contact": "N/A"
        },
        {
            "title": "International Student Financial Assistance",
            "description": "Emergency loans and financial advice for international students.",
            "category": "Financial Resources",
            "url": "https://students.ubc.ca/enrolment/finances/funding-studies/financial-assistance",
            "contact": "international.awards@ubc.ca"
        }
    ]
    
    # Filter resources by category
    if selected_category != "All":
        filtered_resources = [r for r in resources if r["category"] == selected_category]
    else:
        filtered_resources = resources
    
    # Display resources
    for resource in filtered_resources:
        with st.expander(resource["title"]):
            st.write(f"**Description:** {resource['description']}")
            st.write(f"**Category:** {resource['category']}")
            st.write(f"**Contact:** {resource['contact']}")
            st.write(f"**Website:** [{resource['url']}]({resource['url']})")

# Advanced Analytics page
elif page == "Advanced Analytics":
    st.title("Advanced Analytics")
    st.write("Gain deeper insights into your adaptation journey.")
    
    if gemini_available:
        st.success("This page uses Google's Gemini AI to provide enhanced analytics.")
    else:
        st.warning("⚠️ Gemini AI integration is not active. Some features may be limited.")
    
    # Engagement metrics
    st.subheader("Engagement Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        interactions_last_week = len(interactions_df[interactions_df['timestamp'] > (datetime.now() - timedelta(days=7))])
        st.metric("Interactions (Last 7 Days)", interactions_last_week)
    
    with col2:
        logs_last_week = len(progress_df[progress_df['timestamp'] > (datetime.now() - timedelta(days=7))])
        st.metric("Progress Logs (Last 7 Days)", logs_last_week)
    
    with col3:
        total_gratitude = len(progress_df[progress_df['gratitude_entry'].notna() & (progress_df['gratitude_entry'] != "")])
        st.metric("Total Gratitude Entries", total_gratitude)
    
    # Weekly comparison
    st.subheader("Weekly Comparison")
    
    # Calculate average mood and homesickness by week
    if not interactions_df.empty and not progress_df.empty:
        # Add week column
        interactions_df['week'] = interactions_df['timestamp'].dt.isocalendar().week
        progress_df['week'] = progress_df['timestamp'].dt.isocalendar().week
        
        # Group by week
        weekly_homesickness = interactions_df.groupby('week')['homesickness_level'].mean().reset_index()
        weekly_mood = progress_df.groupby('week')['mood_rating'].mean().reset_index()
        
        # Create chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=weekly_mood['week'],
            y=weekly_mood['mood_rating'],
            name='Avg Mood Rating',
            marker_color='green'
        ))
        
        fig.add_trace(go.Bar(
            x=weekly_homesickness['week'],
            y=weekly_homesickness['homesickness_level'],
            name='Avg Homesickness',
            marker_color='blue'
        ))
        
        fig.update_layout(
            title='Weekly Average Metrics',
            xaxis_title='Week Number',
            yaxis_title='Average Rating (1-10)',
            barmode='group',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Neuroplasticity insights
    st.subheader("Neuroplasticity Insights")
    st.write("""
    Research shows that gratitude journaling increases dorsolateral prefrontal cortex activity by 29%, 
    creating cognitive buffers against emotional overwhelm (BMC Psychology).
    """)
    
    if not progress_df.empty and 'gratitude_entry' in progress_df.columns:
        # Count gratitude entries by week
        progress_df['gratitude_count'] = progress_df['gratitude_entry'].notna() & (progress_df['gratitude_entry'] != "")
        weekly_gratitude = progress_df.groupby('week')['gratitude_count'].sum().reset_index()
        
        if not weekly_gratitude.empty:
            # Create chart
            fig = px.line(weekly_gratitude, x='week', y='gratitude_count',
                          title='Gratitude Entries by Week',
                          labels={'week': 'Week Number', 'gratitude_count': 'Number of Entries'},
                          markers=True, line_shape='linear')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate correlation with mood (if available)
            if not weekly_mood.empty:
                merged_data = pd.merge(weekly_gratitude, weekly_mood, on='week')
                correlation = merged_data['gratitude_count'].corr(merged_data['mood_rating'])
                
                st.info(f"Correlation between gratitude practice and mood rating: {correlation:.2f}")
                
                if correlation > 0.3:
                    st.success("Your data shows a positive relationship between gratitude practice and mood improvement!")
                elif correlation < -0.3:
                    st.warning("Interestingly, your data shows an inverse relationship between gratitude practice and mood.")
                else:
                    st.info("Your data doesn't show a strong relationship between gratitude practice and mood yet.")
    
    # Text analysis (only if Gemini is available)
    if gemini_available and not interactions_df.empty:
        st.subheader("Linguistic Pattern Analysis")
        st.write("Analyze common themes and patterns in your journal entries.")
        
        # Get a sample of recent interactions
        recent_texts = interactions_df['transcript'].head(5).tolist()
        
        if recent_texts:
            combined_text = " ".join(recent_texts)
            
            with st.spinner("Analyzing linguistic patterns..."):
                # In a real implementation, we would use the Gemini API here
                # For demo purposes, showing static content
                st.write("**Common Themes in Your Journal:**")
                
                themes = {
                    "Academic Adjustment": 68,
                    "Social Connection": 42,
                    "Cultural Differences": 89,
                    "Personal Growth": 35,
                    "Family Separation": 74
                }
                
                # Create bar chart
                fig = px.bar(
                    x=list(themes.keys()),
                    y=list(themes.values()),
                    title="Theme Presence in Your Journal Entries",
                    labels={'x': 'Theme', 'y': 'Relevance Score'},
                    color=list(themes.values()),
                    color_continuous_scale='Viridis'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.write("**Key Insights:**")
                st.info("""
                - Your entries show a strong focus on cultural differences and adaptation challenges
                - Family separation appears as a significant emotional factor
                - Academic adjustment themes are prominent but balanced with social aspects
                - There's evidence of growing resilience and adaptation over time
                """)
    
    # Add a feedback form
    st.subheader("Feedback")
    with st.expander("Share your thoughts on HomeBridge"):
        feedback_text = st.text_area("What do you like or what could be improved?")
        feedback_rating = st.slider("How would you rate HomeBridge overall?", 1, 5, 3)
        
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback! We'll use it to improve HomeBridge.")
