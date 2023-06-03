import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print ('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    global city
    city = input ('Please enter the city you\'re interested in: ')
    while city not in ['chicago', 'new york city', 'washington']:
        city = input ("Please choose between Chicago, New York City or Washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input ('Please enter month you\'re interested in: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input ('Please enter "all" to get data without month filter or write specific month (January, February, March, April, May or June): ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input ('Please enter day you\'re interested in : ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input ('Please enter "all" to get data without day filter or write specific day of week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday: ').lower()
        
    print ('-'*69)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load chosen file into df
    df = pd.read_csv('{}.csv'.format(city))
    
    #converting columns od Start Time and End Time into format yyyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    #extracting month from Start Time into column called month
    df['month'] = df['Start Time'].dt.month
    
    #filter by month
    if month != 'all':
        # use the index of the months list to get correct int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month to create new dataframe
        df = df[df['month'] == month]
        
    # extract day from Start Time into new column called weekday_name
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by day of week if possible
    if day != 'all':
        
        # filter by day of week to create new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print ('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print ("The most common month is: ", df['month'].value_counts().idxmax())

    # display the most common day of week
    print ("The most common day is: ", df['day_of_week'].value_counts().idxmax())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print ("The most common hour is: ", df['hour'].value_counts().idxmax())
    
    print ("\nThis took %s seconds." % (time.time() - start_time))
    print ('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print ('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print ("The most common start station is: ", df ['Start Station'].value_counts().idxmax())
    
    # display most commonly used end station
    print ("The most common end station is: ", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    print ("The most frequent combination of start station and end station trip")
    most_common_start_and_end_stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print (most_common_start_and_end_stations)
    
    print ("\nThis took %s seconds." % (time.time() - start_time))
    print ('-'*69)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print ('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_dur = df['Trip Duration'].sum() / 3600.0
    print ("total travel time in hours is: ", total_dur)

    # display mean travel time
    mean_dur = df['Trip Duration'].mean() / 3600.0
    print ("mean travel time in hours is: ", mean_dur)
    
    print ("\nThis took %s seconds." % (time.time() - start_time))
    print ('-'*69)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print ('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print (user_types.to_string(name=True,dtype=False))

    # Display counts of gender also includes check for Washington case 
    if city !='washington':
        user_gender = df['Gender'].value_counts()
        print (user_gender.to_string(name=True,dtype=False))

    # Display earliest, most recent, and most common year of birth also includes check for Washington case 
    if city !='washington':
        earliest_year_of_birth = int(df['Birth Year'].min())
        most_recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].value_counts().idxmax())
        print ("The earliest year of birth is:",earliest_year_of_birth,
               ", most recent one is:",most_recent_year_of_birth,
               "and the most common one is: ",most_common_year_of_birth,)

    print ("\nThis took %s seconds." % (time.time() - start_time))
    print ('-'*69)
    
def data_raw (df):
    """Displays the data due filteration.
    5 rows of data will be added after each press"""
    raw_input = input ('Press Enter to see raw data. Write "no" to skip.\n')
    x = 0
    while raw_input.lower() != 'no':
        x = x+5
        print(df.head(x))
        input()
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_raw(df)

        restart = input ('\nWould you like to restart? Write yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()