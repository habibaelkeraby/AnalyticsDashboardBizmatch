import requests
import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
import plost
from functions import *
import plotly.express as px

st.set_page_config(
    page_title="Post-Event Data Analysis Report",
    page_icon="📊",
    layout="wide",
    #initial_sidebar_state="expanded"
)

# Fetching data from API


@st.cache_data
def fetch_data():

    # USERS API CALL url/?eventId=69
    event_id = None

    try:
        event_id = st.query_params["eventId"]
    except:
        raise TypeError('Missing eventId')

    API_KEY = "W3kwgy2Tn40zr0rHwBFL18ov4Bb5FHA5eZw9CC38knZBb"
    #API_KEY2 = "eoZVbiqh7!&@8TZRP1d3rA0yqs0S4K@1BOKk*Dmiv7iAcZl&tiXeqGmFDwRPg5O"
    API_KEY2 = "r&KPHzfiLDOHIN!L@GzKO^MgRf6tIW2I*KDrsmYed$d$BgcspYq0Z6225xbhE%@fNXx&x1pfPBB#e"
    size = 37
    pageNumber = 0

    event_link = "https://newstage.biz-match.appsaya.com/"
    url = event_link + "api/users/search/findByEventIdAndGroupId?projection=withUserGroup&eventId=" + str(
        event_id) + "&groupId=2&size=" + str(size) + "&page=" + str(pageNumber)
    r = requests.get(url, headers={"X-BIZMATCH-API-KEY": API_KEY})

    # initialize list of lists
    all_users = []

    dataset_users = r.json()
    users = dataset_users['_embedded']['users']
    max_page = dataset_users['page']['totalPages']

    while pageNumber < max_page:
        for i in range(size):
            data = users[i]
            user_data = extract_user_data(data)
            all_users.append(user_data)
        pageNumber += 1
        r = requests.get(url, headers={"X-BIZMATCH-API-KEY": API_KEY})
        dataset_users = r.json()
        users = dataset_users['_embedded']['users']

    # MEETING API CALL
    # /?event_id=57
    #event_id = st.query_params["event_id"]
    event_id = 69
    size2 = 1
    pageNumber2 = 0
    r2 = requests.get(
        'https://bizmatch.appsaya.com/api/appointments/search/findByBuyerEventId?projection=withUsers&eventId='
        + str(event_id) + '&size=' + str(size2) + '&page=0',
        headers={'X-BIZMATCH-API-KEY': API_KEY2})

    # initialize list of lists
    all_meetings = []

    dataset_meetings = r2.json()
    meetings = dataset_meetings['_embedded']['appointments']
    size2 = dataset_meetings['page']['totalElements']
    # https://newstage.bizmatch.appsaya.com/
    r2 = requests.get(
        'https://bizmatch.appsaya.com/api/appointments/search/findByBuyerEventId?projection=withUsers&eventId='
        + str(event_id) + '&size=' + str(size2) + '&page=0',
        headers={'X-BIZMATCH-API-KEY': API_KEY2})
    dataset_meetings = r2.json()
    meetings = dataset_meetings['_embedded']['appointments']

    for j in range(size2):
        data = meetings[j]
        meeting_data = extract_meeting_data(data)
        all_meetings.append(meeting_data)

    return all_users, all_meetings


all_users, all_meetings = fetch_data()

# Create the pandas DataFrame for users
df_users = pd.DataFrame(
    all_users,
    columns=[
        'user_salutation',
        'user_name',
        #'user_level',
        'user_designation',
        'user_email',
        'user_verified',
        'country_name',
        'country_region',
        'country_subregion',
        'company_name',
        'company_industrylist',
        'user_wanteddeals',
        'user_interestlist'
    ])

df_users.fillna("Not Specified", inplace=True)
#st.write(df_users)

# Create the pandas DataFrame for meetings
df_meetings = pd.DataFrame(
    all_meetings,
    columns=[
        'meeting_starttime', 'meeting_endtime', 'meeting_status',
        'meeting_format', 'meeting_buyer_company', 'meeting_buyer_country',
        'meeting_buyer_salutation', 'meeting_buyer_designation',
        'meeting_buyer_name', 'meeting_buyer_email', 'meeting_seller_company',
        'meeting_seller_country', 'meeting_seller_salutation',
        'meeting_seller_designation', 'meeting_seller_name',
        'meeting_seller_email'
    ])

df_meetings.fillna("Not Specified", inplace=True)


####################
# DATA VISUALIZATION SECTION

# dashboard title
st.title("Post-Event Data Analysis Dashboard")

# REPORT SECTION 1
st.header("Attendee Demographics")
# insert horizontal divider
st.divider()

st.markdown("**An Overview in Numbers**")
# create 4 columns for number cards
card1, card2, card3, card4, card5 = st.columns(5)
# fill in those three columns with respective metrics or KPIs
card1.metric(label="Countries", value=len(df_users.country_name.unique()))
card2.metric(label="Participants", value=len(df_users.user_name.unique()))
card3.metric(label="Companies", value=len(df_users.company_name.unique()))
card4.metric(label="Job Titles/Designations",
             value=len(df_users.user_designation.unique()))
card5.metric(label="Meetings Booked", value=len(df_meetings.meeting_starttime))

# insert horizontal divider
st.divider()

col1, col2 = st.columns([0.3, 0.7], gap="large")


with col1:
    # Apply filter on the dataframe
    dynamic_filters = DynamicFilters(
        df_users, filters=['country_name', 'company_name', 'user_designation','user_salutation'])
    st.write("Apply filters in any order 👇")
    dynamic_filters.display_filters(location='columns', num_columns=1)
    #dynamic_filters.display_df()
    df_filtered = dynamic_filters.filter_df()


with col2:
    # Create a pie chart to show the participant gender distribution
    #plost.pie_chart(data=df_filtered.groupby(
        #['user_salutation']).user_name.count().reset_index(),
                    #theta='user_name',
                    #color='user_salutation',
                    #title="Participants per Salutation")

    fig = px.pie(df_filtered.groupby(['user_salutation'])['user_name'].count().reset_index(),
         values='user_name', names='user_salutation', title='Participant per Salutation')
    #fig.update_traces(textposition='inside')
    #fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, key="user_salutation", on_select="rerun")
    
    # Create a bar chart to show the number of users per country
    #plost.bar_chart(data=df_filtered.groupby(
        #'country_name').user_name.count().reset_index(),
                    #bar='country_name',
                    #value='user_name',
                    #direction='horizontal',
                    #title="Participants per Country")

    fig = px.bar(df_filtered.groupby('country_name')['user_name'].count().reset_index(),
                 y='user_name', x='country_name', text='user_name', title='Participants per Country')
    #fig.update_traces(texttemplate='%{text:s}', textposition='outside')
    #fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig, key="country_name", on_select="rerun")


    # Create a bar chart to show the number of users per region
    #plost.bar_chart(data=df_filtered.groupby(
        #['country_region']).user_name.count().reset_index(),
                    #bar='country_region',
                    #value='user_name',
                    #color='country_region',
                    #direction='horizontal',
                    #title="Participant Geographic Distribution")
    
    fig = px.bar(df_filtered.groupby('country_region')['user_name'].count().reset_index(),
         y='user_name', x='country_region', text='user_name', title='Participant Geographic Distribution')
    #fig.update_traces(texttemplate='%{text:s}', textposition='outside')
    #fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig, key="country_region", on_select="rerun")

    # Detailed view of geographical data
    with st.expander(
            "View details of participant distribution by geographical region:"
    ):
        st.write(
            df_filtered.groupby(['country_region', 'country_subregion'
                                 ]).user_name.count().reset_index())
    
    # Create a pie chart to show the number of users per designation
    #plost.pie_chart(data=df_filtered.groupby(
        #['user_designation']).user_name.count().reset_index(),
                    #theta='user_name',
                    #color='user_designation',
                    #title="Participant Designation Distribution")
    
    fig = px.pie(df_filtered.groupby(['user_designation'])['user_name'].count().reset_index(),
         values='user_name', names='user_designation', title='Participant Designation Distribution')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, key="user_designation", on_select="rerun",user_container_width=True)

####################

# REPORT SECTION 2
st.header("Engagement Analysis")
# insert horizontal divider
st.divider()

# Create a pie chart to show the participant gender distribution
#plost.pie_chart(data=df_users.groupby(['user_verified'
                                       #]).user_name.count().reset_index(),
                #theta='user_name',
                #color='user_verified',
                #title="Participant Account Verification Rate")

fig = px.pie(df_users.groupby(['user_verified'])['user_name'].count().reset_index(),
     values='user_name', names='user_verified', title='Participant Account Verification Rate')
#fig.update_traces(textposition='inside')
#fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, key="user_verified", on_select="rerun")

# Create a pie chart to show meeting status
#plost.pie_chart(data=df_meetings.groupby(
    #['meeting_status']).meeting_seller_company.count().reset_index(),
                #theta='meeting_seller_company',
                #color='meeting_status',
                #title="Meeting Status Distribution")

fig = px.pie(df_meetings.groupby(['meeting_status'])['meeting_seller_company'].count().reset_index(),
     values='meeting_seller_company', names='meeting_status', title='Meeting Status Distribution')
#fig.update_traces(textposition='inside')
#fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, key="meeting_status", on_select="rerun")

# Create a pie chart to show meeting format
#plost.pie_chart(data=df_meetings.groupby(
    #['meeting_format']).meeting_seller_company.count().reset_index(),
                #theta='meeting_seller_company',
                #color='meeting_format',
                #title="Meeting Format Distribution")

fig = px.pie(df_meetings.groupby(['meeting_format'])['meeting_seller_company'].count().reset_index(),
     values='meeting_seller_company', names='meeting_format', title='Meeting Format Distribution')
#fig.update_traces(textposition='inside')
#fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, key="meeting_format", on_select="rerun")

# Create a bar chart to show the number of meetings per starttime
#plost.bar_chart(data=df_meetings.groupby(
    #'meeting_starttime').meeting_seller_company.count().reset_index(),
                #bar='meeting_starttime',
                #value='meeting_seller_company',
                #direction='vertical',
                #title="Meetings per Time Slot")

fig = px.bar(df_meetings.groupby('meeting_starttime')['meeting_seller_company'].count().reset_index(),
     y='meeting_seller_company', x='meeting_starttime', text='meeting_seller_company', title='Meetings per Time Slot')
#fig.update_traces(texttemplate='%{text:s}', textposition='outside')
#fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig, key="meeting_starttime", on_select="rerun")
st.write('The times are in GMT. To reflect the actual times, take into account an offset of +3 hours (Timezone (GMT + 3)Asia/Riyadh).')

# Create a bar chart to show the number of meetings per company
#plost.bar_chart(data=df_meetings.groupby(
    #'meeting_seller_company').meeting_status.count().reset_index(),
                #bar='meeting_seller_company',
                #value='meeting_status',
                #direction='horizontal',
                #title="Meetings per Meeting Sender Company")

fig = px.bar(df_meetings.groupby('meeting_seller_company')['meeting_seller_name'].count().reset_index(),
     y='meeting_seller_name', x='meeting_seller_company', text='meeting_seller_name', title='Meetings per Meeting Sender Company')
#fig.update_traces(texttemplate='%{text:s}', textposition='outside')
#fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig, key="meeting_seller_name", on_select="rerun")

# Create a pie chart to show the number of meetings per company
#plost.pie_chart(data=df_meetings.groupby(
    #'meeting_seller_company').meeting_status.count().reset_index(),
                #color='meeting_seller_company',
                #theta='meeting_status',
                #title="Meetings per Meeting Sender Company")

# Create a bar chart to show the number of meetings per company
#plost.bar_chart(data=df_meetings.groupby(
    #'meeting_buyer_company').meeting_status.count().reset_index(),
                #bar='meeting_buyer_company',
                #value='meeting_status',
                #direction='horizontal',
                #title="Meetings per Meeting Receiver Company")

fig = px.bar(df_meetings.groupby('meeting_buyer_company')['meeting_buyer_name'].count().reset_index(),
     y='meeting_buyer_name', x='meeting_buyer_company', text='meeting_buyer_name', title='Meetings per Meeting Receiver Company')
#fig.update_traces(texttemplate='%{text:s}', textposition='outside')
#fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig, key="meeting_buyer_name", on_select="rerun")


# Create a pie chart to show the number of meetings per company
#plost.pie_chart(data=df_meetings.groupby(
    #'meeting_buyer_company').meeting_status.count().reset_index(),
                #color='meeting_buyer_company',
                #theta='meeting_status',
                #title="Meetings per Meeting Receiver Company")

# Create a pie chart to show the number of meetings per country
#plost.pie_chart(data=df_meetings.groupby(
    #'meeting_seller_country').meeting_status.count().reset_index(),
                #color='meeting_seller_country',
                #theta='meeting_status',
                #title="Meetings per Meeting Sender Country")

fig = px.pie(df_meetings.groupby(['meeting_seller_country'])['meeting_seller_name'].count().reset_index(),
     values='meeting_seller_name', names='meeting_seller_country', title='Meetings per Meeting Sender Country')
#fig.update_traces(textposition='inside')
#fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, key='meeting_seller_country', on_select="rerun")

#plost.pie_chart(data=df_meetings.groupby(
    #'meeting_buyer_country').meeting_status.count().reset_index(),
                #color='meeting_buyer_country',
                #theta='meeting_status',
                #title="Meetings per Meeting Receiver Country")

fig = px.pie(df_meetings.groupby(['meeting_buyer_country'])['meeting_buyer_name'].count().reset_index(),
     values='meeting_buyer_name', names='meeting_buyer_country', title='Meetings per Meeting Receiver Country')
#fig.update_traces(textposition='inside')
#fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig, key='meeting_buyer_country', on_select="rerun")

####################

# REPORT SECTION 3
st.header("Cross Preference Analysis")
# insert horizontal divider
st.divider()

c1, c2 = st.columns(2)

with c1:
    st.markdown("**Top Interests based on Participant Job Designation**")

    # Create a df to store top interests per designation
    interests_df = pd.DataFrame(columns=['user_designation', 'top_interests'])

    # Loop to find top interests for each unique designation
    for i in range(len(df_users.user_designation.unique())):
        # Append new row to df
        new_row = {
            "user_designation":
            df_users.user_designation.unique()[i],
            "top_interests":
            get_top_interests(df_users.user_designation.unique()[i], df_users)
        }
        interests_df = pd.concat(
            [interests_df, pd.DataFrame([new_row])], ignore_index=True)

    # Display df
    st.dataframe(interests_df)

with c2:
    st.markdown("**Top Industries based on Participant Job Designation**")

    # Create a df to store top interests per designation
    industries_df = pd.DataFrame(
        columns=['user_designation', 'top_industries'])

    # Loop to find top interests for each unique designation
    for i in range(len(df_users.user_designation.unique())):
        # Append new row to df
        new_row = {
            "user_designation":
            df_users.user_designation.unique()[i],
            "top_industries":
            get_top_industries(df_users.user_designation.unique()[i], df_users)
        }
        industries_df = pd.concat(
            [industries_df, pd.DataFrame([new_row])], ignore_index=True)

    # Display df
    st.dataframe(industries_df)

st.divider()

st.markdown("**All Meeting Data**")
st.write(df_meetings)