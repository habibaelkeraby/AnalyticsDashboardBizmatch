# FUNCTIONS FILE

#####################
'''
Function to read relevant information of user
Output is list of relevant user data to be appended to dataframe
'''


def extract_user_data(data):

  # Relevant data

  # User details
  user_salutation = data['salutation']
  user_name = data['name']
  #user_level = data['level']['level']
  user_designation = data['designation']
  user_email = data['emailAddress']
  user_verified = data['emailVerified']

  # Geographical data
  if data['company']['country'] == None:
    country_name = None
    country_region = None
    country_subregion = None
  else:
    country_name = data['company']['country']['name']
    country_region = data['company']['country']['region']
    country_subregion = data['company']['country']['subregion']

  # Company details
  company_name = data['company']['name']
  company_industries = data['company']['category']
  company_industrylist = [industry['name'] for industry in company_industries]

  # Wanted deals & Interests
  user_wanteddeals = data['company']['wantedDeal']
  user_interests = data['interestedIndustry']
  user_interestlist = [industry['name'] for industry in user_interests]

  # Gather into list
  user_data = [user_salutation,
             user_name,
             #user_level,
             user_designation,
             user_email,
             user_verified,
             country_name,
             country_region,
             country_subregion,
             company_name,
             company_industrylist,
             user_wanteddeals,
             user_interestlist]

  return user_data
#####################
'''
Function to read relevant information regarding meetings/appointments
Output is list of relevant meeting data to be appended to dataframe
'''

def extract_meeting_data(data):
  
  # Relevant data
  
  # Meeting buyer
  meeting_buyer_company = data['buyer']['company']['name']
  meeting_buyer_country = data['buyer']['company']['country']['name']
  meeting_buyer_salutation = data['buyer']['salutation']
  meeting_buyer_designation = data['buyer']['designation']
  meeting_buyer_name = data['buyer']['name']
  meeting_buyer_email = data['buyer']['emailAddress']
  
  # Meeting seller
  meeting_seller_company = data['seller']['company']['name']
  try:
    meeting_seller_country = data['seller']['company']['country']['name']
  except:
    meeting_seller_country = 'Not Specified'
  meeting_seller_salutation = data['seller']['salutation']
  meeting_seller_designation = data['seller']['designation']
  meeting_seller_name = data['seller']['name']
  meeting_seller_email = data['seller']['emailAddress']
  
  # Metting info
  meeting_starttime = data['start']
  meeting_endtime = data['end']
  meeting_status = data['status']
  meeting_format = data['meetingFormat']
  
  
  # Gather into list
  meeting_data = [meeting_starttime,
                  meeting_endtime,
                  meeting_status,
                  meeting_format,
                  meeting_buyer_company,
                  meeting_buyer_country,
                  meeting_buyer_salutation,
                  meeting_buyer_designation,
                  meeting_buyer_name,
                  meeting_buyer_email,
                  meeting_seller_company,
                  meeting_seller_country,
                  meeting_seller_salutation,
                  meeting_seller_designation,
                  meeting_seller_name,
                  meeting_seller_email
                 ]
  
  return meeting_data
  
#####################
'''
Function to filter df by designation given as input (filter_item)
Output is list of top 5 interests related to the designation given
'''

def get_top_interests(filter_term, df):
  # Filter df by designation specified
  filtered_df = df[df["user_designation"]==filter_term]
  # Extract all interests selected
  interest_list = filtered_df["user_interestlist"].explode().unique() 
  # Remove nested lists
  interest_list = [str(item) for item in interest_list if not isinstance(item,list)]
  # Join all items as a single string then split 
  interest_list = ','.join(interest_list).split(",")
  # Count the instances of each unique item
  from collections import Counter
  mydict = Counter(interest_list)
  # Return top five results
  return sorted(mydict, key=mydict.get, reverse=True)[0:4]

#####################

'''
Function to filter df by designation given as input (filter_item)
Output is list of top 5 industries related to the designation given
'''

def get_top_industries(filter_term, df):
  # Filter df by designation specified
  filtered_df = df[df["user_designation"]==filter_term]
  # Extract all interests selected
  industry_list = filtered_df["company_industrylist"].explode().unique() 
  # Remove nested lists
  industry_list = [str(item) for item in industry_list if not isinstance(item,list)]
  # Join all items as a single string then split 
  industry_list = ','.join(industry_list).split(",")
  # Count the instances of each unique item
  from collections import Counter
  mydict = Counter(industry_list)
  # Return top five results
  return sorted(mydict, key=mydict.get, reverse=True)[0:4]

#####################