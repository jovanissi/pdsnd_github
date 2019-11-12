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
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City, or Washington?\n')
    city = city.lower()
    while city != 'chicago' and city != 'washington' and city != 'new york city':
        city = input('Entered city is unknown, please try again\n')
        
    month = 'all'
    day = 'all'
    
    filter_by = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter\n')
    filter_by = filter_by.lower()
    
    if filter_by == 'month':
        # Get user input for month (all, january, february, ... , june)
        month = get_month()
    elif filter_by == 'day':
        # Get user input for day of week (all, monday, tuesday, ... sunday)
        day = get_day()
    elif filter_by == 'both':
        month = get_month()
        day = get_day()


    print('-'*40)
    return city, month, day
                      
                      
def get_month():
    month = input('Which month? January, February, March, April, May, or June?\n')
    
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    not_right_month = True
    
    while not_right_month:
        month = month.lower()
        if month in months:
            not_right_month = False
        else:
            month = input('Please choose the right month among January, February, March, April, May, or June\n')
            continue
        
    return month


def get_day():
    day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n')
    
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    not_right_day = True
    
    while not_right_day:
        day = day.lower()
        if day in days:
            not_right_day = False
        else:
            day = input('Please choose the right day among Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday\n')
            continue
        
    return day


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
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # Adding the column for start station and end station trip
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print('The most common month is: ', df['month'].value_counts().iloc[[0]])

    # Display the most common day of week
    print('The most common day of week is: ', df['day_of_week'].value_counts().iloc[[0]])

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour is:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station is: ', df['Start Station'].value_counts().iloc[[0]])

    # Display most commonly used end station
    print('The most commonly used end station is: ', df['End Station'].value_counts().iloc[[0]])

    # Display most frequent combination of start station and end station trip
    print('The most most frequent combination of start station and end station trip is: ', df['Trip'].value_counts().iloc[[0]])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('The total travel time is: ', df[['Trip Duration']].sum())

    # Display mean travel time
    print('The mean travel time is: ', df.describe().loc['mean']['Trip Duration'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:\n', df['User Type'].value_counts())

    # Display counts of gender
    if df.get('Gender') is not None:
        print('Counts of gender types:\n', df['Gender'].value_counts())
    else:
        print('\nNo gender column for this city\n')

    # Display earliest, most recent, and most common year of birth
    if df.get('Birth Year') is not None:
        print('Earliest year of birth is: ', int(df['Birth Year'].min()))
        print('Most recent year of birth is: ', int(df['Birth Year'].max()))
        print('Most common year of birth is: ', df['Birth Year'].value_counts().iloc[[0]])
    else:
        print('No birth year column for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def display_raw_data(df, count=0):
    """Displaying raw data to user if they choose to"""
    
    choice = input('Would you like to see raw data? Choose "yes" or "no"\n')
    
    if choice == 'yes':
        start = count * 5
        end = start + 5
        print(df.iloc[start:end])
        return True
    
    else:
        return False


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        count = 0
        while display_raw_data(df, count):
            count += 1
            display_raw_data(df, count)
            if not display_raw_data(df, count):
                break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
