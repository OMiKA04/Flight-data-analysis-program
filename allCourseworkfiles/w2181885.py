"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: W2181885
 4. Date: 23.11.2025
****************************************************************************

"""

from graphics import *
import csv
import math
from collections import Counter

# Global variables to share airport/year 
GLOBAL_DEPARTURE_CODE = ""
GLOBAL_YEAR = ""

# List to hold all the flight data rows
data_list = []

# Dictionaries for mapping codes to full names
airport_code = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport Internationa",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International"
}

iata_code = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}

def load_csv(CSV_chosen):
    """
    This function loads any csv file by name into the list "data_list"
    """
    data_list.clear() 
    try:
        with open(CSV_chosen, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                data_list.append(row) 
    except FileNotFoundError:
        print(f"Error: The file {CSV_chosen} was not found. Please ensure it is in the same directory.")
        
        
def city_code_validation():  
    # Ask user for input and convert to uppercase
    city_code = input("Please enter a three-letter city code: ").upper()
    
    # Loop until a valid code is entered
    while True:
        if len(city_code) != 3:
            city_code = input("Wrong code length - please enter a three-letter city code: ").upper()
        elif city_code not in airport_code.keys():
            city_code = input("Unavailable city code - please enter a valid citycode: ").upper()
        else:
            break # Exit loop if input is valid
    return city_code

def year_validation():
    year = input("Please enter the year required in the format YYYY: ")
    
    # Loop until a valid year (2004-2025) is entered
    while True:
        if len(year) != 4 or not year.isdigit():
            year = input("Wrong data type - please enter a four-digit year value: ")
        elif int(year) >= 2004 and int(year) <= 2025:
            break # Exit loop if input is valid
        else:
            year = input("Out of range - please enter a value from 2004 to 2025: ")
    return year

def selected_file_name():
    # Get validated inputs
    city_code = city_code_validation()
    print("\n")
    year = year_validation()
    
    # Create filename 
    file_name = f'{city_code}{year}.csv'
    return file_name, city_code, year

def number_of_flights():
    global GLOBAL_DEPARTURE_CODE
    global GLOBAL_YEAR
    
    # Get file details and load data
    selected_data_file, city_code, year = selected_file_name()
    GLOBAL_DEPARTURE_CODE = city_code
    GLOBAL_YEAR = year
    
    load_csv(selected_data_file)
    
    # If file was empty or not found, return zeros
    if not data_list:
        return 0, 0, 0, 0, 0.0, 0.0, 0.0, [], 0
        
    # Count flights where terminal is "2"
    terminal_2 = sum(1 for row in data_list if row[8].strip() == "2")
    
    # Count flights where distance is less than 600
    under_600 = sum(1 for row in data_list if int(row[5]) < 600)
    
    # The total number of departure flights by Air France aircraft.
    af_flights = sum(1 for row in data_list if row[1][0:2] == "AF")
    
    # The total number of flights departing in temperatures below 15C
    temp_under_15 = sum(1 for row in data_list if int(row[10][0:2]) < 15)
    
    # Average BA flights per hour
    ba = sum(1 for row in data_list if row[1][0:2] == "BA")
    ba_avg = ba/12 # Average per hour (12 hour window)
    ba_planes = round((ba/len(data_list))*100,2) if len(data_list) > 0 else 0.00
    
    # Air France Delay Calculation
    # Only counts if Actual Time (row[6]) < Scheduled Time (row[7])? NOTE: Logic seems to check if flight arrived earlier/later. 
    af_delayed = sum(1 for row in data_list if row[1][0:2] == "AF" and row[6] < row[7]) / (af_flights if af_flights > 0 else 1) * 100

    # Rain Hours Calculation
    rain_hours = set() # Use a set to store unique hours
    for row in data_list: 
        if "rain" in row[10].lower(): # Check weather column
            hour = row[2].split(":")[0] # Extract hour from time
            rain_hours.add(hour) 
    total_rain_hours = len(rain_hours)
    
    # Least Common Destination Calculation
    destination_counts = Counter(row[4] for row in data_list)
    if destination_counts:
        least_count = min(destination_counts.values())
        # Find all airports that share the minimum count
        least_common_names = [airport_code.get(code, code)
            for code, count in destination_counts.items()
            if count == least_count]
    else:
        least_common_names = []
    
    return terminal_2, under_600, af_flights, temp_under_15, ba_avg, ba_planes, af_delayed, least_common_names, total_rain_hours
    
def task_d_histogram():
    """
    Task D: Plots a horizontal histogram matching the visual template.
    """
    if not data_list:
        print("No data loaded. Cannot plot histogram.")
        return
        
    # --- Input Validation ---
    while True:
        airline_code = input("\nEnter the two-character Airline code to plot a histogram: ").upper()
        if airline_code in iata_code:
            break
        print("Unavailable Airline code please try again.")
        
    full_airline_name = iata_code[airline_code]
    full_airport_name = airport_code.get(GLOBAL_DEPARTURE_CODE, GLOBAL_DEPARTURE_CODE)
    year = GLOBAL_YEAR
    
    # Create a dictionary for hours 00 to 11
    hourly_flights = {h: 0 for h in range(12)}
    
    has_data = False
    for row in data_list:
        if row[1].startswith(airline_code): 
            try:
                hour = int(row[2].split(":")[0])
                # Only count flights between 00 and 11
                if 0 <= hour <= 11:
                    hourly_flights[hour] += 1
                    has_data = True
            except ValueError:
                continue

    if not has_data:
        print(f"No departing flights found for {full_airline_name} ({airline_code}) in the 00-11 range.")
        return

    # Create the graphics window
    WIN_W, WIN_H = 800, 600
    win = GraphWin("Histogram", WIN_W, WIN_H, autoflush=False)
    
    # 1. Background Color (Cream/Off-White)
    win.setBackground(color_rgb(250, 252, 245)) 

    # 2. Draw Title
    title_text = f"Departures by hour for {full_airline_name} from {full_airport_name} {year}"
    title = Text(Point(WIN_W/2, 50), title_text)
    title.setSize(16)
    title.setStyle("bold")
    title.setTextColor(color_rgb(80, 80, 80))
    title.draw(win)

    # 3. Layout Constants (defining where bars go)
    LEFT_AXIS_X = 150
    TOP_Y = 100
    BOTTOM_Y = 550
    BAR_AREA_HEIGHT = BOTTOM_Y - TOP_Y
    BAR_COUNT = 12
    SLOT_HEIGHT = BAR_AREA_HEIGHT / BAR_COUNT
    BAR_HEIGHT = SLOT_HEIGHT * 0.6 # Bars take up 60% of slot height
    GAP = (SLOT_HEIGHT - BAR_HEIGHT) / 2
    
    # 4. Draw "Hours" Labels on the left
    label_center_y = TOP_Y + (BAR_AREA_HEIGHT / 2)
    
    lbl_hours = Text(Point(60, label_center_y - 20), "Hours")
    lbl_hours.setSize(12)
    lbl_hours.setStyle("bold")
    lbl_hours.setTextColor(color_rgb(80, 80, 80))
    lbl_hours.draw(win)
    
    lbl_range = Text(Point(60, label_center_y + 20), "00:00\nto\n12:00")
    lbl_range.setSize(10)
    lbl_range.setStyle("bold")
    lbl_range.setTextColor(color_rgb(80, 80, 80))
    lbl_range.draw(win)

    # 5. Determine Scaling 
    max_count = max(hourly_flights.values())
    if max_count == 0: max_count = 1
    MAX_BAR_WIDTH = WIN_W - LEFT_AXIS_X - 100 
    scale = MAX_BAR_WIDTH / max_count

    # 6. Draw Axis Line
    Line(Point(LEFT_AXIS_X, TOP_Y), Point(LEFT_AXIS_X, BOTTOM_Y)).draw(win)

    # 7. Loop to Draw Bars
    current_y = TOP_Y
    BAR_FILL = color_rgb(240, 160, 170) # Pinkish color
    TEXT_COLOR = color_rgb(60, 60, 60)

    for hour in range(12):
        count = hourly_flights[hour]
        
        # Calculate Bar Coordinates
        y1 = current_y + GAP
        y2 = y1 + BAR_HEIGHT
        bar_len = count * scale
        
        # A. Draw the Bar itself
        if count > 0:
            bar = Rectangle(Point(LEFT_AXIS_X, y1), Point(LEFT_AXIS_X + bar_len, y2))
            bar.setFill(BAR_FILL)
            bar.setOutline(color_rgb(100, 100, 100)) 
            bar.draw(win)
            
            # B. Draw the number count to the right of the bar
            val_text = Text(Point(LEFT_AXIS_X + bar_len + 15, (y1+y2)/2), str(count))
            val_text.setSize(10)
            val_text.setStyle("bold")
            val_text.setTextColor(TEXT_COLOR)
            val_text.draw(win)

        # C. Draw the Hour Label to the left
        hour_str = f"{hour:02d}"
        lbl = Text(Point(LEFT_AXIS_X - 20, (y1+y2)/2), hour_str)
        lbl.setSize(10)
        lbl.setStyle("bold") 
        lbl.setTextColor(TEXT_COLOR)
        lbl.draw(win)
        
        # Move down to next slot
        current_y += SLOT_HEIGHT
        
    # Handling the graphics error when manually closing the window
    try:
        win.flush() # Force update
        print(f"\nTask D Histogram displayed. Click the window to close.")
        win.getMouse() # Wait for click
        win.close()
    except GraphicsError:
        print(" ")


def save_results():
    # Run calculations
    terminal_2, under_600, af_flights, temp_under_15, ba_avg, ba_planes, af_delayed, least_common_names, total_rain_hours = number_of_flights()

    filename = "results.txt"
    full_airport_name = airport_code.get(GLOBAL_DEPARTURE_CODE, GLOBAL_DEPARTURE_CODE)
    csv_file_name = f"{GLOBAL_DEPARTURE_CODE}{GLOBAL_YEAR}.csv"

    # Write results to a text file 
    with open(filename,"a") as f: 
        f.write("*"*75 + "\n")
        f.write(f"File {csv_file_name} selected - Planes departing {full_airport_name} {GLOBAL_YEAR}\n")
        f.write("*"*75 + "\n")
        f.write(f"The total number of flights from this airport was {len(data_list)}\n")
        f.write(f"The total number of flights departing Terminal Two was {terminal_2}\n")
        f.write(f"The total number of departures on flights under 600 miles was {under_600}\n")
        f.write(f'There were {af_flights} Air France flights from this airport\n')
        f.write(f'There were {temp_under_15} flights departing in temperatures below 15 degrees\n')
        f.write(f"There was an average of {ba_avg:.2f} British Airways flights per hour from this airport\n")
        f.write(f'British Airways planes made up {ba_planes}% of all departures\n')
        f.write(f'{round(af_delayed,2)}% of Air France departures were delayed\n')
        f.write(f"There were {total_rain_hours} hours in which rain fell\n")
        f.write(f"The least common destinations are {least_common_names}\n")
        f.write("\n") 
    
    # Print the same results to the console
    print("\n")
    print("*"*75)
    print(f"File {csv_file_name} selected - Planes departing {full_airport_name} {GLOBAL_YEAR}")
    print("*"*75)
    print(f"The total number of flights from this airport was {len(data_list)}")
    print(f"The total number of flights departing Terminal Two was {terminal_2}")
    print(f"The total number of departures on flights under 600 miles was {under_600}")
    print(f'There were {af_flights} Air France flights from this airport')
    print(f'There were {temp_under_15} flights departing in temperatures below 15 degrees')
    print(f"There was an average of {ba_avg:.2f} British Airways flights per hour from this airport")
    print(f'British Airways planes made up {ba_planes}% of all departures')
    print(f'{round(af_delayed,2)}% of Air France departures were delayed')
    print(f"There were {total_rain_hours} hours in which rain fell")
    print(f"The least common destinations are {least_common_names}")
    print("\n")
    
    # Launch the histogram 
    task_d_histogram()
    

# Main Program Loop

def main():
    # Run the initial analysis
    save_results()
    
    # Main program loop to allow restarting
    while True:
        # validating Yes/No input
        while True:
            user_choice = input("\nDo you want to select a new data file? Y/N: ").upper()
            if user_choice in ('Y', 'N'):
                break
            print("Invalid input. Please enter 'Y' or 'N'.")
            
        if user_choice == 'N':
            print("Exiting program.")
            break
        
        save_results()

if __name__ == "__main__":
    main()