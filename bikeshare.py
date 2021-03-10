import time
import calendar
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

    # get user input for city (chicago, new york city, washington). HINT: Use a
    # while loop to handle invalid inputs

    city = input("""Select the city to analyze using the first letter of the city:
        Chicago (c), New York City (n), Washington (w).  """)

    while city[0] not in ['c', 'n', 'w']:
        city = input("""Please only select the city to analyze using the first letter of the city:
        Chicago (c), New York City (n), Washington (w). """)

    if city[0] == 'c':
        city = 'chicago'
    elif city[0] == 'n':
        city = 'new york city'
    else:
        city = 'washington'

    # get user input for month (all, january, february, ... , june)

    month = input("""Select the month to analyze using month number:
        All (all), Jan (1), Feb (2), Mar(3), Apr (4), May (5), Jun (6).  """)

    while month not in ['all', '1', '2', '3', '4', '5', '6']:
        month = input("""Please only select the month (or all) to analyze using month number:
        All (all), Jan (1), Feb (2), Mar(3), Apr (4), May (5), Jun (6).  """)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("""Select the day to analyze using 'all' or the day number:
        All (all), Mon (0), Tue (1), Wed (2), Thu (3), Fri (4), Sat (5), Sun (6).  """)

    while day not in ['all', '0', '1', '2', '3', '4', '5', '6']:
        day = input("""Please only select the day to analyze (or all) using the day number:
        All (all), Mon (0), Tue (1), Wed (2), Thu (3), Fri (4), Sat (5), Sun (6).  """)

    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':

        # filter by month to create the new dataframe
        df = df[df['month'] == int(month)]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == calendar.day_name[int(day)].title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month

    # find the most popular month
    popular_month = calendar.month_name[df['month'].mode()[0]]

    print('Most Popular Month:', popular_month)

    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract day from the Start Time column to create an day column
    df['day'] = df['Start Time'].dt.day

    # find the most popular day
    popular_day = df['day'].mode()[0]

    print('Most Popular Day:', popular_day)

    # display the most common start hour

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].mode()[0]

    print('Most Popular Starting Station is:', popular_start_station)

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]

    print('Most Commonly Used End Station is:', popular_end_station)

    # display most frequent combination of start station and end station trip

    df['Combo Stations'] = df['Start Station'] + ' to ' + df['End Station']

    popular_combination = df['Combo Stations'].mode()[0]

    print('Most Frequent Combination of stations is:', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum() // 60

    print('Total Travel Time: {} minutes'.format(total_travel_time))

    # display mean travel time

    mean_travel_time = df['Trip Duration'].mean() // 60

    print('Mean Travel Time: {} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_type = df.groupby('User Type')['User Type'].count().to_string(header=False)

    print('User Types:\n{}\n'.format(user_type))

    # Display counts of gender

    if 'Gender' in df:
        user_gender = df.groupby('Gender')['Gender'].count().to_string(header=False)

        print('Gender:\n{}\n'.format(user_gender))
    else:
        print('Gender data not available in this data set')

    # Display earliest, most recent, most common year of birth, and average age of riders

    if 'Birth Year' in df:

        earliest_birth = format(df['Birth Year'].min(), 'n')

        most_recent_birth = format(df['Birth Year'].max(), 'n')

        most_common_birth = format(df['Birth Year'].mode()[0], 'n')

        avg_age = format((int(time.strftime("%Y")) - df['Birth Year']).mean(),'.0f')

        print('Earliest Birth Year:', earliest_birth)
        print('Most Recent Birth Year:',most_recent_birth)
        print('Most Common Birth Year:',most_common_birth)
        print('The Average Age of Riders was:', avg_age)
    else:
        print('Birth Year data not available in this data set')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Asks if the user would like to see raw data. Continues asking for 5 more rows until no"""

    print('\nViewing Raw Data...\n')
    start_time = time.time()

    start = 0

    # Ask if the user wants to see five lines of raw data

    show_raw_data = input("""\nWould you like to see raw data? yes or no.  """)
    while show_raw_data not in ['yes','no']:
        show_raw_data = input("""Please only select yes or no.  """)

    # Present Raw Data
    if show_raw_data == 'yes':
        print("\n",df[start:start ++ 5])

    if show_raw_data == 'no':
        return

    # Ask if user would like to see 5 more lines, until the user indicates no
    while True:
        show_again = input("""\nDo you want to see 5 more lines of raw data? yes or no.  """)
        while show_again not in ['yes','no']:
            show_again = input("""Please only select yes or no.  """)
        if show_again == 'no':
            return
        start += 5
        print("\n",df[start:start ++ 5])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
