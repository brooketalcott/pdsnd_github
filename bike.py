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
    def prompt_user(prompt,validate):
        while True:
            try:
                response = input(prompt).lower()
            except ValueError:
                print('That didn\'t make sense to me.')
                continue
            if response in validate:
                break
            else:
                print("\n\n\n\nSorry, that's not one of the options.\n"
                'Please try again')
                continue
        return response

    cities = (
    'chicago','new york city', 'washington'
    )
    months = (
    'all','january','february','march','april','may','june','july'
    )
    days = (
    'all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'
    )

    city = (prompt_user('\n'
    'Which city would you like to see?\n'
    'Choose from Chicago, New York City, or Washington\n\n',cities))

    month = (prompt_user('\nWe can look at the data by month\n'
    'We have data from January through July.\n'
    'Let me know which month you\'d like to see,\nor type "all" to see all of'
    ' them\ne.g. January\n\n',months))

    day = prompt_user('\nAre you interested in any particular day of the week?'
    '\nType in the day of the week,\nor enter "all" to see all of them'
    '\ne.g. Monday\n\n',days)

    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = [
        'january','february','march','april','may','june','july',
        'august','september','october','november','december'
        ]
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def print_pop_stats(df,options):
    """displays the statistics about the most popular option passed to function"""
    def popular(option):
        return df[option].mode()[0]

    for readable, findable in options.items():
        print('The Most Popular',readable,popular(findable))

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    options = {
    'Travel Month:': 'month',
    'Day of Week:': 'day_of_week',
    'Start Hour:': 'hour'
    }
    df['hour'] = df['Start Time'].dt.hour

    print_pop_stats(df,options)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    options = {
    'starting station:':'Start Station',
    'ending station:': 'End Station',
    'trip:':'Trip'
    }
    df['Trip'] =  df['Start Station'].str.cat(df['End Station'], sep=' to ')
    print_pop_stats(df,options)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    def readable_time(time):
    #https://www.w3resource.com/python-exercises/python-basic-exercise-65.php
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minute = time // 60
        time %= 60
        second = time
        return "%d days %d hours %d minutes %d seconds"%(day,hour,minute,second)

    total_travel_time = readable_time(df['Trip Duration'].sum())

    print('Travelers spent a total of ',total_travel_time)

    # display mean travel time
    avg_duration = readable_time(df['Trip Duration'].mean())
    print('Average travel time was ', avg_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df.Gender.value_counts()
        print(gender_counts,'\n')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_dob = df['Birth Year'].min()
        max_dob = df['Birth Year'].max()
        common_dob = df['Birth Year'].mode()[0]

        print(f'Youngest riders were born in {int(max_dob)}.\n'
        f'Oldest riders were born in {int(min_dob)}.\n'
        f'The most common birth year was {int(common_dob)}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Raw data is displayed upon request by the user in this manner:
    Script should prompt the user if they want to see 5 lines of raw data,
    display that data if the answer is 'yes', and continue these prompts and
    displays until the user says 'no'."""

    while True:
        response = input('Would you like to see 5 lines of raw data?\n'
        'yes or no\n')
        try:
            valid_responses = ['yes', 'no']
            if response.lower() not in valid_responses:
                print('\n\n'
                'Please keep in mind the rubric was specific about this,'
                '\nI need a yes or no.\n')
                continue
            if response.lower() == 'no':
                break
            if response.lower() == 'yes':
                sample_data = df.sample(n=5).to_csv(index=False,header=False)
                print('\n',sample_data)
                continue
        except ValueError:
            print('That didn\'t make sense to me.')
            continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes (y) or no.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
