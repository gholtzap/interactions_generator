import pandas as pd
import re
import csv



# USER CHANGED VALUES
index_of_emplid = ord('A')-65
index_of_name_first = ord('C')-65
index_of_name_last = ord('D')-65
index_of_booking_room = ord('F')-65


def csv_to_text(csv_file, column_name, output_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    print(data.columns)
    
    # Check if the given column exists in the DataFrame
    if column_name not in data.columns:
        print(f"Column '{column_name}' not found in the CSV file.")
        return

    # Write the specified column to a text file
    with open(output_file, 'w') as f:
        for index, row in data.iterrows():
            f.write(str(row[column_name]) + '\n')

    print(f"Column '{column_name}' has been successfully written to {output_file}.")

def csv_to_list(csv_file, column_name):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Check if the given column exists in the DataFrame
    if column_name not in data.columns:
        print(f"Column '{column_name}' not found in the CSV file.")
        return []

    # Save the specified column as a list
    column_values = data[column_name].tolist()

    return column_values


csv_file = "Agave 3 Roster_FOR_API_TEST.csv"
column_name = "Unnamed: "+str(index_of_booking_room)
output_file = "output.txt"
csv_to_text(csv_file, column_name, output_file)

# FILTER EMPLIDS
pattern_emplid = re.compile(r'^\d{10}$')
emplid_values = csv_to_list(csv_file,"Unnamed: "+str(index_of_emplid))
filtered_emplid = [str(value) for value in emplid_values if pattern_emplid.match(str(value))]
#print(filtered_emplid)


# FILTER FIRST NAMES
pattern_firstname = re.compile(r'^[A-Z][a-z]*$')
firstname_values = csv_to_list(csv_file,"Unnamed: "+str(index_of_name_first))
filtered_firstname = [str(value) for value in firstname_values if pattern_firstname.match(str(value))]
#print(filtered_firstname)

# FIlTER LAST NAMES
pattern_lastname = re.compile(r'^[A-Z][a-z]*(-[A-Z][a-z]*)?$')
lastname_values = csv_to_list(csv_file,"Unnamed: "+str(index_of_name_last))
filtered_lastname = [str(value) for value in lastname_values if pattern_lastname.match(str(value))]
#print(filtered_lastname)

# FILTER BOOKING ROOMS

pattern_booking_rooms = re.compile(r'^[A-Z]{4}-\d{4}-A\d$')
bookingroom_values = csv_to_list(csv_file,"Unnamed: "+str(index_of_booking_room))

filtered_bookingroom = [str(value) for value in bookingroom_values if pattern_booking_rooms.match(str(value))]
#print(filtered_bookingroom)
extracted_bookingroom = [int(value[5:9]) for value in filtered_bookingroom]
#print(extracted_bookingroom)

# ADD INTERACTION ROW
number_interactions = [0] * len(extracted_bookingroom)

# COMBINE ALL VALUES INTO ONE LIST
# FORMAT: ID, FIRST, LAST, ROOM
combined_list = list(zip(filtered_emplid, filtered_firstname, filtered_lastname, extracted_bookingroom,number_interactions))

# END OF SETUP

with open("combined_data.csv", "w",newline='') as csvfile:
    
    csv_writer = csv.writer(csvfile)
    
    for record in combined_list:
        csv_writer.writerow(record)
    
    


