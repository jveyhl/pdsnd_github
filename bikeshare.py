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
    cities = ["chicago", "new york city", "washington"]
    
    while True:
        try:
            x = input("Enter chicago, new york city or washington: ")
            # verify that input is in list of cities and retrieve index
            cityindex = cities.index(x)
            city = cities[cityindex]
            break
        except:
            print("Invalid input; enter chicago, new york city or washington")

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    while True:
        try:
            month = input("Enter all, january, february, march, april, may or june: ")
            # filter by month if applicable
            if month != "all":
                # use the index of the months list to get the corresponding int; in df jan = 1...jun = 6              
                month = months.index(month)+1
                break
            elif month == "all":
                break
        except:
            print("Invalid input; enter all, january, february, march, april, may or june:")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["all", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    while True:
        try:
            day = input("Enter all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday: ")
            if day != "all":
                day = day.title()
            if day in days:
                break
        except:
            print("Invalid input; enter all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday:")

    print("-"*40)
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
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popmonth = df["month"].mode()[0]
    print('Most frequent month:', popmonth)

    # display the most common day of week
    popdow = df["day_of_week"].mode()[0]
    print('Most frequent day of the week:', popdow)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    pophour = df['hour'].mode()[0]
    print('Most frequent start hour:', pophour)
 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popstart = df["Start Station"].mode()[0]
    print('Most frequent start station:', popstart)

    # display most commonly used end station
    popend = df["End Station"].mode()[0]
    print('Most frequent end station:', popend)

    # display most frequent combination of start station and end station trip
    # make new column that combines start and end stations
    df["start_end"] = df["Start Station"]+" to "+df["End Station"]
    popstartend = df["start_end"].mode()[0]
    print('Most frequent start station and end station combination:', popstartend)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in minutes
    tot_tt = df["Trip Duration"].sum()/60
    print("The total travel time is", tot_tt, "minutes")

    # display mean travel time in minutes
    avg_tt = df["Trip Duration"].mean()/60
    print("The average (mean) travel time is", avg_tt, "minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    utcounts = df["User Type"].value_counts()
    print("The counts for each user type are:\n", utcounts, sep = "")

    # Display counts of gender
    gencounts = df["Gender"].value_counts()
    print("\nThe counts for each gender are:\n", gencounts, sep = "")

    # Display earliest, most recent, and most common year of birth
    by_earliest = int(df["Birth Year"].min())
    by_mostrec = int(df["Birth Year"].max())
    by_common = int(df["Birth Year"].mode()[0])
    print("\nThe earliest, most recent, and most common year of birth, respectively are:", by_earliest, by_mostrec, by_common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        # washington.csv doesn't have a "Gender" column.
        if city != "washington":
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

