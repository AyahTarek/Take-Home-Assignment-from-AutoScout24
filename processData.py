import csv
# Import Data
def importData(FileName):

    input_list = []
    # to add row by row
    list_of_rows = []
    with open(FileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            for i in row:
                list_of_rows.append(i)
            break
        for row in csv_reader:
            list_per_row = []
            for i in range(len(list_of_rows)):
                list_per_row.append(row[i])
            input_list.append(list_per_row)
            line_count += 1
    return input_list

# Get average price per each type
def gettingAvgPerSellerType(input_list):

    private_seller_list = []
    private_seller_total = 0

    dealer_seller_list = []
    dealer_seller_total = 0

    other_seller_list = []
    other_seller_total = 0

    for item in input_list:
        # listing price field
        seller_price = int(item[2])
        # listing seller type field
        seller_type = item[4]

        if seller_type == 'private':
            private_seller_list.append(seller_price)
            private_seller_total = private_seller_total + seller_price

        elif seller_type == 'dealer':
            dealer_seller_list.append(seller_price)
            dealer_seller_total = dealer_seller_total + seller_price

        else:
            other_seller_list.append(seller_price)
            other_seller_total = other_seller_total + seller_price

    private_seller_avg = int(private_seller_total/len(private_seller_list))
    dealer_seller_avg = int(dealer_seller_total/len(dealer_seller_list))
    other_seller_avg = int(other_seller_total/len(other_seller_list))

    return private_seller_avg, dealer_seller_avg, other_seller_avg

# Write list data to CSV file
def writeListToCSV(fileName, list_to_be_written):

    with open(fileName, 'w') as csvfile:
        fwriter = csv.writer(csvfile)
        for x in list_to_be_written:
            fwriter.writerow(x)

# Write average price per seller type to CSV file
def writeAvgToFile(private_data, dealer_data, other_data):

    column = ("Seller Type","Average")
    private_avg = ("private","€"+str(private_data)+",-")
    dealer_avg = ("dealer","€"+str(dealer_data)+",-")
    other_avg = ("other","€"+str(other_data)+",-")
    avg_to_file = []
    avg_to_file.append(column)
    avg_to_file.append(private_avg)
    avg_to_file.append(dealer_avg)
    avg_to_file.append(other_avg)
    writeListToCSV("Report One.csv", avg_to_file)

# Calculate percentage of available cars per make
def percentagePerMake(input_list):

    # Count the frequency of each unique make available cars
    unique_of_makes = {}
    Total_Number = len(input_list)
    for item in input_list:
        make = item[1]
        if make in unique_of_makes:
            unique_of_makes[make] +=1
        else:
            unique_of_makes[make] = 1
# calculate the percentage
    for key, value in unique_of_makes.items():
        value = int((value/Total_Number) * 100)
# Sort in descending order
    unique_of_makes["Make"] = ""
    sortedDict = sortDict(unique_of_makes)
    for key, value in sortedDict.items():
        sortedDict[key] = str(value) + "%"
    return sortedDict

def prepareHeadersForPercentagePerMake():
    dict_to_be_written = {}
    dict_to_be_written["Make"] = "Distribution"
    return dict_to_be_written

 # Write dictionary data to CSV file
def writeDictToFile(fileName, dict_to_be_written):
    file = open(fileName, "w")
    writer = csv.writer(file)
    for key, value in dict_to_be_written.items():
        writer.writerow([key, value])
    file.close()

# Write percentage available of car per each make to file
def writePercentagePerMakeToFile(list_of_percentage):

    writeDictToFile("Report Two.csv", list_of_percentage)

# Function to sort dictionary based on the values in a descending order
def sortDict(dict_to_be_sorted):
    sorted_dict = {}
    i = 0
    for k in dict_to_be_sorted.keys():
        if k == "Make":
            sorted_dict["Make"] = "Distribution"
            del dict_to_be_sorted[k]
            break;
    sorted_values = sorted(dict_to_be_sorted.values(), reverse=True)
    for item in sorted_values:
        if item == "Make":
            continue
        for k in dict_to_be_sorted.keys():
            if dict_to_be_sorted[k] == item:
                sorted_dict[k] = dict_to_be_sorted[k]
                dict_to_be_sorted[k] = 0
                i = i + 1
                break
    return sorted_dict

# Calculate the average price of the thirty percentage most contacted listing
def thirty_percent_most_contacted(listing_input_list, contacts_input_list):

    # Set data structure to get the unique total number of the contacted listing
    total_unique_contacted = set()
    # Calculate the frequency per each unique contacted listing
    contacts_freq = {}
    for item in contacts_input_list:
        # Map between the two files (listing and contacts) based on the id field
        listing = item[0]
        total_unique_contacted.add(listing)
        if listing in contacts_freq:
            contacts_freq[listing] += 1
        else:
            contacts_freq[listing] = 1
            # Sort in descending order
    sorted_dict = sortDict(contacts_freq)
    # Calculate how much does 30% construct from our data
    thirty_percentage_representation = int((len(total_unique_contacted)*30)/100)
    list_of_most_contacted_ids = []
    for i in range(thirty_percentage_representation):
        # Append keys of the 30% most contacted listing into a list
        list_of_most_contacted_ids.append(list(sorted_dict.keys())[i])
    list_of_prices_per_each_id = []
    total = 0
    # Calculate price per each item in the formed list of the top 30% contacted listing
    for id in list_of_most_contacted_ids:
        for search_for_id in listing_input_list:
            if (search_for_id[0] == id):
                list_of_prices_per_each_id.append(search_for_id[2])
                total = total + int(search_for_id[2])
# Calculate the overall average of the calculated prices of the list of keys of the top 30% contacted listing
    avg_of_thirty_percentage_most_contacted = int(total / len(list_of_prices_per_each_id))
    return avg_of_thirty_percentage_most_contacted

# Write the average price of the top 30 contacted listing
def writeTopThirtyAvgToFile(avg):

    list_to_be_written = []
    column = ["Average Price"]
    list_to_be_written.append(column)
    list_to_be_written.append(["€"+str(avg)+",-"])
    writeListToCSV("Report Three.csv",list_to_be_written)

 # Main

listing_input_list = importData("listings.csv")
private_data, dealer_data, other_data = gettingAvgPerSellerType(listing_input_list)
writeAvgToFile(private_data, dealer_data, other_data)
list_of_percentage = percentagePerMake(listing_input_list)
writePercentagePerMakeToFile(list_of_percentage)

contacts_input_list = importData("contacts.csv")
avg_of_thirty_percentage_most_contacted = thirty_percent_most_contacted(listing_input_list, contacts_input_list)
writeTopThirtyAvgToFile(avg_of_thirty_percentage_most_contacted)


