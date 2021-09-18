import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
	Asks user to specify a city, month, and day to analyze.

	Returns:
		(str) city - name of the city to analyze
		(str) month - name of the month to filter by, or "all" to apply no month filter
		(str) day - name of the day of week to filter by, or "all" to apply no day filter
	"""
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    avaliable_cities = ["chicago", "new york city", "washington"]
    avaliable_months = ["january", "february", "march", "april", "may", "june"]
    avaliable_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    filter_list = ["month", "day", "both", "none"]
    month = "none"
    day = "none"
    city = input("""What city do you wish to see data from, choose from the following
	, Chicago, New York city and Washington:\n """).lower()
    while city not in avaliable_cities:
        print("please enter a valid city name.")
        city = input(
            "What city do you wish to see data from, choose from the following, Chicago, New York city and Washington:\n ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    s_filter = input("would you like to filter by month,day,both or non of them? type 'none' for no filter.\n ").lower()
    while s_filter not in filter_list:
        print("Please enter a valid choice")
        s_filter = input(
            "would you like to filter by month,day,both or non of them? type 'none' for no filter.\n ").lower()
    if s_filter == "month" or s_filter == "both":
        month = input(
            "kindly choose one month from the following list, january, february,march,april,may or june:\n ").lower()
        while month not in avaliable_months:
            print("kidnly choose correct month")
            month = input(
                "kindly choose one month from the following list, january, february,march,april,may or june:\n ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if s_filter == "day" or s_filter == "both":
        day = input("kindly choose a day (monday,tuesday,wednesday,thursday,friday,saturday, and sunday):\n ").lower()
        while day not in avaliable_days:
            print("kindly choose correct day")
            day = input(
                "kindly choose a day (monday,tuesday,wednesday,thursday,friday,saturday, and sunday):\n ").lower()
    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['Month'] = df["Start Time"].dt.month
    df["week_day"] = df["Start Time"].dt.day_name()  # reference No. 1 in readme file

    if month != "none":
        avaliable_months = ["january", "february", "march", "april", "may", "june"]
        month = avaliable_months.index(month) + 1
        df = df.loc[df['Month'] == month]

    if day != "none":
        df = df.loc[df["week_day"] == day.title()]
    # print(df)
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.
		The function take in account the value of month and day
		if have been selected as filter to avoid unnessesary calculations."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    df['Start Time'] = pd.to_datetime(df["Start Time"])
    if month == "none":
        df["month"] = df["Start Time"].dt.month
        print("The most common month is:", df['month'].mode()[0])
    else:
        print("Common month : filter was set to 'month' or 'both'")
    # TO DO: display the most common day of week
    if day == "none":
        df['week_day'] = df["Start Time"].dt.day_name()
        print("The most common day is:", df["week_day"].mode()[0])
    else:
        print("common day : filter was set to 'day' or 'both'")
    # TO DO: display the most common start hour
    df['hour'] = df["Start Time"].dt.hour
    print("The most common hour is:", df["hour"].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #  display most commonly used start & end station
    common_start_station = df["Start Station"].value_counts().idxmax()  # Reference no. 2 in readme file
    common_end_station = df["End Station"].value_counts().idxmax()
    common = common_start_station, common_end_station
    print("The commonly used starting and end station is: ", common)
    # TO DO: display most frequent combination of start station and end station trip
    df["trips"] = "From (" + df["Start Station"] + ") toward (" + df["End Station"] + ")"
    common_trip = df["trips"].value_counts().idxmax()
    print("The most common trip starting ", common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    total_duriation_hours = df["Trip Duration"].sum() // 3600
    total_duriation_min = (df["Trip Duration"].sum() % 3600) // 60
    total_duration_sec = (df["Trip Duration"].sum() % 3600) % 60
    print("The total trips duration during requested filter is {} hours, {} minutes and {} seconds.".
          format(total_duriation_hours, total_duriation_min, int(total_duration_sec)))
    # TO DO: display mean travel time
    print("The trips duration mean value is: %s seconds." % (df["Trip Duration"].mean()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Info regarding number of users \n")
    print(df["User Type"].value_counts().to_frame())  # Reference no. 3 in readme file
    # TO DO: Display counts of gender
    try:
        print("\nInfo reagarding number of users' geneder")
        print(df["Gender"].value_counts().to_frame())
    except:
        print("No gender information available")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print("\nThe oldest users' year of birth is:", df["Birth Year"].min())
        print("The youngest users' year of birth is:", df["Birth Year"].max())
        print("The most common year of birth amoung users is:", df["Birth Year"].mode()[0])
    except:
        print("No birth year information avaliable")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(city):
    """ showes the user the raw data of the city chosen by the user"""
    response = input("Do you want to revise the raw data? (y/n)").lower()
    data = pd.read_csv(CITY_DATA[city])
    data = data.fillna(0)
    x = 0  # can be used as starting index
    y = 5  # can be used as go-to index
    while response == "y":
        print(data.iloc[x:y])
        x += 5
        y += 5
        response = input("Do you want to revise more data? (y/n)").lower()
        if y - 5 >= data.last_valid_index():  # Reference no. 4 in readme file
            print("end of file")
            break


def main():
    try:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            raw_data(city)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
    except KeyboardInterrupt:
        print("Calculation were interrupted, the program will stop")


if __name__ == "__main__":
    main()
