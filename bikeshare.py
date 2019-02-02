from datetime import datetime
import time
import pandas as pd
import sys, traceback
import numpy as np
import calendar

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def city_filter():
    """Fetch the city name from the user input"""
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York, "
                     "or Washington?\nEnter the name of the city you "
                     "want to explore some bikeshare data:\n").lower()
        if city == "new york":
            city = "new york city"
        if city in CITY_DATA.keys():
            break
        print("Wrong entry. You can enter only Chicago, New York "
              "City or Washington.\n")

    return city


def month_day_filter():
    """Fetch the month and day of the week from the user input"""
    # get user input for month (all, january, february, ... , june)
    month = None
    day = None
    day_month_list = ['month', 'day', 'none', 'both']

    while True:
        day_month = input("\nWould you like to filter the bikeshare data by "
                          "month, day, both or not at all?\nType day for "
                          "filter by 'Day'. Type month for filter by "
                          "'Month'. Type 'Both' for filtering both by month "
                          "and day. Type 'none' for no time filter.\n").lower()
        if day_month in day_month_list:
            break
        print("Wrong entry. You can enter only 'day', 'month', 'both' or "
              "'none'")

    while True:
        month_list = ['january', 'february', 'march', 'april', 'may',
                      'june']
        day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']

        if day_month == "both":
            month = input("Which month? January, February, March, "
                          "April, May, June:\n").lower()
            if month in month_list:
                pass
            else:
                print("\nWrong input. Please enter a valid month\n")
                continue

            while True:
                day = input("Which day? Please enter an integer (Ex: 0 for "
                            "Monday).\nAlso you can enter Monday, Tuesday, "
                            "Wednesday, Thursday, Friday, Saturday, "
                            "Sunday:\n").lower().title()
                try:
                    day = int(day)
                    if 0 <= day <= 6:
                        day = calendar.day_name[day]
                        break
                    else:
                        print("\nWrong input. Please enter a valid integer "
                              "mapped day\n")
                        continue
                except ValueError:
                    if day in day_list:
                        break
                    else:
                        print("\nWrong input. Please enter a valid day\n")
                        continue
            break

        # get user input for day of week (all, monday, tuesday, ... sunday)
        elif day_month == "none":
            day = None
            month = None
            break

        elif day_month == "month":
            month = input("Which month? January, February, March, April, "
                          "May, June:\n").lower()

            if month in month_list:
                break
            else:
                print("\nWrong input. Please enter a valid month\n")
                continue

        elif day_month == "day":
            day = input("Which day? Please enter an integer (Ex: 0 for "
                        "Monday).\nAlso you can enter Monday, Tuesday, "
                        "Wednesday, Thursday, Friday, Saturday, "
                        "Sunday\n").lower().title()
            try:
                day = int(day)
                if 0 <= day <= 6:
                    day = calendar.day_name[day]
                    break
                else:
                    print("\nWrong input. Please enter a valid integer "
                          "mapped day\n")
                    continue

            except ValueError:
                if day in day_list:
                    break
                else:
                    print("\nWrong input. Please enter a valid day\n")
                    continue
    return month, day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let's explore some US bikeshare data!")
    city = city_filter()
    month, day = month_day_filter()

    print('-' * 40)
    return city, month, day


def load_month_data(month, df):
    """filter by month to create the new dataframe"""
    # use the index of the months list to get the corresponding int
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months.index(month) + 1

    # filter by month to create the new dataframe
    df = df[df['month'] == month]
    # print(df.head())
    return df


def load_day_data(day, df):
    """filter by day of week to create the new dataframe"""
    df = df[df['day_of_week'] == day.title()]
    # print(df.head())
    return df


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

    # Print out the full DataFrame in single window
    pd.set_option('display.expand_frame_repr', False)

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month is not None:
        df = load_month_data(month, df)

    # filter by day of week if applicable
    if day is not None:
        df = load_day_data(day, df)
    return df


def load_individual_trip(df):
    """Displays individual details based on user entry(Y/N)"""
    while True:
        individual_data = input("\nWould you like to see more details on "
                                "individual trips?\nType Yes(y) or "
                                "No(n):\n").lower()
        if individual_data == 'y' or individual_data == 'yes' or \
                individual_data == 'n' or individual_data == 'no':
            if individual_data == 'y' or individual_data == 'yes':
                print(df.head())
                continue
            else:
                break
        else:
            print("Invalid input. Please type Yes(y) or No(n)")


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month is None:
        popular_month = df['month'].value_counts().reset_index()['index'][0]
        popular_month_name = calendar.month_name[popular_month]
        print("The most popular month: {}".format(popular_month_name))
    else:
        print("You have filter the results by month. Hence the popular "
              "month is {}".format(month))

    # display the most common day of week
    if day is None:
        popular_day = df['day_of_week'].value_counts().reset_index()['index'][0]
        print("The most popular day of the week: {}".format(popular_day))
    else:
        print("You have filter the results by day. Hence the popular "
              "day of the week is {}".format(day))

    # display the most common start hour
    df['hours'] = df['Start Time'].dt.hour
    popular_hour = df['hours'].value_counts().reset_index()['index'][0]
    print("The most popular hour of the week in 24 hour format: {} "
          "hours".format(popular_hour))
    popular_hour = datetime.strptime(str(popular_hour) + ":00", "%H:%M")
    print("The most popular hour of the week in 12 hour format: {} "
          "".format(popular_hour.strftime("%I:%M %p")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def sec_to_days(total_duration_sec):
    """Convert total duration seconds into days, hours, minutes and seconds"""
    days = int(total_duration_sec) // (24 * 3600)
    total_duration_sec = total_duration_sec % (24 * 3600)
    hours = total_duration_sec // 3600
    total_duration_sec %= 3600
    minutes = total_duration_sec // 60
    total_duration_sec %= 60
    seconds = total_duration_sec
    return days, hours, minutes, seconds


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration_sec = df['Trip Duration'].sum()
    days, hours, minutes, seconds = sec_to_days(total_duration_sec)

    print("Total trip duration: {} days {} hours {} minutes {} "
          "seconds".format(int(days), int(hours), int(minutes), int(seconds)))

    # display mean travel time
    average_duration_sec = df['Trip Duration'].mean()
    days, hours, minutes, seconds = sec_to_days(average_duration_sec)

    print("Average trip duration: {} days {} hours {} minutes {} "
          "seconds".format(int(days), int(hours), int(minutes), int(seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def popular_station_stats(df, station_type):
    popular_station = str(
        df[station_type].value_counts().reset_index()['index'][0])
    popular_station_count = int(
        df[station_type].value_counts().reset_index()[station_type][0])
    station_total_count = int(df[station_type].count())
    percentage_trip = (popular_station_count * 100) / station_total_count
    return popular_station, popular_station_count, percentage_trip


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station, popular_station_count, percentage_trip = popular_station_stats(
        df, 'Start Station')
    print("Most popular Start station: {}".format(popular_start_station))
    print("Trips from popular start station: {}".format(popular_station_count))
    print("The total percentage of trips from popular start station: {0:.2f}%".format(
            percentage_trip))

    # display most commonly used end station
    popular_end_station, popular_station_count, percentage_trip = popular_station_stats(
        df, 'End Station')
    print("\nMost popular end station: {}".format(popular_start_station))
    print("Trips from popular end station: {}".format(popular_station_count))
    print("The total percentage of trips from popular end station: {0:.2f}%".format(
            percentage_trip))

    # display most frequent combination of start station and end station trip
    sorted_popular_stations = df.groupby(['Start Station', 'End Station'])[
        'Start Station'].count().sort_values(ascending=False)
    total_trips = df['End Station'].count()
    percentage_trip = (sorted_popular_stations[0] * 100) / total_trips
    print("\nMost popular trip is:\nStart Station: {}\nEnd Station: {}\nTotal "
          "Trips: {}".format(
            sorted_popular_stations.index[0][0],
            sorted_popular_stations.index[0][1],
            sorted_popular_stations[0]))
    print("Trip percentage: {0:.2f}%".format(percentage_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The User types and their occurrences are:")
    for val, cnt in df["User Type"].value_counts().iteritems():
        print('User Type: {}\tOccurrences: {}'.format(val, cnt))

    if city != "washington":
        # Display counts of gender
        print("\nThe gender types and their occurrences are:")
        for val, cnt in df["Gender"].value_counts().iteritems():
            print('Gender: {}\tOccurrences: {}'.format(val, cnt))

        # Display earliest, most recent, and most common year of birth
        print(
            "\nThe earliest year of birth: {}".format(int(df['Birth Year'].min())))
        print("The most recent year of birth: {}".format(
            int(df['Birth Year'].max())))
        print("The most common year of birth: {}".format(
            int(df['Birth Year'].value_counts().reset_index()['index'][0])))
    else:
        print("\nNo gender and year of birth analysis for washington city")
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    try:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df, month, day)
            trip_duration_stats(df)
            station_stats(df)
            user_stats(df, city)
            load_individual_trip(df)
            restart_options = ['y', 'n', 'yes', 'no']
            while True:
                restart = input('\nWould you like to restart? Enter yes(y) or '
                                'no(n).\n').lower()
                if restart in restart_options:
                    break
                else:
                    print("Invalid Input.")
                    continue
            if restart == 'y':
                restart = 'yes'
            elif restart == 'n':
                restart = 'no'
            if restart.lower() != 'yes':
                break
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
