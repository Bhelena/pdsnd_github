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
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter a city name: Chicago, New York City or Washington: ') #allow user to introduce one or all cities
        if city.lower() in ['all','chicago', 'new york city', 'washington']:
            break
        else:
            print('No data for this city. Please enter a valid city: either Chicago, New York City or Washington')

    # get user input for month (all, january, february, ... , june) 
    while True:
         month = input('Enter a month (all, January, February, ..., June) Data available until June: ') #make sure user knows that data only goes until june         
         if month.lower() in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
         else:
            print('No data for this month. Please enter a month between January and June or enter all')
           
    # get user input for day of week (all, monday, tuesday, ... sunday)
    

    while True:
         day = input('Enter a day of the week (all, Monday, Tuesday, ..., Sunday): ')        
         if day.lower() in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
         else:
            print('Please make sure you introduced correctly the name of the day') #make sure user introduced day name correctly


    print('-'*40)
    return city.lower(), month.lower(), day.lower() # convert city into lowercase for robustness





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

    # load data file into a dataframe-- allow user also to select all cities
    
    if city.lower()== 'new york city':    
        df = pd.read_csv("new_york_city.csv")
    elif city.lower() =='all':
        df1= pd.read_csv("new_york_city.csv")
        df2= pd.read_csv("chicago.csv")
        df3= pd.read_csv("washington.csv")
        df= pd.concat([df1,df2,df3])
    else:
        df = pd.read_csv(f"{city.lower()}.csv")

    # convert the "Start Time" column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from "Start Time" to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month 
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['Start Time'].dt.month == month_index]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df





def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
     # get most common values: use mode() from pandas
    # display the most common month 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week 
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('\nCounts of User Types:\n', user_counts)

    # Display counts of gender (if the data is available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender:\n', gender_counts)
    else:
        print('\nGender data is not available for this city.')

    # Display earliest, most recent, and most common year of birth (if the data is available)
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nEarliest Birth Year:', earliest_birth_year)
        print('Most Recent Birth Year:', most_recent_birth_year)
        print('Most Common Birth Year:', most_common_birth_year)
    else:
        print('\nBirth Year data is not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most commonly used end station: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count').sort_values(by='count', ascending=False).iloc[0]
    print("Most frequent combination of start station and end station trip: Start Station = {}, End Station = {}, Count = {}".format(popular_trip['Start Station'], popular_trip['End Station'], popular_trip['count']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    start_loc = 0
    while True:
        # Ask the user if they want to see the next 5 rows of data
        show_data = input("Do you want to see the next 5 rows of data? (yes/no)").lower()
        if show_data == "yes":
            # Increment the start location by 5 to get the next 5 rows of data
            start_loc += 5
            print(df.iloc[start_loc:start_loc+5])
        else:
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break
    display_data(df)



if __name__ == "__main__":
	main()

