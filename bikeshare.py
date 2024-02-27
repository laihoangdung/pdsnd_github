import numpy as np
import pandas as pd
import time
import datetime

# Global variables
CITIES = ['chicago', 'new york', 'washington']
DAYS_OF_WEEK = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
DAYS_OF_WEEK_NAME = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'sep']
ANSWER_FOR_VIEWING_RAW_DATA = ["yes", "no"]

# CITY DATA
CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv' 
}


# Get input value and validation
def get_input(values, question, add_all_option=True):
    """
    Get input and validate

    :params
        values (list): the input value should be one of elements in this list
        question (string): input question
        add_all_option: add all options to get all data
    
    :return
        input value
    """
        
    question = f"{question} {', '.join(values)}"
    if add_all_option:
        question += f" or all"

    if add_all_option:
        values.append("all") # additional value for getting all data

    question += "(Case insensitive is allowed)"

    value = input(f"{question}: ")
    value = value.lower()

    while value not in values:
        print("Wrong input value. Please try again !!!")
        value = input(f"{question}: ")
        value = value.lower()

    return value


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york, washington)
    city = get_input(CITIES, "Which city would you like to see the data ?", False)

    # get user input for month (all, january, february, ... , june)
    month = get_input(MONTHS, "Which month?")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_input(DAYS_OF_WEEK, "Which day?")


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

    day_name = DAYS_OF_WEEK_NAME[DAYS_OF_WEEK.index(day)] if day != "all" else day
    print(f"*** Load data for city: {city}, month: {month}, day: {day_name} ***")
    df = pd.read_csv(CITY_DATA[city])

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    df["month"] = df["Start Time"].dt.month
    df["weekday"] = df["Start Time"].dt.weekday
    df["hour"] = df["Start Time"].dt.hour

    # Filter
    if month != "all":
        df = df[df["month"] == (MONTHS.index(month) + 1)]
    
    if day != "all":
        df = df[df["weekday"] == DAYS_OF_WEEK.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        most_common_month = df["month"].mode()[0]
        print('Most common month:', most_common_month)
    except:
        print("There is no data for month")

    # display the most common day of week
    try:
        most_common_day = df["weekday"].mode()[0]
        print('Most common day:', DAYS_OF_WEEK_NAME[most_common_day])
    except:
        print("There is no data for weekday")

    # display the most common start hour
    try:
        most_common_hour = df["hour"].mode()[0]
        print('Most common hour:', most_common_hour)
    except:
        print("There is no data for hour")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        most_start_station = df["Start Station"].mode()[0]
        print('Most start station:', most_start_station)
    except:
        print("There is no data for start station")

    # display most commonly used end station
    try:
        most_end_station = df["End Station"].mode()[0]
        print('Most end station:', most_end_station)
    except:
        print("There is no data for end station")

    # display most frequent combination of start station and end station trip
    try:
        most_start_end_station = (df["Start Station"] + ' to ' + df["End Station"]).mode()[0]
        print('Most start station and end station trip:', most_start_end_station)
    except:
        print("There is no data to calcualte the most start station and end station")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def convert_second_to_time_format(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return "%d:%02d:%02d" % (hours, minutes, seconds)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    try:
        duration = df["Trip Duration"].sum()
        print("Total travel time is: ", convert_second_to_time_format(duration))

        # display mean travel time
        mean = df["Trip Duration"].mean()
        print("Mean travel time is: ", convert_second_to_time_format(mean))
    except:
        print("There is no data for trip duration")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types = df["User Type"].value_counts()
        print("User types stats: ", user_types)
        print("-"*20)
    except:
        print("There is no data for user type")

    # Display counts of gender
    try:
        gender = df["Gender"].value_counts()
        print("Gender stats: ", gender)
        print("-"*20)
    except:
        print("There is no data for gender")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df["Birth Year"].min()
        most_recent = df["Birth Year"].max()
        common_year = df["Birth Year"].mode()[0]

        print("Earliest birth year: ", int(earliest))
        print("Most recent birth year: ", int(most_recent))
        print("Common birth year: ", int(common_year))
    except:
        print("There is no data for birth year")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(df):
    print("View raw data from data source ....")
    answer = get_input(ANSWER_FOR_VIEWING_RAW_DATA, "Do you want to view raw data?", False)
    index = 0
    if answer == "yes":
        print(df.head())
        index += 5

        while answer == "yes":
            answer = get_input(ANSWER_FOR_VIEWING_RAW_DATA, "Do you want to view next 5 rows?", False)
            if answer == "yes":
                print(df[index: index+5])
                index += 5
    else:
        return

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()