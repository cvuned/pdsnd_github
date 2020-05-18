import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

valid_months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
valid_days = ('monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'mo', 'tu', 'we', 'th', 'fr', 'sa', 'su', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all')    

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
    
    city_list = ['new york city', 'washington', 'chicago']
    while True: 
        
        city = str(input('Which city do you want to Explore? Chicago, New York City or Washington?  ')).lower() 
        if city in city_list: 
            print('Great! \n You have decided to explore {}. \n'.format(city.title()))
            break
        else: 
            print('\n Unexpected data input! \n Sorry, you tried selecting {}, but we only have data for Chicago, New York City and Washington'.format(city))
        
    # TO DO: get user input for month (all, january, february, ... , june)
    while True: 
        
        month = str(input('What month do you want to explore? Choose \'all\' to see all our data. \n Otherwise, select a month between January and June.  ')).lower() 
        if month in valid_months: 
            print('Great! \n You have decided to explore {}.\n'.format(month.title()))
            break
        else: 
            print('\n Unexpected data input! \n Sorry, you tried selecting {}, we could not recognize that as a valid month.'.format(month))
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
            
    while True: 


        day = str(input('What month do you want to explore? Choose \'all\' to see all our data. \n You can also write the days as \'mo\', \'tu\', \'we\', \'th\', \'fr\', \'sa\', \'su\'.  ')).lower()
        if day in valid_days: 
            print('Great!\n You have decided to explore {}. Let\'s start. \n'.format(day.title()))
            if day != 'all': 
                # gets the index with modulo(7) to equate mo == monday  
                day = valid_days[valid_days.index(day)%7]                                              
            break
        else: 
            print('\n Unexpected data input! \n Sorry, you tried selecting {}, we could not recognize that as a valid day. '.format(day))
    print('\n We will be exploring {} data for: Month = {}, Day = {}. '.format(city.title(),month.title(),day.title()))
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
    df = pd.read_csv(CITY_DATA[city])
   
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.weekday_name
    # hour column added for ease
    df['Hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = valid_months[df['Month'].mode()[0]].title()
    print('{} is the most popular month'.format(popular_month))
    
    # TO DO: display the most common day of week
    popular_day = df['Day_of_week'].mode()[0]
    print('{} is the most popular day of the week'.format(popular_day))


    # TO DO: display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('{} is the most popular start hour'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('{} is the most popular start station'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('{} is the most popular end station'.format(popular_end_station))
    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = 'from '+ df['Start Station'] + ' to ' + df['End Station']
    #print(df['Trip'].head())                          
    popular_trip = df['Trip'].mode()[0] 
    print('Going {} is the most popular trip'.format(popular_trip))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print(df['Trip Duration'].sum(axis=0))
    total_travel_time = df['Trip Duration'].sum(axis=0)
    total_travel_time_breakdown = [total_travel_time, 0, 0, 0, 0]
    conversion_ratio = [60, 60, 24, 365]
    
    # The following loop breaks down the total travel time in seconds into bigger units (years, days, hours and minutes 
    for i in range(len(total_travel_time_breakdown)-1): 
        total_travel_time_breakdown[i+1] = total_travel_time_breakdown[i] // conversion_ratio[i]
        total_travel_time_breakdown[i] = total_travel_time % conversion_ratio[i]
    total_travel_time_breakdown.reverse()
    print('The accumulated travel time is {} seconds. \n That is: {} year(s), {} day(s), {} hour(s), {} minute(s) and {} second(s).'.format(total_travel_time, total_travel_time_breakdown[0], total_travel_time_breakdown[1], total_travel_time_breakdown[2],total_travel_time_breakdown[3],total_travel_time_breakdown[4]))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is {} seconds.'.format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print('\n')

    # TO DO: Display counts of gender
    if 'Gender' in df: 
        genders = df['Gender'].value_counts()
        print(genders)
        print('\n')
    else: 
        print('Unfortunately no gender data is available for this city.')
    
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df: 
        earliest_birth = int(df['Birth Year'].min())
        print('{} is the earliest year of birth.'.format(earliest_birth))
        
        most_recent_birth = int(df['Birth Year'].max())
        print('{} is the most recent year of birth.'.format(most_recent_birth))
        
        popular_birth_year = int(df['Birth Year'].mode()[0])
        print('{} is the most common year of birth.'.format(popular_birth_year))

    else: 
        print('Unfortunately no birth year data is available for this city.')

        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_raw_data(df): 
    # This function displays raw data on request of the column being examined, 5 lines at a time. 
    valid_columns = ['Start Time', 'End Time', 'Trip Duration','Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year','Month', 'Day_of_week', 'Hour', 'Trip']

    # This FIRST While block checks if the user wants to see any data at all.
    while True: 
        user_wants_raw_data = str(input('Do you want to see raw data? \n')).lower() 
        if user_wants_raw_data == 'yes': 
            lines_displayed = 0
            # This SECOND While block checks what data the user wants to see, if any.
            while True:
                print('\n These are the columns that can be explored:')
                print(valid_columns)
                #if lines_displayed == 0: 
                column = str(input('What data do you want to see?\n')).title() 
                if column in valid_columns: 
                    # Now we print data, 5 rows at a time until the user doesn't want to see more data
                    user_wants_more_data = 'yes' # The first five lines are always displayed 
                    while True: 
                        if user_wants_more_data in ('yes', ''): 
                            if lines_displayed+5 < df[column].shape[0]:
                                print(df[column][lines_displayed:lines_displayed+5])
                                lines_displayed += 5
                                # If there are less than 5 lines remaining, checks how many and displays them: 
                            elif lines_displayed+5 < df[column].shape[0]: 
                                print(df[column][lines_displayed:])
                                print('All data has been displayed')
                                break
                            else:
                                break
                        elif user_wants_more_data in ('no', 'stop', 'quit', 'q','cancel', 'I regret my poor decisions'):
                            break
                        else: 
                            print('\n Unexpected data input! \n Please, write \'yes\' or press \'Enter\' to continue. \n Otherwise, write \'no\'.')
                        user_wants_more_data = str(input('Do you want to see more data?\n')).lower()
                elif column in ('', 'no', 'stop', 'quit', 'q','cancel', 'I regret my poor decisions'):
                    break
                else: 
                    print('\n Unexpected data input! \n Please, select a column. \n Otherwise, write \'no\' or press enter to continue.')

        elif user_wants_raw_data in ('no',''): 
            print('Ok! Let\'s continue.')
            break
        else: 
            #print('user input = -->{}<-- .'.format(user_wants_raw_data)) 
            print('\n Unexpected data input! \n Please, answer \'yes\' if you want to see more data. \n Otherwise, write \'no\' or press enter to continue.')
  
          
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Raw data is displayed upon request by the user
        display_raw_data(df)      
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
