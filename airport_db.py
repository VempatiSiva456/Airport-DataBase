import datetime
import subprocess as sp
import pymysql
import pymysql.cursors
import sys
from tabulate import tabulate

colors_dict_1 = {
    "BLUE": "\033[1;34m",
    "RED": "\033[1;31m",
    "CYAN": "\033[1;36m",
    "GREEN": "\033[0;32m",
    "RESET": "\033[0;0m",
    "BOLD": "\033[;1m",
    "REVERSE": "\033[;7m",
    "ERROR":"\033[;7m"+"\033[1;31m"
}

def offload_commit(con):
    #con.commit()
    return

def debug_print(msg):
    decorate_output("REVERSE")
    #print(msg)
    decorate_output("RESET")

def error_print(msg):
    decorate_output("RED")
    print(msg)
    decorate_output("RESET")
    
def add_yes_print():
    decorate_output("GREEN")
    print("Insertion successful")
    decorate_output("RESET")

def success_print(msg):
    decorate_output("GREEN")
    print(msg)
    decorate_output("RESET")
    
def decorate_output(color_str):
    #print("Decorated")
    sys.stdout.write(colors_dict_1[color_str])

def part():
    print("-----------------------------------------------------------------")
    return


def part2():
    print("=====================================================================")
    return

def part3():
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return

def date_less_cur(date_str):
    today_date = datetime.date.today()
    today_date_str = today_date.strftime("%Y-%m-%d")

    if date_str < today_date_str:
        return 1
    else:
        return 0

def date_more_cur(date_str):
    today_date = datetime.date.today()
    today_date_str = today_date.strftime("%Y-%m-%d")

    if date_str > today_date_str:
        return 1
    else:
        return 0

def numeric_check(ch):
    
    if ch>='0' and ch<='9':
        return 1
    else:
        return 0

def dep_ahead_arv(arrival_str, depart_str):
    if len(arrival_str)!=5 or len(depart_str)!=5:
        error_print('Invalid format')
        return -1
    
    if numeric_check(arrival_str[0])+numeric_check(arrival_str[1])+numeric_check(arrival_str[3])+numeric_check(arrival_str[4])!=4:
        error_print("Error: Enter only digits for mm and hh in arrival time")
        return -1
    
    if numeric_check(depart_str[0])+numeric_check(depart_str[1])+numeric_check(depart_str[3])+numeric_check(depart_str[4])!=4:
        error_print("Error: Enter only digits for mm and hh in departure time")
        return -1

    arrival_hrs = int(arrival_str[0:2])
    arrival_min = int(arrival_str[3:5])
    depart_hrs = int(depart_str[0:2])
    depart_min = int(depart_str[3:5])

    
    if depart_hrs > arrival_hrs:
        error_print('Arrival time can not be ahead of departure time')
        return -1
    
    elif depart_hrs == arrival_hrs and depart_min > arrival_min:
        error_print('Arrival time can not be ahead of departure time')
        return -1
    
    else:
        return 0

def is_valid_time_zone(time_str):
    # +05:30
    if len(time_str)!=6:
        error_print("Invalid format")
        return -1

    if numeric_check(time_str[1])+numeric_check(time_str[2])+numeric_check(time_str[4])+numeric_check(time_str[5])!=4:
        error_print("Enter only digits for mm and hh")
        return -1

    hrs=int(time_str[1:3])
    mins=int(time_str[4:6])

    if (time_str[0]!='+' and time_str[0]!='-') or time_str[3]!=':':
        error_print("Invalid format")
        return -1

    if hrs>12:
        error_print("hrs not valid")
        return -1
    if mins>60:
        error_print("mins not valid")
        return -1
    
    return 0

def print_err_date(state):
    if state == 1:
        print('The date entered cannot be after current date. Current date: ' + str(datetime.date.today()))
    elif state == -1:
        print('The date entered cannot be before current date. Current date: ' + str(datetime.date.today()))

def get_query_atoms(attr):
    keys_str = ""
    values_str = ""
    dict_len = len(attr.keys())
    i = -1

    for key, value in attr.items():

        i += 1
        if value == '' or value == 'NULL':
            continue

        keys_str += "`"+key+"`"
        values_str += '"'+value+'" '

        if i != dict_len-1:
            keys_str += ", "
            values_str += ", "
    
    if keys_str[-2]==',':
        keys_str=keys_str[:-2]

    if values_str[-2]==',':
        values_str=values_str[:-2]

    return (keys_str, values_str)

############################################################################################
# Done-------------
def add_airline(cur, con):
    #print("inside add_airline function")
    table_Name = "`Airline`"

    attr = {}
    print('Enter details of the new airline:')

    attr['IATA_Airline_Code'] = input('Enter 2-character IATA airline designator code * :')

    attr['Company_Name'] = input('Enter airline Name * : ')

    attr['Number_of_aircrafts_owned'] = input('Enter number of aircrafts currently owned by the airline: ')

    tmp = input('Enter 1 if airline is active, 0 otherwise: ')

    if tmp == 1:
        attr['Active'] = True
    elif tmp == 0:
        attr['Active'] = False
        

    attr['Country_of_Ownership'] = input('Enter country of ownership of airline: ')

    keys_str, values_str = get_query_atoms(attr)

    # print('Table Name:' + keys_str)
    #print(values_str)

    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"


    try:
        cur.execute(query_str)
        add_yes_print()
        con.commit()

    except Exception as e:
        print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return

################################################################################################

# done ---------- CHECKED
def add_aircraft(cur, con):
    debug_print("inside add_aircraft function")
    table_Name = "`Aircraft`"

    attr = {}
    print('Enter details of the new aircraft: ')

    attr['Registration_No.'] = input("Enter registration number of aircraft: ")
    attr['Manufacturer'] = input("Enter manufacturer of aircraft: ")
    attr['Plane_Model'] = input("Enter model of aircraft: ")
    attr['Distance_Travelled'] = input("Enter Distance_Travelled: ")
    attr['Flight_ID'] = input("Enter Flight_ID: ")
    attr['Last_Maintanence_Check_Date'] = input("Enter Last_Maintanence_Check_Date: [YYYY-MM-DD]: ")

    if date_more_cur(attr['Last_Maintanence_Check_Date']) == 1:
        print_err_date(1)
        con.rollback()
        return
    attr['Owners_IATA_Airline_Code'] = input("Enter IATA code of owner airline: ")

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"


    try:
        cur.execute(query_str)
        add_yes_print()
        #con.commit()

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return
    
    query_str2 = 'UPDATE Airline, Aircraft SET Number_of_aircrafts_owned = Number_of_aircrafts_owned - 1 WHERE Aircraft.Owners_IATA_Airline_Code = Airline.IATA_Airline_Code'
    try:
        cur.execute(query_str2)
        con.commit()

    except Exception as e:
        error_print('Failed to increment number of aricrafts owned by airline the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return

#####################################################################################
# done -> CHECKED
def add_Emergency_Contact(cur, con, aadhar_relative):

    #print("inside Emergency_Contact_func")
    table_Name = "`Emergency_Contact`"

    attr = {}
    print('Enter details of the emergency contact entry:')
    attr['Aadhar_card_number'] = aadhar_relative
    attr["Name"] = input('Name*: ')

    attr['Phone_No'] = input('Phone_No: ')

    keys_str, values_str = get_query_atoms(attr)
    print(keys_str)
    print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("Emergency contact added")
        return 0

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

# done #checked
def add_passenger(cur, con):
    #print("inside add_passenger function")
    table_Name = "`Passenger`"

    attr = {}
    print('Enter details of the new passenger: ')

    attr["Aadhar_card_number"] = input("Enter aadhar card number 12 digit number: ")

    tmp_Name = input("Enter Name: ")

    Name_list = tmp_Name.split(' ')   

    if len(Name_list) >= 3:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ' '.join(Name_list[1:-1])
        attr['Last_Name'] = Name_list[-1]
    elif len(Name_list) == 2:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ''
        attr['Last_Name'] = Name_list[1]
    elif len(Name_list) == 1:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ''
        attr['Last_Name'] = ''
    else:
        print('Error: Incorrect format of Name entered')
        input('Press any key to continue.')
        return

    attr["DOB"] = input("Enter Date of birth in format YYYY-MM-DD: ")
    if date_more_cur(attr['DOB']) == 1:
        print_err_date(1)
        con.rollback()
        return
    
    year = int(attr["DOB"][0:4])
    if 2020-year>60:
        attr["Senior_Citizen"] ="1"
    else:
        attr["Senior_Citizen"] = "0"
        

    attr["Gender"] = int(input("Enter \n1 for Male \n2 for  Female \n3 for Others\n"))

    if attr['Gender'] == 1:
        attr['Gender'] = 'Male'
    elif attr['Gender'] == 2:
        attr['Gender'] = 'Female'
    elif attr['Gender'] == 3:
        attr['Gender'] = 'Others'
    else:
        print("Invalid number inserted. Please try again")
        con.rollback()
        return

    attr["House_Number"] = input("Enter House_Number of residence: ")
    attr["Building"] = input("Enter building number of residence: ")
    attr["City"] = input("Enter city of residence: ")
    attr["Email-ID"] = input("Enter email-ID: ")
    # attr["Senior_Citizen"] = input(
    #     "Enter 0. non Senior_Citizen\n 1. Senior_Citizen\n")
    attr["Nationality"] = input("Enter nationality of passenger eg.Indian: ")



    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"


    try:
        cur.execute(query_str)
        offload_commit(con)
        num_Emergency_Contacts = int(input("Enter number of emergency contacts you want to add between 0 and 3: "))
        if num_Emergency_Contacts > 3:
            error_print("ERROR: Only upto 3 contacts allowed")
            return
        else:
            for i in range(num_Emergency_Contacts):
                if add_Emergency_Contact(cur, con, attr["Aadhar_card_number"]) == -1:
                    return
        con.commit()
        add_yes_print()

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        error_print(e)
        input('Press any key to continue.')
        return

##############################################################################################
# Done checked
def add_airport(cur, con):
    #print("inside add_airport function")
    table_Name = "`Airport`"

    attr = {}
    print('Enter details of the new airport: ')

    attr["IATA_CODE"] = input(" Enter 3 character IATA code *: ")
    attr["Manager"] = input("Enter Airport's Manager Name :")

    ######################################################
    attr["Time_Zone"] = input(" Enter in +hh:mm or -hh:mm format , note mm has to be between 0 and 60 and divisible by 15, hh between 0 and 12: ")
    if is_valid_time_zone(attr["Time_Zone"])==-1:
        error_print("error in Time_Zone entered by user")
        return
    ########################################################
    
    attr["Name"] = input("Enter Name of airport: ")
    attr["City"] = input("Enter city where airport is situated: ")
    attr["Country"] = input("Enter country where airport is situated: ")

    attr["Latitude"] = input("Enter latitude: ")
    if float(attr['Latitude']) > 90 or float(attr['Latitude']) < -90:
        error_print("ERROR : Invalid latitudes")
        return

    attr["Longitude"] = input("Enter longitude: ")
    if float(attr['Longitude']) > 180 or float(attr['Longitude']) < -180:
        error_print("ERROR : Invalid longitudes")
        return

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    # print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"


    try:
        cur.execute(query_str)
        add_yes_print()
        con.commit()

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        error_print(e)
        input('Press any key to continue.')
        return

##########################################################################################
# Done
def add_runway(cur, con):
    debug_print("inside add_runway function")
    table_Name = "`Runway`"

    attr = {}
    print('Enter details of the new runway: ')

    attr["IATA_CODE"] = input(
        "Enter IATA airport code of corresponding airport: ")
    attr["Runway_ID"] = input("Enter Runway_ID: ")
    attr["Length"] = input("Enter length in feet: ")
    attr["Width"] = input("Enter width in feet: ")

    ################DISPLAY A MENU HERE########################################
    stat_choice = int(input("Enter status 1. Assigned\n 2. available\n 3. Disfunctional\n"))

    attr["Status"] = ""
    if stat_choice == 1:
        attr["Status"] = 'Assigned'
    elif stat_choice == 2:
        attr["Status"] = 'Available'
    elif stat_choice == 3:
        attr["Status"] = 'Disfunctional'

    ######################################################

    keys_str, values_str = get_query_atoms(attr)
    # print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"


    try:
        cur.execute(query_str)
        add_yes_print()
        con.commit()

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return


# Done
def add_terminal(cur, con):
    #print("inside add_terminal function")
    table_Name = "`Terminal`"

    attr = {}
    print('Enter details of the new terminal: ')

    attr["IATA_CODE"] = input("Enter IATA code of corresponding airport: ")
    attr["Termina_ID"] = input("Enter Termina_ID: ")
    attr["Flight_Handling_capacity"] = input("Enter Flight_Handling_capacity: ")
    attr["Floor_Area"] = input("Enter Floor_Area: ")

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"


    try:
        cur.execute(query_str)
        add_yes_print()
        con.commit()

    except Exception as e:
        error_print('Failed to insert Terminal into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return

###################################################################################################
# Done
def add_stopover_airports(cur,con,route_id):
    #print("inside stopover_airports function")
    table_Name = "`Stopover_Airports_of_Route`"

    attr = {}
    print('Enter details of the new stopover airport: ')

    attr['Route_ID'] = route_id
    attr['Stopover_Airport_IATA_CODE'] = input("Enter iata code of stopover airport: ")


    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("in stopover query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        print("Stopover executed")
        #add_yes_print()
        return 0


    except Exception as e:
        error_print('Failed to insert Stopover airport into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1


def add_Flight_Crew_SERVES_ON_THE_Route(cur,con,route_id,aadhar_num):
    
    debug_print("inside Flight_Crew_SERVES_ON_THE_Route")
    table_Name = "`Flight_Crew_SERVES_ON_THE_Route`"

    attr = {}
    #print('Enter details of the new runway: ')

    attr["Route_ID"] = route_id
    attr["Aadhar_card_number"]=aadhar_num


    keys_str, values_str = get_query_atoms(attr)
    # print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        #add_yes_print()
        return 0
        
    except Exception as e:
        error_print('Failed to insert crew member into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

def add_Crew_has_worked_together(cur,con,a1,a2,a3,a4):
    debug_print("INSIDE Crew_has_worked_together")
    table_Name = "`Crew_has_worked_together`"

    attr = {}
    #print('Enter details of the new runway: ')

    attr["Pilot_Captain_Aadhar_card_number"] = a1
    attr["Pilot_First_Officer Aadhar_card_number"] = a2
    attr["Flight_Attendant_Aadhar_card_number"] = a3
    attr["Flight_Engineer_Aadhar_card_number"] = a4

    query_init=f'''SELECT DISTINCT  `Language`
                    FROM `Languages_spoken_by_airline_employee`
                    WHERE (`Aadhar_card_number`={a1})
                    OR(`Aadhar_card_number`={a2})
                    OR(`Aadhar_card_number`={a3})
                    OR(`Aadhar_card_number`={a4})
                    '''
    
    cur.execute(query_init)    
    result = cur.fetchall()
    #print("Result len is {result}")
    attr["Number_of_Languages_spoken_overall"]=str(len(result))

    keys_str, values_str = get_query_atoms(attr)
    # print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        #add_yes_print()
        return 0
        
    except Exception as e:
        error_print('Failed to insert TEAM INTO DATABASES.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

def add_route(cur, con):

    # print("inside add_Route function")
    table_Name = "`Route`"

    attr = {}
    print('Enter details of the new route: ')

    attr['Route_ID'] = input('Route_ID: ')
    attr['Source_IATA_CODE'] = input('source airport iata code: ')
    attr['Destination_IATA_CODE'] = input('Destination airport iata code: ')

    if attr['Source_IATA_CODE'] == attr['Destination_IATA_CODE']:
        error_print('source airport iata code can not be same as destination iata code')
        return

    #################################################
    attr['Date'] = input('Date: [YYYY-MM-DD] (Press enter for today\'s date): ')

    if attr['Date'] == '':
        attr['Date'] = datetime.date.today().strftime('%Y-%m-%d')
    ###################################################

    if date_less_cur(attr['Date']) == 1:
        print_err_date(-1)
        con.rollback()
        return
    ###########################################
    #job 2
    attr['Scheduled_Arrival'] = input('Scheduled_Arrival (Press enter if information not available): [HH:MM]: ')
    attr['Scheduled_Departure'] = input('Scheduled_Departure: [HH:MM] (Press enter if information not available): ')
    if attr['Scheduled_Arrival']!='' and attr['Scheduled_Departure']!='':
        if dep_ahead_arv(attr['Scheduled_Arrival'], attr['Scheduled_Departure']) == -1:
            return
    ############################################################################
    error_print("Press enter if information for an attribute is not available")
    attr['Time_duration'] = input('Time_duration [HH:MM]: ')
    attr['Take_off_runway_id'] = input('Take off Runway_ID: ')
    attr['Distance_Travelled'] = input('Distance_Travelled: ')
    attr['Landing_RunWay_ID'] = input('Landing Runway_ID: ')
    attr['Registration_No.'] = input('aircraft registration number: ')
    attr['Status'] = input('Current_Status: [Departed, Boarding, On_route, Delayed, Arrived, Check-in, Not_applicable]: ')


      

    #print(keys_str)
    #print(values_str)
    

    #print("query str is %s->", query_str)
    attr['Pilot_Captain_Aadhar_card_number'] = input('Enter Pilot captain\'s Aadhar card number: ')
    attr['Chief_Flight_Attendant_Aadhar_card_number'] = input('Enter Chief flight attendant\'s Aadhar card number: ')

    keys_str, values_str = get_query_atoms(attr)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"


    try:
        cur.execute(query_str)
        offload_commit(con)
        add_yes_print()
        ######################################################################
        num_stopover = int(input('Enter number of stopover airports encountered in the route: '))
        for i in range(num_stopover):
            if add_stopover_airports(cur,con,attr['Route_ID'])==-1:
                return
        ####################################################################
        # ADD CREW

        # Take Captain input
        
        if add_Flight_Crew_SERVES_ON_THE_Route(cur,con,attr['Route_ID'],attr['Pilot_Captain_Aadhar_card_number'] )==-1:
                return

        # Take chief flight attendant input
        if add_Flight_Crew_SERVES_ON_THE_Route(cur,con,attr['Route_ID'],attr['Chief_Flight_Attendant_Aadhar_card_number'])==-1:
                return

        # Take first officer input
        aadhar_first_officer = input('Enter First Officer\'s Aadhar card number: ')
        if add_Flight_Crew_SERVES_ON_THE_Route(cur,con,attr['Route_ID'],aadhar_first_officer)==-1:
                return
        
        # Take Flight engineer input
        aadhar_engineer = input('Enter Flight Engineer\'s Aadhar card number: ')
        if add_Flight_Crew_SERVES_ON_THE_Route(cur,con,attr['Route_ID'],aadhar_engineer)==-1:
                return


        num_hostess=int(input("Enter number of non-chief flight attendants: "))
        for i in range(num_hostess):
            aadhar_to_add=input("Input aadhar of non-chief flight attendant: ")
            if add_Flight_Crew_SERVES_ON_THE_Route(cur,con,attr['Route_ID'],aadhar_to_add)==-1:
                return

        if add_Crew_has_worked_together(cur,con,attr['Pilot_Captain_Aadhar_card_number'],aadhar_first_officer,
            attr['Chief_Flight_Attendant_Aadhar_card_number'],aadhar_engineer)==-1:
            return
        con.commit()
    ###################################################################
    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return

#################################################################################################
# Done
def add_pnr_info_deduction(cur, con, pnr_of_Boarding_Pass):
    table_Name = "`PNR_Info_Deduction`"

    attr = {}
    #print('Enter details of the PNR_Info_Deduction: ')

    #########################################################################################
    attr["PNR_Number"] = pnr_of_Boarding_Pass
    attr["Route_ID"] = input("Enter Route_ID: ")
    attr["Scheduled_Boarding_Time"] = input("Enter schdeuled boarding time allotted to you based \
            on your seat, class of traveletc.: ")
    attr["class_of_travel"] = input("Enter Travel class business/economy: ")
    attr["Source_IATA_CODE"] = input("Enter source airport IATA code: ")

    ########################################################################
    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)       
        return 0

    except Exception as e:
        print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

# Done
def add_Boarding_Pass_Special_Services(cur, con, barcode_number, special_service_to_add):
    #print("inside Boarding_Pass_Special_Services")
    table_Name = "`Boarding_Pass_Special_Services`"

    attr = {}
    #print('Enter details of the new Boarding_Pass_Special_Services: ')

    attr["Barcode_No."] = barcode_number
    attr["Special_Services"] = special_service_to_add

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    # print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("Boarding_Pass_Special_Services inserted")
        return 0

    except Exception as e:
        print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

# done
def add_Luggage(cur, con, barcode_number):
    #print("inside Luggage")
    table_Name = "`Luggage`"

    attr = {}
    #print('Enter details of the new Luggage:')

    attr["Baggage_ID"] = input("Enter Baggage_ID")
    attr["Barcode_No."] = barcode_number

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"


    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("Luggage inserted")
        return 0

    except Exception as e:
        print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

# Done
def add_Boarding_Pass_details(cur, con):
    # print("inside add_boarding pass function")
    table_Name = "`Boarding_Pass`"

    attr = {}
    print('Enter details of the Boarding pass entry: ')

    attr["Barcode_No."] = input("Enter 12 char boarding pass Barcode_No.: ")
    attr["PNR_Number"] = input("Enter PNR number to which boarding pass belongs: ")
    attr["Seat"] = input("Enter seat: ")
    attr["Aadhar_card_number"] = input("Enter 12 digit Aadhar Card Number: ")

    keys_str, values_str = get_query_atoms(attr)
    print(keys_str)
    print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"


    try:
        cur.execute(query_str)
        offload_commit(con)
        add_yes_print()
        #############################################################################################
        num_Luggages = int(input("Enter number of Luggages you want to link to this boarding pass: "))
        for i in range(num_Luggages):
            if add_Luggage(cur, con, attr["Barcode_No."]) == -1:
                return

        ##########################################################################################
        add_more_details = int(input('''
        Press 1 if you want to add additional details like class_of_travel, Src airport etc.,
        \n
        Press 0 if you have already added these details for another boarding pass on the same PNR'''))

        if add_more_details == 1:
            if add_pnr_info_deduction(cur, con, attr["PNR_Number"]) == -1:
                return

        #########################################################################################
        #############################################################################################
        print("List of available Special_Services that can be added are \nA. Wheelchair \nB. Disability Assistance \nC. XL seats \nD. Priority Boarding\n")
        ss_dict = {
            "A": "Wheelchair",
            "B": "Disability Assistance",
            "C": "XL seats",
            "D": "Priority Boarding"
        }
        ss_str = input("Enter Special_Services\nEg: enter AC for Wheelchair and XL seats: ")
        for i in range(len(ss_str)):
            add_ss = ss_dict[ss_str[i]]
            if add_Boarding_Pass_Special_Services(cur, con, attr["Barcode_No."], add_ss) == -1:
                return

        ##########################################################################################
        con.commit()

    except Exception as e:
        print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return

#######################################################################################
#done
def add_On_Ground_emp(cur, con, aadhar_num):

    debug_print("inside add_On_Ground_emp")
    table_Name = "`On_Ground`"

    attr = {}
    print('Enter details of the add_On_Ground_emp: ')
    attr['Aadhar_card_number'] = aadhar_num
    attr['Job_title'] = input("Job_title: ")

    keys_str, values_str = get_query_atoms(attr)
    # print(keys_str)
    # print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("On_Ground employee inserted")
        return 0

    except Exception as e:
        print('Failed to insert into the database.')
        con.rollback()
        error_print(e)
        input('Press any key to continue.')
        return -1

#done
def add_pilot(cur, con, aadhar_num):

    debug_print("inside Pilot")
    table_Name = "`Pilot`"

    attr = {}
    print('Enter details of the Pilot: ')
    attr['Aadhar_card_number'] = aadhar_num
    attr["Pilot_license_number"] = input("Enter Pilot_license_number: ")
    attr["Number_of_flying_hours"] = input("Enter Number_of_flying_hours: ")

    #########################################################################
    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    # print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("added pilot")
        return 0

    except Exception as e:
        print('Failed to insert into the database.')
        con.rollback()
        error_print(e)
        input('Press any key to continue.')
        return -1

#done
def add_Flight_Attendant(cur, con, aadhar_num):

    debug_print("inside Flight_Attendant")
    table_Name = "`Flight_Attendant`"

    attr = {}
    print('Enter details of the Flight_Attendant: ')
    attr['Aadhar_card_number'] = aadhar_num
    attr["Training/Education"] = input("Enter Training: ")

    #########################################################################
    keys_str, values_str = get_query_atoms(attr)
    # print(keys_str)
    # print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    # print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("Filght Attendant has been inserted")
        return 0

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        error_print(e)
        input('Press any key to continue.')
        return -1

# Done
def add_Flight_Engineer(cur, con, aadhar_num):

    debug_print("inside Flight_Engineer")
    table_Name = "`Flight_Engineer`"

    attr = {}
    print('Enter details of the Flight_Engineer: ')
    attr['Aadhar_card_number'] = aadhar_num
    attr["Education"] = input("Enter Education: ")
    attr["Manufacturer"] = input("Enter manufacturer of plane he specializes in: ")
    attr["Plane_Model_No."] = input("Enter model of plane he specializes in: ")

    #########################################################################
    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("Flight engineer added")
        return 0

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

# Done
def add_Flight_Crew(cur, con, aadhar_num):

    debug_print("inside Flight_Crew")
    table_Name = "`Flight_Crew`"

    attr = {}
    print('Enter details of the Flight_Crew:')
    attr['Aadhar_card_number'] = aadhar_num
    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("Flight crew added")
        
        print('''
        Press 1 to add pilot
        \n
        Press 2 to add flight attendant
        \n
        Press 3 to add flight engineer''')
        emp_class = int(input())

        if emp_class == 1:
            if add_pilot(cur, con, attr["Aadhar_card_number"]) == -1:
                return -1
        elif emp_class == 2:
            if add_Flight_Attendant(cur, con, attr["Aadhar_card_number"]) == -1:
                return -1
        else:
            if add_Flight_Engineer(cur, con, attr["Aadhar_card_number"]) == -1:
                return -1

    #########################################################################

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

    #########################################################################



#done
def add_language(cur, con, aadhar_num):
    debug_print("inside Languages_spoken_by_airline_employee")
    table_Name = "`Languages_spoken_by_airline_employee`"

    attr = {}
    attr["Aadhar_card_number"] = aadhar_num
    attr["Language"] = input('Enter Name of language to be added:')

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("Language has been added")
        return 0

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        error_print(e)
        input('Press any key to continue.')
        return -1

#done
def add_Airline_Employees_CREW(cur, con):

    debug_print("inside Airline_Employees/CREW")
    table_Name = "`Airline_Employees/CREW`"

    attr = {}
    print('Enter details of the Airline_Employees/CREW entry:')

    attr["Aadhar_card_number"] = input("Aadhar_card_number: ")

    tmp_Name = input("Enter Name: ")
    ################################################################
    Name_list = tmp_Name.split(' ')

    if len(Name_list) >= 3:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ' '.join(Name_list[1:-1])
        attr['Last_Name'] = Name_list[-1]
    elif len(Name_list) == 2:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ''
        attr['Last_Name'] = Name_list[1]
    elif len(Name_list) == 1:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ''
        attr['Last_Name'] = ''
    else:
        print('Error: Incorrect format of Name entered')
        input('Press any key to continue.')
        return
    ##############################################################
    
    attr["Joining_Date"] = input("Joining Date: [YYYY-MM-DD]: ")
    if date_more_cur(attr['Joining_Date']) == 1:
        print_err_date(1)
        con.rollback()
        return
    attr["Salary"] = input("Salary: ")
    attr["Nationality"] = input("Nationality: ")
    
    ######################################################################
    attr["DOB"] = input("DOB: [YYYY-MM-DD]: ")
    if date_more_cur(attr['DOB']) == 1:
        print_err_date(1)
        con.rollback()
        return
    ################################################################
    attr["Gender"] = input("Gender: [Male, Female, Others]: ")
    attr["Employer_IATA_Airline_Code"] = input("Airline employer IATA code: ")
    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        add_yes_print()
        num_lang = int(input('Enter Number of languages spoken by the employee: '))
        for i in range(num_lang):
            if add_language(cur, con, attr['Aadhar_card_number']) == -1:
                return

        #############################################################################
        print('''
        Press 1 if employee is part of FLIGHT CREW
        \n
        Press 2 if employee is part of On_Ground team''')

        emp_class = int(input())

        if emp_class == 2:
            if add_On_Ground_emp(cur, con, attr["Aadhar_card_number"]) == -1:
                return
        else:
            if add_Flight_Crew(cur, con, attr["Aadhar_card_number"]) == -1:
                return
       
        con.commit()

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        error_print(e)
        input('Press any key to continue.')
        return


    #########################################################################


#########################################################################################################
#Done
def add_Air_Traffic_Controller(cur, con, aadhar_num):

    debug_print("inside Air_Traffic_Controller")
    table_Name = "`Air_Traffic_Controller`"

    attr = {}
    print('Enter details of the Air_Traffic_Controller: ')
    attr['Aadhar_card_number'] = aadhar_num
    attr['Current_communication_Frequency'] = input("Current_communication_Frequency: ")
    attr['Training/Education'] = input("Training/Education: ")

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("ATC ADDED")
        return 0

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

#Done
def add_Management_and_operations_executives(cur, con, aadhar_num):

    debug_print("inside Management_and_operations_executives")
    table_Name = "`Management_and_operations_executives`"

    attr = {}
    print('Enter details of the Management_and_operations_executives: ')
    attr['Aadhar_card_number'] = aadhar_num
    attr['Job_title'] = input("Job_title: ")

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("Management_and_operations_executives added")
        return 0

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

# Done
def add_security(cur, con, aadhar_num):

    debug_print("inside security")
    table_Name = "`Security`"

    attr = {}
    print('Enter details of the security: ')
    attr['Aadhar_card_number'] = aadhar_num
    attr['Designation'] = input("Designation: ")
    attr['Security_ID_Number'] = input("Security_ID_Number: ")

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        offload_commit(con)
        success_print("Security inserted")
        return 0

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return -1

# Done
def add_airport_crew(cur, con):

    debug_print("inside airport_crew")
    table_Name = "`Airport_Employees/CREWS`"

    attr = {}
    print('Enter details of the airport_crew entry: ')

    attr["Aadhar_card_number"] = input("Aadhar card number: ")

    tmp_Name = input("Enter Name: ")

    Name_list = tmp_Name.split(' ')

    if len(Name_list) >= 3:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ' '.join(Name_list[1:-1])
        attr['Last_Name'] = Name_list[-1]
    elif len(Name_list) == 2:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ''
        attr['Last_Name'] = Name_list[1]
    elif len(Name_list) == 1:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ''
        attr['Last_Name'] = ''
    else:
        print('Error: Incorrect format of Name entered')
        input('Press any key to continue.')
        return

    attr["Experience"] = input("Experience: ")
    attr["Salary"] = input("Salary: ")
    attr["Nationality"] = input("Nationality: ")

    ####################################################################
    attr["DOB"] = input("DOB: [YYYY-MM-DD]: ")
    if date_more_cur(attr['DOB']) == 1:
        print_err_date(1)
        con.rollback()
        return
    #############################################################
    attr["Gender"] = input("Gender")
    attr["Working_Airport_IATA_CODE"] = input("airport IATA code of employing airport")
    attr["Supervisor_Aadhar_card_number"] = input("Supervisior's Aadhar card number:")

    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    #print("query str is %s->", query_str)
    try:
        cur.execute(query_str)
        offload_commit(con)
        add_yes_print()
        #############################################################################
        print('''
        Press 1 if employee is Air traffic controller
        \n
        Press 2 if employee is part of Management
        \n
        Press 3 if employee is part of Security''')

        emp_class = int(input())

        if emp_class == 1:
            if add_Air_Traffic_Controller(cur, con, attr["Aadhar_card_number"]) == -1:
                return
        elif emp_class == 2:
            if add_Management_and_operations_executives(cur, con, attr["Aadhar_card_number"]) == -1:
                return
        else:
            if add_security(cur, con, attr["Aadhar_card_number"]) == -1:
                return

        #########################################################################
        con.commit()

    except Exception as e:
        error_print('Failed to insert into the database.')
        con.rollback()
        print(e)
        input('Press any key to continue.')
        return

def add_feedback(cur, con):

    debug_print("inside Pilot")
    table_Name = "`Flight_Crew_feedback`"

    attr = {}
    print('Enter details of the feedback: ')
    attr["Pilot_Captain_Aadhar_card_number"] = input("Enter concerned Captain's Pilot aadhar number: ")
    attr["Pilot_First_Officer Aadhar_card_number"] = input("Enter concerned First Officer aadhar number: ")
    attr["Flight_Attendant_Aadhar_card_number"] = input("Enter concerned Flight attendant aadhar number: ")
    attr["Flight_Engineer_Aadhar_card_number"] = input("Enter concerned Flight engineer's aadhar number: ")
    attr["Feedback_given_by_the_passengers_for_the_crew"] = input("Enter single line feedback: ")

    #########################################################################
    keys_str, values_str = get_query_atoms(attr)
    #print(keys_str)
    #print(values_str)
    query_str = 'INSERT INTO '+table_Name + \
        " ( "+keys_str+" ) VALUES"+" ( "+values_str+" );"

    # print("query str is %s->", query_str)

    try:
        cur.execute(query_str)
        con.commit()
        success_print("added Feedback")
        return 0

    except Exception as e:
        print('Failed to insert into the database.')
        con.rollback()
        error_print(e)
        input('Press any key to continue.')
        return -1
    
########################################################################################################################################################################################################
########################################################################################################################################################################################################
    

colors_dict3 = {
    "BLUE": "\033[1;34m",
    "RED": "\033[1;31m",
    "CYAN": "\033[1;36m",
    "GREEN": "\033[0;32m",
    "RESET": "\033[0;0m",
    "BOLD": "\033[;1m",
    "REVERSE": "\033[;7m",
    "ERROR": "\033[;7m"+"\033[1;31m"
}


def decorate3(color_str):
    # print("Decorated")
    sys.stdout.write(colors_dict3[color_str])

def del_print(msg):
    decorate3("GREEN")
    print(msg)
    decorate3("RESET")

def err_print_msg(msg):
    decorate3("ERROR")
    print(msg)
    decorate3("RESET")

def get_deletion_equation(attr,key_attrs,type_str):
    
    query_str = ""
    dict_len = len(attr.keys())

    for i in range(dict_len):

        #i += 1
        if attr[key_attrs[i]] == '':
            return ""

        query_str += "`"+key_attrs[i]+"`"+" = "

        if type_str[i]=='1':
            query_str+'''"'''
        query_str +="'" +attr[key_attrs[i]]+"'"
        if type_str[i]=='1':
            query_str+'''"'''

        if i != dict_len-1:
            query_str+" AND "

    return query_str

# DONE
def delete_aircraft(cur,con):
    #print("Inside delete_aircraft func")
    table_Name="Aircraft"

    attr={}

    key_attrs=["Registration_No."]

    attr[key_attrs[0]]=input("Enter reg num of aircraft you wish to delete: ")



    try:
        ans=get_deletion_equation(attr,key_attrs,"0") # non-int - pass 1 else pass 0
        if ans=="":
            print("Key attribute value cannot be left empty")
            print("Failed to delete from database")
            input("Press any key to continue")
            return
        query_str = "DELETE FROM "+table_Name+" WHERE "+ans+" ; "
        cur.execute(query_str)
        con.commit()
        res_cnt=cur.rowcount
        if res_cnt == 0:
            del_print("No such aircraft exists")
        ############################################
        else:
            del_print("Deleted aircraft")
        ###########################################


        input("Press any key to continue")

    except Exception as e:
        con.rollback()
        err_print_msg("Failed to delete from database")
        err_print_msg(">>>>>>>>>>>>>", e)
        input("Press any key to continue")
        return

    query_str2 = 'UPDATE Airline, Aircraft SET Number_of_aircrafts_owned = Number_of_aircrafts_owned - 1 WHERE Owners_IATA_Airline_Code = `IATA_Airline_Code`'
    try:
        cur.execute(query_str2)
        con.commit()

    except Exception as e:
        err_print_msg('Failed to decrement number of aricrafts owned by airline the database.')
        con.rollback()
        err_print_msg(e)
        input('Press any key to continue.')
        return

# Done
def delete_Luggage(cur,con):
    #print("Inside delete_Luggage func")
    table_Name="Luggage" 

    attr={}

    key_attrs=["Baggage_ID"]

    attr[key_attrs[0]]=input("Enter Baggage_ID of Luggage you wish to delete: ")



    try:
        ans=get_deletion_equation(attr,key_attrs,"0") # non-int - pass 1 else pass 0
        if ans=="":
            print("Key attribute value cannot be left empty")
            print("Failed to delete from database")
            input("Press any key to continue")
            return
        query_str = "DELETE FROM "+table_Name+" WHERE "+ans+" ; "
        cur.execute(query_str)
        con.commit()

        res_cnt=cur.rowcount
        if res_cnt == 0:
            del_print("No such Luggage exists")
        ############################################
        else:
            del_print("Deleted Luggage")
        ###########################################


        input("Press any key to continue")

    except Exception as e:
        con.rollback()
        err_print_msg("Failed to delete from database")
        err_print_msg(">>>>>>>>>>>>>", e)
        input("Press any key to continue")
    return

#done
def delete_Airline_Employees_CREW(cur,con):
    table_Name="Airline_Employees/CREW" 

    attr={}

    key_attrs=["Aadhar_card_number"]

    attr[key_attrs[0]]=input("Enter Aadhar card number of airline employee you wish to delete: ")



    try:
        ans=get_deletion_equation(attr,key_attrs,"0") # non-int - pass 1 else pass 0
        if ans=="":
            print("Key attribute value cannot be left empty")
            print("Failed to delete from database")
            input("Press any key to continue")
            return
        query_str = "DELETE FROM "+table_Name+" WHERE "+ans+" ; "

        cur.execute(query_str)
        con.commit()

        res_cnt=cur.rowcount
        if res_cnt == 0:
            del_print("No such airline employee exists")
        ############################################
        else:
            del_print("Deleted airline employee")
        ###########################################


        input("Press any key to continue")

    except Exception as e:
        con.rollback()
        err_print_msg("Failed to delete from database")
        err_print_msg(">>>>>>>>>>>>>", e)
        input("Press any key to continue")
    return

# DONE
def delete_airport_crew(cur,con):
    #print("Inside delete_airport_crew func")
    table_Name="`Airport_Employees/CREWS`" 

    attr={}

    key_attrs=["Aadhar_card_number"]

    attr[key_attrs[0]]=input("Enter Aadhar card number of airport employee you wish to delete: ")



    try:
        ans=get_deletion_equation(attr,key_attrs,"0") # non-int - pass 1 else pass 0
        if ans=="":
            print("Key attribute value cannot be left empty")
            print("Failed to delete from database")
            input("Press any key to continue")
            return
        query_str = "DELETE FROM "+table_Name+" WHERE "+ans+" ; "

        cur.execute(query_str)
        con.commit()
        res_cnt=cur.rowcount
        if res_cnt == 0:
            del_print("No such airport employee exists")
        ############################################
        else:
            del_print("Deleted airport employee")
        ###########################################


        input("Press any key to continue")

    except Exception as e:
        con.rollback()
        err_print_msg("Failed to delete from database")
        err_print_msg(">>>>>>>>>>>>>", e)
        input("Press any key to continue")
    return
#done
def delete_route(cur,con):
    #print("Inside delete_route func")
    table_Name="Route" 

    attr={}

    key_attrs=["Route_ID"]

    attr[key_attrs[0]]=input("Enter Route_ID of route you wish to delete: ")



    try:
        ans=get_deletion_equation(attr,key_attrs,"0") # non-int - pass 1 else pass 0
        if ans=="":
            print("Key attribute value cannot be left empty")
            print("Failed to delete from database")
            input("Press any key to continue")
            return
        query_str = "DELETE FROM "+table_Name+" WHERE "+ans+" ; "
        cur.execute(query_str)
        con.commit()

        res_cnt=cur.rowcount
        if res_cnt == 0:
            del_print("No such route exists")
        ############################################
        else:
            del_print("Deleted route")
        ###########################################


        input("Press any key to continue")

    except Exception as e:
        con.rollback()
        err_print_msg("Failed to delete from database")
        err_print_msg(">>>>>>>>>>>>>", e)
        input("Press any key to continue")
    return


######################################################################################################################################################################################
######################################################################################################################################################################################


# analysis_funcs_dict = {
#         "1":analysis_passenger_Boarding_Pass_Special_Services,#
#         "2":analysis_big_airlines,#
#         "3":analysis_experienced_pilot,#
#         "4":analysis_search_Name,#
#         "5":analysis_busiest_airports,#
#         "6":analysis_loved_airlines,#
#         "7":analysis_feedback_patterns,
#         "8":analysis_find_tickets,#
#         "9":analysis_crashed_survivors,
#         "10":analysis_airline_pilots,
#         "11":analysis_favoured_aircrafts
# }

# analysis_funcs_msg = {
#         "1":"Names of all passengers who have WHEELCHAIR ASSISTANCE/Disability assisstance as a special service in their BOARDING PASS",#
#         "2":"NameS OF ALL AIRLINES whose flight crew is >=x where 'x' is to be inputted from user",#
#         "3":"find the pilot with maximum number of flying hrs",#
#         "4":"Search for all PASSENGERS whose Name contains a given substring",#
#         "5":"RANK BUSIEST AIRPORTS by number of scheduled flight departures on a particular day",#
#         "6":"RANK most used airline by sorting as per the number of boarding passes issued for that airline since data collection began",
#         "7":"Feedback of flight crew patterns",#
#         "8":"display all flights between two airports on a given date or on any date",
#         "9":"Names of all passengers who were travelling on a particular route/Crashed flight/Flight with a COVID infected patient",
#         "10":"Names of all pilots who work for a given airline",
#         "11":"Find most used aircraft across all airlines"
# }

def display_query_result(cur,con,query):
    try:
        cur.execute(query)
        con.commit()
        result = cur.fetchall()
        
        if len(result) != 0:
            header = result[0].keys()
            rows =  [x.values() for x in result]
            print(tabulate(rows, header, tablefmt = 'psql'))
        
        else:
            print("Alas! -> No rows found!") #length of result is 0

    except Exception as e:
        print(e)
        con.rollback()
        input("Press any key to continue")



# Done
def analysis_passenger_Boarding_Pass_Special_Services(cur,con):
    print("Inside update_passenger func")

    # iata_airport_code=input("Enter iata code of airport ")

    query_str='''SELECT `First_Name`,`Minit`,`Last_Name`,`Passenger`.`Aadhar_card_number` 
                FROM `Boarding_Pass_Special_Services`,`Passenger`,`Boarding_Pass` 
                WHERE (`Special_Services`='Wheelchair' OR  `Special_Services`='Disability Assistance')
                AND (`Boarding_Pass_Special_Services`.`Barcode_No.`=`Boarding_Pass`.`Barcode_No.`)
                AND (`Boarding_Pass`.`Aadhar_card_number`=`Passenger`.`Aadhar_card_number`);
                        '''
    display_query_result(cur, con, query_str)

# CHECKED
def analysis_big_airlines(cur,con):
    #print("Inside analysis_big_airlines")

    
    limit_var=int(input("Enter 'x' in order to display airlines having a total number of employees greater than 'x': "))

    query_str = '''SELECT `IATA_Airline_Code`, `Company_Name`
                FROM `Airline`
                WHERE `IATA_Airline_Code` IN (SELECT `Employer_IATA_Airline_Code`
                            FROM `Airline_Employees/CREW`
                            GROUP BY `Employer_IATA_Airline_Code`
                            HAVING COUNT(*)>={0});'''.format(str(limit_var))
    
    display_query_result(cur,con,query_str)

# CHECKED
def analysis_experienced_pilot(cur,con):
    print("Inside analysis_experienced_pilot func")

    # SELECT LName, FName
    # FROM EMPLOYEE
    # WHERE Salary > ALL ( SELECT Salary
    # FROM EMPLOYEE
    # WHERE Dno = 5 );
    query_str='''SELECT `Pilot_license_number`,`First_Name`,`Last_Name`,`Number_of_flying_hours`,`Employer_IATA_Airline_Code`
                    AS `Employer Airline`
                    FROM   `Pilot`,   `Airline_Employees/CREW`  
                    WHERE (`Pilot`.`Aadhar_card_number`=`Airline_Employees/CREW`.`Aadhar_card_number`) 
                    AND  `Number_of_flying_hours` >= ( SELECT MAX(`Number_of_flying_hours`)
                                                    FROM  `Pilot`);'''

    display_query_result(cur, con, query_str)

#done
def analysis_search_Name(cur,con):
    #print("Inside update_passenger func")

        # % replaces an arbitrary number of zero or more characters, and the underscure (_) replaces a single character. 

    sought_Name=input("Enter substring which needs to be found in Names of the passengers: ")

    query_str='''SELECT `Aadhar_card_number` ,`First_Name`,`Minit`,`Last_Name`
                FROM Passenger
                WHERE (`First_Name` LIKE '%{0}%') OR (`Minit` LIKE '%{0}%') OR (`Last_Name` LIKE '%{0}%');
                        '''.format(sought_Name)
    display_query_result(cur, con, query_str)

#done
def analysis_busiest_airports(cur,con):
    print("Inside busiest_airports func")

    ### SHOULD WE TAKE DATE AS INPUT
    query_str='''SELECT `IATA_CODE`,`Name`,`City`,COUNT(*) AS `Number of Scheduled_Departures`
                FROM `Route`, `Airport`
                WHERE (`IATA_CODE`=`Source_IATA_CODE`)
                GROUP BY `Source_IATA_CODE`  
                ORDER BY COUNT(*)  DESC;
                '''
    display_query_result(cur, con, query_str)

#done
def analysis_loved_airlines(cur,con):
    print("Inside update_passenger func")


    query_str='''SELECT `IATA_Airline_Code`,`Company_Name`,COUNT(*) as    `love_quotient`
                FROM `Airline`,`Aircraft`,`Boarding_Pass`,`Route`
                WHERE (`IATA_Airline_Code`=`Owners_IATA_Airline_Code`) AND (`Aircraft`.`Registration_No.`=`Route`.`Registration_No.`)
                AND(`Boarding_Pass`.`Route_ID`=`Route`.`Route_ID`)
                GROUP BY `IATA_Airline_Code`
                ORDER BY COUNT(*) DESC;
                        '''
    display_query_result(cur, con, query_str)


def analysis_feedback_patterns(cur,con):
    print("You are giving Feedbacks :), No need go back")

    query_str='''
                        '''
#done
def analysis_find_tickets(cur,con):
    #print("Inside analysis_find_tickets func")


    src_iata=input("Enter iata code of src airport (Eg:DEL) : ")
    dest_iata=input("Enter iata code of dest airport (Eg:MUM) : ")

    date_sought=input("Enter date when the journey needs to be made [YYYY-MM-DD] Eg:(2020-10-06): ")

    query_str='''SELECT `Source_IATA_CODE` AS 'Source airport' ,
                        `Destination_IATA_CODE` AS 'Destination Airport',
                        `Date`,
                        `Owners_IATA_Airline_Code` AS 'Airline',
                        `Flight_ID`,
                        `Scheduled_Arrival` 
                FROM `Route`,`Aircraft`
                WHERE (`Source_IATA_CODE`="{0}")
                AND   (`Destination_IATA_CODE`="{1}")
                AND (`Date`="{2}")
                AND   (`Route`.`Registration_No.`=`Route`.`Registration_No.`) 
                                    ;
                        '''.format(src_iata,dest_iata,date_sought)
    #print(f"DEBUG: query is {query_str}")
    display_query_result(cur, con, query_str)    

# DONE
def analysis_crashed_survivors(cur,con):
    print("Inside update_passenger func")

    crashed_route_id=input("Enter Route_ID of the flight whose passengers need to be displayed: ")
    query_str='''SELECT `First_Name`,`Last_Name`, `Boarding_Pass`.`Aadhar_card_number`,`Barcode_No.`,`Seat`
                FROM `Boarding_Pass`,`Passenger`
                WHERE (`Boarding_Pass`.`Aadhar_card_number`=`Passenger`.`Aadhar_card_number`)
                AND(`Route_ID`={0})
                        '''.format(crashed_route_id)

    display_query_result(cur, con, query_str)

# DONE
def analysis_airline_pilots(cur,con):

    iata_airline=input("Enter iata code of airline whose pilots are to be listed: ")
    query_str='''SELECT `Pilot_license_number`,`First_Name`,`Last_Name`,`Number_of_flying_hours`
                FROM `Pilot`,`Airline_Employees/CREW`
                WHERE (`Pilot`.`Aadhar_card_number`= `Airline_Employees/CREW`.`Aadhar_card_number`)
                AND (`Employer_IATA_Airline_Code`="{0}" )    
                        '''.format(iata_airline)

    display_query_result(cur, con, query_str)

# DONE
def analysis_favoured_aircrafts(cur,con):
    #print("Inside update_passenger func")
    #https://stackoverflow.com/a/2421441
    query_str='''SELECT `Manufacturer` AS `Manufacturer`,
                        `Plane_Model` AS `Model`,
                        COUNT(*) AS `Total occurrences`
                FROM `Aircraft`
                WHERE `Owners_IATA_Airline_Code`  IS NOT NULL
                GROUP BY `Manufacturer`,`Plane_Model`
                ORDER BY `Total occurrences` DESC;
                        '''
    
    display_query_result(cur, con, query_str)

########################################################################################################################################################
########################################################################################################################################################


def print_query(query, cur, con):
    try:
        #print(f"QUERY IS {query}")
        cur.execute(query)
        con.commit()
        result = cur.fetchall()
        
        if len(result) != 0:
            header = result[0].keys()
            rows =  [x.values() for x in result]
            print(tabulate(rows, header, tablefmt = 'psql'))
        
        else:
            print("Not found!") #length of result is 0

    except Exception as e:
        print(e)
        con.rollback()
        input("Press any key to continue")


def read_data(cur, con, table_Name):
    #print("inside " +  table_Name)

    query = "select * from `" + table_Name +"`;"
    print_query(query, cur, con)
    #table_Name = "`Airport
    
###########################################################################################################################################################
###########################################################################################################################################################


colors_dict = {
    "BLUE": "\033[1;34m",
    "RED": "\033[1;31m",
    "CYAN": "\033[1;36m",
    "GREEN": "\033[0;32m",
    "RESET": "\033[0;0m",
    "BOLD": "\033[;1m",
    "REVERSE": "\033[;7m",
    "ERROR": "\033[;7m"+"\033[1;31m"
}


def decorate(color_str):
    # print("Decorated")
    sys.stdout.write(colors_dict[color_str])


expose_add_funcs = [["Airline", "Passenger", "Airport", "Runway", "Route", "Terminal"],
                    ["Passenger", "Aircraft", "Route",
                        "Boarding Pass", "Airline Employees"],
                    ["Feedback and rating"]]

add_funcs_dict = {
    "Airline": add_airline,
    "Passenger": add_passenger,
    "Aircraft": add_aircraft,
    "Airport": add_airport,
    "Runway": add_runway,
    "Terminal": add_terminal,
    "Route": add_route,
    "Boarding Pass": add_Boarding_Pass_details,
    "Airline Employees": add_Airline_Employees_CREW,
    "Airport Employees": add_airport_crew,
    "Feedback and rating": add_feedback
}


def add_display(cur, con, user_id):

    decorate("BLUE")
    print("Select the entity whom you would like to insert in the Database:\n")
    i = 0
    tables_add = [
        "Airline",
        "Passenger",
        "Aircraft",
        "Airport",
        "Runway",
        "Terminal",
        "Route",
        "Boarding Pass",
        "Airline Employees",
        "Airport Employees",
        "Feedback and rating"
    ]

    decorate("RED")
    for i in range(len(expose_add_funcs[user_id])):
        print(f"Press {i} for insertion in {expose_add_funcs[user_id][i]}")
    decorate("RESET")

    choice_to_add = int(input("enter choice > "))
    if choice_to_add >= len(expose_add_funcs[user_id]) or choice_to_add < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        add_funcs_dict[expose_add_funcs[user_id][choice_to_add]](cur, con)


###########################################################################################################
expose_read_funcs = [
    ["Airline", "Passenger", "Airport", "Runway",
        "Terminal", "Boarding_Pass", "Route"],
    ["Route", "Airport_Employees/CREWS", "Aircraft",
        "Boarding_Pass", "Feedback and rating"],
    ["Route", "Airline", "Airport"]
]


def read_display(cur, con, user_id):

    decorate("BLUE")
    print("Select the entity whoose entries you want to view:\n")
    i = 0

    decorate("RED")
    for i in range(len(expose_read_funcs[user_id])):
        print(f"Press {i} for reading of {expose_read_funcs[user_id][i]}")
    decorate("RESET")

    choice_to_read = int(input("enter choice > "))
    if choice_to_read >= len(expose_read_funcs[user_id]) or choice_to_read < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        read_data(cur, con, expose_read_funcs[user_id][choice_to_read])


#################################################################################################


expose_delete_funcs = [["Airport Employees"],
                       ["Aircraft", "Route", "Airline Employees", "Luggage"],
                       []]

delete_funcs_dict = {
    # "Airline":delete_airline,#
    #  "Passenger":delete_passenger,#
    "Aircraft": delete_aircraft,
    #   "Airport":delete_airport,#
    #    "Runway":delete_runway,#
    #     "Terminal":delete_terminal,#
    "Route": delete_route,
    #      "Boarding Pass":delete_Boarding_Pass_details,#
    "Airline Employees": delete_Airline_Employees_CREW,
    "Airport Employees": delete_airport_crew,
    #       "Feedback and rating":delete_feedback,
    "Luggage": delete_Luggage
}


def delete_display(cur, con, user_id):

    if user_id == 2:
        print("This user has no permissions to delete from database")
        return

    decorate("BLUE")
    print("Select the entity whose entries you want to delete:\n")
    i = 0

    decorate("RED")
    for i in range(len(expose_delete_funcs[user_id])):
        print(f"Press {i} for deletion from {expose_delete_funcs[user_id][i]}")
    decorate("RESET")

    choice_to_delete = int(input("enter choice > "))
    if choice_to_delete >= len(expose_delete_funcs[user_id]) or choice_to_delete < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        delete_funcs_dict[expose_delete_funcs[user_id]
                          [choice_to_delete]](cur, con)


#################################################################################################
#################################################################################################


colors_dict = {
    "BLUE": "\033[1;34m",
    "RED": "\033[1;31m",
    "CYAN": "\033[1;36m",
    "GREEN": "\033[0;32m",
    "RESET": "\033[0;0m",
    "BOLD": "\033[;1m",
    "REVERSE": "\033[;7m",
    "ERROR": "\033[;7m"+"\033[1;31m"
}


def decorate_stuff(color_str):
    # print("Decorated")
    sys.stdout.write(colors_dict[color_str])

def date_less_cur(date_str):
    today_date = datetime.date.today()
    today_date_str = today_date.strftime("%Y-%m-%d")

    if date_str < today_date_str:
        return 1
    else:
        return 0


def date_more_cur(date_str):
    today_date = datetime.date.today()
    today_date_str = today_date.strftime("%Y-%m-%d")

    if date_str > today_date_str:
        return 1
    else:
        return 0


def print_err_date(state):
    decorate_stuff('ERROR')
    if state == 1:
        print('The date entered cannot be after current date. Current date: ' +
              str(datetime.date.today()))
    elif state == -1:
        print('The date entered cannot be before current date. Current date: ' +
              str(datetime.date.today()))
    decorate_stuff('RESET')


def numeric_check(ch):
    if ch >= '0' and ch <= '9':
        return 1
    else:
        return 0


def dep_ahead_arv(arrival_str, depart_str):
    #decorate_stuff('ERROR')
    #print(f"DEBUG:Arrival is {arrival_str}\nDeparture is {depart_str}")
    #decorate_stuff

    if len(arrival_str) != 5 or len(depart_str) != 5:
        print('Invalid format')
        decorate_stuff('RESET')

        return -1

    if numeric_check(arrival_str[0])+numeric_check(arrival_str[1])+numeric_check(arrival_str[3])+numeric_check(arrival_str[4]) != 4:
        print("Enter only digits for mm and hh in arrival time")
        decorate_stuff('RESET')

        return -1

    if numeric_check(depart_str[0])+numeric_check(depart_str[1])+numeric_check(depart_str[3])+numeric_check(depart_str[4]) != 4:
        print("Enter only digits for mm and hh in departure time")
        decorate_stuff('RESET')

        return -1

    arrival_hrs = int(arrival_str[0:2])
    arrival_min = int(arrival_str[3:5])
    depart_hrs = int(depart_str[0:2])
    depart_min = int(depart_str[3:5])

    if depart_hrs > arrival_hrs:
        print('Arrival time can not be ahead of departure time')
        decorate_stuff('RESET')

        return -1

    elif depart_hrs == arrival_hrs and depart_min > arrival_min:
        print('Arrival time can not be ahead of departure time')
        decorate_stuff('RESET')

        return -1

    else:
        return 0


def get_updation_equation(attr, key_attr):

    query_str = ""
    dict_len = len(attr.keys())
    i = -1
    
    for key, value in attr.items():

        i += 1
        if key in key_attr:
            continue
        if value == '' or value == 'NULL':
            continue

        query_str =query_str+ "`"+key+"`"+" = "+'"'+value+'"'

        if i != dict_len-1:
            query_str =query_str+ ", "

    if query_str[-2]==',':
        query_str=query_str[:-2]
    return query_str


def get_selection_equation(attr, key_attr):

    query_str = ""
    list_len = len(key_attr)
    i = -1

    for key in key_attr:
        i += 1

        if attr[key] == '':
            return ""

        query_str += "`"+key+"`"+" = "+'"'+attr[key]+'"'

        if i != list_len-1:
            query_str = query_str+" AND "

    return query_str


def try_except_block(attr, key_attr, cur, con, table_Name):
    #print('INSIDE try_except_block')
    try:
        set_values = get_updation_equation(attr, key_attr)
        decorate_stuff('ERROR')
        if set_values == "":
            print("ERROR: Some value must be selected for updation")
            print("Failed to update database")
            decorate_stuff('RESET')
            input("Press any key to continue")
            return

        cond_values = get_selection_equation(attr, key_attr)
        if cond_values == "":
            print("ERROR: Value of the key attributes cannot be NULL")
            print("Failed to update database")
            decorate_stuff('RESET')
            input("Press any key to continue")
            return

        query_str = "UPDATE "+table_Name+" SET "+set_values+" WHERE "+cond_values+" ; "
        #print(f"Query_STR IS ", query_str)
        cur.execute(query_str)
        con.commit()
        res_len = cur.rowcount
        decorate_stuff('BLUE')
        print(f"Number of tuples updated are {res_len}")
        decorate_stuff('GREEN')
        print('Updation successful')

        # display_updated_rows(result)
        decorate_stuff('RESET')

        return

    except Exception as e:
        print('ERROR:Failed to update the database.')
        con.rollback()
        print(e)
        decorate_stuff('RESET')
        input('Press any key to continue.')
        return

# checked

# DONE +++
def update_passenger(cur, con):
    #print("Inside update_passenger func")
    table_Name = "Passenger"

    attr = {}

    attr["Aadhar_card_number"] = input(
        "Enter Aadhar card number of the passenger you want to update: ")
    print("Press enter without entering any value if you don't want to update a particular value")
    tmp_Name = input("Enter new Name: ")

    key_attr = ["Aadhar_card_number"]

    Name_list = tmp_Name.split(' ')

    if len(Name_list) >= 3:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ' '.join(Name_list[1:-1])
        attr['Last_Name'] = Name_list[-1]
    elif len(Name_list) == 2:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = '-'
        attr['Last_Name'] = Name_list[1]
    elif len(Name_list) == 1:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = '-'
        attr['Last_Name'] = '-'
    else:
        attr['First_Name'] = ''
        attr['Minit'] = ''
        attr['Last_Name'] = ''

    attr["Gender"] = int(
        input("Enter Gender \n1. Male \n2. Female \n3. Others\n 4. Unchanged\n ENTER HERE >"))

    if attr['Gender'] == 1:
        attr['Gender'] = 'Male'
    elif attr['Gender'] == 2:
        attr['Gender'] = 'Female'
    elif attr['Gender'] == 3:
        attr['Gender'] = 'Others'
    else:
        attr['Gender'] = ''

    attr["House_Number"] = input("Enter new House_Number of residence: ")
    attr["Building"] = input("Enter new building number of residence: ")
    attr["City"] = input("Enter new city of residence: ")

    try_except_block(attr, key_attr, cur, con, table_Name)


def update_aircraft(cur, con):
    #print("inside update_aircraft function")
    table_Name = "`Aircraft`"

    attr = {}

    key_attr = ["Registration_No."]

    attr['Registration_No.'] = input("Enter registration number of aircraft: ")
    print("Press enter  without entering any value if you don't want to update a particular value")
    print('Enter updated details of the aircraft: ')
    attr['Flight_ID'] = input("Enter updated Flight_ID: ")
    attr['Last_Maintanence_Check_Date'] = input("Enter Last_Maintanence_Check_Date: [YYYY-MM-DD]: ")
    if date_more_cur(attr['Last_Maintanence_Check_Date']) == 1:
        print_err_date(1)
        con.rollback()
        return
    #attr['Owners_IATA_Airline_Code'] = input("Enter IATA code of owner airline: ")

    try_except_block(attr, key_attr, cur, con, table_Name)

  # checked

#DONE++
def update_airport(cur, con):
    #print("inside update_airport function")
    table_Name = "`Airport`"

    attr = {}

    key_attr = ["IATA_CODE"]

    print('Enter details of the new airport: ')

    attr["IATA_CODE"] = input(" Enter 3 character IATA code * :")
    print("Press enter  without entering any value if you don't want to update a particular value :")

    attr["Name"] = input("Enter the new Name of airport: ")

    try_except_block(attr, key_attr, cur, con, table_Name)



# checked
def update_runway_status(cur, con):
    #print("inside update_runway_status function")
    table_Name = "`Runway`"

    attr = {}

    key_attr = ["IATA_CODE", "Runway_ID"]

    attr["IATA_CODE"] = input(
        "Enter IATA airport code of corresponding airport: ")
    attr["Runway_ID"] = input("Enter Runway_ID: ")
    print("Press enter  without entering any value if you don't want to update a particular value")

    stat_choice = int(
        input("Enter status as\n 1 for assigned\n 2 for available\n 3 for disfunctional\n >"))

    attr["Status"] = ""
    if stat_choice == 1:
        attr["Status"] = 'Assigned'
    elif stat_choice == 2:
        attr["Status"] = 'Available'
    elif stat_choice == 3:
        attr["Status"] = 'Disfunctional'
    else:
        attr["Status"] = ''

    try_except_block(attr, key_attr, cur, con, table_Name)

# checked

#DONE++
def update_airport_crew(cur, con):
    #Name,yrs_exp, salary, nationality,employer, gender
    #print("inside update_airport_crew function")
    table_Name = "`Airport_Employees/CREWS`"

    attr = {}

    key_attr = ["Aadhar_card_number"]

    attr["Aadhar_card_number"] = input(
        "Aadhar card number of the employee you want to update: ")
    print("Press enter without entering any value if you don't want to update a particular value")

    tmp_Name = input("Enter new Name: ")

    Name_list = tmp_Name.split(' ')

    if len(Name_list) >= 3:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ' '.join(Name_list[1:-1])
        attr['Last_Name'] = Name_list[-1]
    elif len(Name_list) == 2:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = '-'
        attr['Last_Name'] = Name_list[1]
    elif len(Name_list) == 1:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = '-'
        attr['Last_Name'] = '-'
    else:
        attr['First_Name'] = ''
        attr['Minit'] = ''
        attr['Last_Name'] = ''

    attr["Experience"] = input("New total number of years of Experience: ")
    attr["Salary"] = input("New Salary: ")
    attr["Nationality"] = input("New Nationality: ")
    attr["Gender"] = input(
        "Enter Gender \n1. Male \n2. Female \n3. Others\n 4. Unchanged\n ENTER HERE >")

    if attr['Gender'] == 1:
        attr['Gender'] = 'Male'
    elif attr['Gender'] == 2:
        attr['Gender'] = 'Female'
    elif attr['Gender'] == 3:
        attr['Gender'] = 'Others'
    else:
        attr['Gender'] = ''
    attr["Working_Airport_IATA_CODE"] = input(
        "airport IATA code of employing airport: ")

    try_except_block(attr, key_attr, cur, con, table_Name)


##############################################################################################
def update_route_details(cur, con):
    #print("Inside update_route_details function")
    # NOTE: Distance_Travelled should be updated in route
    table_Name = "Route"

    attr = {}

    key_attr = ["Route_ID"]

    attr["Route_ID"] = input("Enter Route_ID for which the information needs to be updated: ")

    decorate_stuff('BLUE')
    print("Press enter without typing any value if you do not want to update value of a particular attribute")
    decorate_stuff("RESET")

    #############################################################################################
    
    attr['Status'] = input("Enter one of 'Departed', 'Boarding','On_route','Delayed','Arrived','Checking','Not_applicable' as the status: ")

    if attr['Status'] == 'Departed':
        decorate_stuff('BLUE')
        print("Also updating the status of the Take OFF Runway as `Available`")
        decorate_stuff('RESET')

        query_update = f'''UPDATE Route ,Runway SET Runway.`Status`="Available" WHERE `Runway_ID`=`Take_off_runway_id`
        AND `Route_ID`={attr["Route_ID"]}
        AND `Source_IATA_CODE`=`IATA_CODE`;'''

        cur.execute(query_update)
        tmp_var = ''
        tmp_var = input("Enter actual departure time of the flight in  [HH:MM] format: ")
        # attr["Actual departure time"]=input("Enter actual departure time of the flight in  [HH:MM] format")
        if tmp_var == '':
            print("ERROR: User failed to enter a non-empty input for ACTUAL FLIGHT departure time")
            return
        else:
            attr["Actual departure time"] = tmp_var

    elif attr['Status'] == 'Arrived':
        decorate_stuff('BLUE')
        print("Also updating the status of the LANDING Runway as `Available`")
        decorate_stuff('RESET')
        query_update = f'''UPDATE Route ,Runway SET Runway.`Status`="Available" WHERE `Runway_ID`=`Landing_RunWay_ID`
                        AND `Route_ID`={attr["Route_ID"]}
                        AND `Destination_IATA_CODE`=`IATA_CODE`;'''

        cur.execute(query_update)

        tmp_var = ''
        tmp_var = input(
            "Enter actual arrival time of the flight in  [HH:MM] format: ")
        # attr["Actual departure time"]=input("Enter actual departure time of the flight in  [HH:MM] format")
        if tmp_var == '':
            print("ERROR: User failed to enter a non-empty input for ACTUAL FLIGHT arrival time")
            return
        else:
            attr["Actual arrival time"] = tmp_var


        ####################################################################################    
        # job 2
        depart_query = '''SELECT `Actual departure time` FROM Route WHERE `Route_ID` = {0};'''.format(
            attr["Route_ID"])
        cur.execute(depart_query)
        temp = cur.fetchall()
        str_delta = str(temp)
        seconds = int(str_delta[-8:-3])
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        attr["Actual departure time"] = "{0}:{1:0=2d}".format(hours, minutes)

        if dep_ahead_arv(attr["Actual arrival time"], attr["Actual departure time"]) == -1:
            return

        tmp_var = input("Enter total Distance_Travelled by flight: ")
        # attr["Actual departure time"]=input("Enter actual departure time of the flight in  [HH:MM] format")
        if tmp_var == '':
            print("ERROR: User failed to enter OVERALL Distance_Travelled")
            return
        # Job 1
        else:
            attr["Distance_Travelled"] = tmp_var
            query_str = '''UPDATE Aircraft, Route 
                            SET Aircraft.`Distance_Travelled` = Aircraft.`Distance_Travelled` + {0} 
                            WHERE `Route_ID` = {1} AND Registration_No. = Registration_No.;'''.format(attr["Distance_Travelled"], attr["Route_ID"])
            
            query_str2 = '''UPDATE `Route`, `Pilot`
                            SET Pilot.`Number_of_flying_hours` = Pilot.`Number_of_flying_hours`  + 2
                            WHERE (`Route_ID` = {1})
                            AND  (`Aadhar_card_number`=`Pilot_Captain_Aadhar_card_number`); '''.format(0, attr["Route_ID"])
            try:
                cur.execute(query_str)
                cur.execute(query_str2)
                con.commit()

            except Exception as e:
                print("Failed to update the database.")
                con.rollback()
                print(e)
                input('Press any key to continue.')
                return

        #################################################################################################
            # Add distance to aircraft
            # Add flying hrs to both pilots
        ###############################################################################################

    attr["Take_off_runway_id"] = input("Enter NEW Runway_ID (if there was a change) which has been allotted for take_off: ")
    attr["Landing_RunWay_ID"] = input("Enter NEW Runway_ID (if there was a change) which has been allotted for LANDING: ")

    try_except_block(attr, key_attr, cur, con, table_Name)

#Name,yrs_exp, salary, nationality,employer, gender

#DONE+++++
def update_Airline_Employees_CREW_personal_details(cur, con):
    #print("inside update_Airline_Employees_CREW_personal_details function")
    table_Name = "`Airline_Employees/CREW`"

    attr = {}

    key_attr = ["Aadhar_card_number"]

    attr["Aadhar_card_number"] = input("Aadhar_card_number: ")
    print('Enter new details of the Airline_Employees/CREW entry: ')
    print("Press enter without typing any value if you do not want to update value of a particular attribute")

    tmp_Name = input("Enter new Name: ")

    Name_list = tmp_Name.split(' ')

    if len(Name_list) >= 3:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = ' '.join(Name_list[1:-1])
        attr['Last_Name'] = Name_list[-1]
    elif len(Name_list) == 2:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = '-'
        attr['Last_Name'] = Name_list[1]
    elif len(Name_list) == 1:
        attr['First_Name'] = Name_list[0]
        attr['Minit'] = '-'
        attr['Last_Name'] = '-'
    else:
        attr['First_Name'] = ''
        attr['Minit'] = ''
        attr['Last_Name'] = ''

    attr["Number of years of Experience"] = input(
        "Updated Number of years of Experience: ")
    attr["Salary"] = input("Salary: ")
    attr["Nationality"] = input("Nationality: ")
    attr["Gender"] = int(
        input("Enter Gender \n1 for Male \n2 for Female \n3 for Others\n4 for Unchanged\n ENTER HERE > "))

    if attr['Gender'] == 1:
        attr['Gender'] = 'Male'
    elif attr['Gender'] == 2:
        attr['Gender'] = 'Female'
    elif attr['Gender'] == 3:
        attr['Gender'] = 'Others'
    else:
        attr['Gender'] = ''
    attr["Employer_IATA_Airline_Code"] = input(
        "Airline employer IATA code: ")

    try_except_block(attr, key_attr, cur, con, table_Name)

#done+++++
def update_airline_details(cur, con):
    # Update num_aircradfts_owned, Active,country of ownership
    #print("inside update_airline_details function")
    table_Name = "`Airline`"

    attr = {}

    key_attr = ["IATA_Airline_Code"]

    attr['IATA_Airline_Code'] = input('Enter 2-character IATA airline designator code * : ')

    print('Enter new details of the Airline_Employees/CREW entry: ')
    print("Press enter without typing any value if you do not want to update value of a particular attribute")

  

    tmp = int(input('Enter 1 if airline is active, 0 if inactive, 2 for unchanged\n ENTER HERE > '))

    if tmp == 1:
        attr['Active'] = "1"
    elif tmp == 0:
        attr['Active'] = "0"
    else:
        attr['Active'] = ''

    attr['Country_of_Ownership'] = input(
        'Enter country of ownership of airline: ')

    try_except_block(attr, key_attr, cur, con, table_Name)

#done++++++
def update_atc_freq(cur, con):
    #print("inside update_atc_freq function")
    table_Name = "`Air_Traffic_Controller`"

    attr = {}

    key_attr = ["Aadhar_card_number"]
    attr['Aadhar_card_number'] = input(
        'Aadhar card number of the employee: ')
    print('Enter new details of the Air_Traffic_Controller: ')
    print("Press enter without typing any value if you do not want to update value of a particular attribute")
    attr['Current_communication_Frequency'] = input(
        "Current_communication_Frequency: ")

    try_except_block(attr, key_attr, cur, con, table_Name)



###############################################################################################################################
################################################################################################################################


expose_update_funcs = [["3", "4", "5", "6", "9"],
                       ["1", "2", "6", "7", "8"],
                       []]

update_funcs_dict = {
    "1": update_passenger,
    "2": update_aircraft,
    "3": update_airport,
    "4": update_runway_status,
    "5": update_airport_crew,
    "6": update_route_details,
    "7": update_Airline_Employees_CREW_personal_details,
    "8": update_airline_details,
    "9": update_atc_freq
}

update_funcs_msg = {
    "1": "for updating Name, gender, address of passenger",
    "2": "for updating Flight_ID, last check maintenance date aircraft",
    "3": "for updating Name of airport",
    "4": "for updating status of runway",
    "5": "for updating Name, years of experiences, salary, nationality, employer, gender of airport crew",
    "6": "for updating actual arrival time, actual departure time, Distance_Travelled over the route, status of the journey",
    "7": "for updating airline crew personal details like salary, current employer etc.",
    "8": "for updating active_status of the airline, country of wonership",
    "9": "for updating the frequency at which the air traffic contoller is operating"
}

# in 11, give status change, time change,


def update_display(cur, con, user_id):
    if user_id == 2:
        print("This user has no permissions to update database")
        return
    decorate("BLUE")
    print("Select option as per what you want to update:\n")
    i = 0

    decorate("RED")
    len_use = len(expose_update_funcs[user_id])
    for i in range(len_use):
        print(
            "Press ",i,"for ",update_funcs_msg[expose_update_funcs[user_id][i]])
    decorate("RESET")

    choice_to_update = int(input("enter choice > "))
    if choice_to_update >= len(expose_update_funcs[user_id]) or choice_to_update < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        update_funcs_dict[expose_update_funcs[user_id]
                          [choice_to_update]](cur, con)


#################################################################################################

expose_analysis_funcs = [["1", "2", "3", "4", "5", "6", "8", "9", "10", "11"],
                         ["1", "2", "5", "7", "8", "10", "11"],
                         ["2", "3", "5", "6", "8", "11"]]


analysis_funcs_dict = {
    "1": analysis_passenger_Boarding_Pass_Special_Services,
    "2": analysis_big_airlines,
    "3": analysis_experienced_pilot,
    "4": analysis_search_Name,
    "5": analysis_busiest_airports,
    "6": analysis_loved_airlines,
    "7": analysis_feedback_patterns,
    "8": analysis_find_tickets,
    "9": analysis_crashed_survivors,
    "10": analysis_airline_pilots,
    "11": analysis_favoured_aircrafts
}

analysis_funcs_msg = {
    "1": "Names of all passengers who have WHEELCHAIR ASSISTANCE/Disability assisstance as a special service in their BOARDING PASS",
    "2": "Names OF ALL AIRLINES whose flight crew is >=x where 'x' is to be inputted from user",
    "3": "find the pilot with maximum number of flying hrs",
    "4": "Search for all PASSENGERS whose Name contains a given substring",
    "5": "RANK BUSIEST AIRPORTS by number of scheduled flight departures on a particular day",
    "6": "RANK most used aircraft by sorting as per the number of boarding passes issued for that aircraft since data collection began",
    "7": "Feedback of flight crew patterns",
    "8": "display all flights between two airports on a given date or on any date",
    "9": "Names of all passengers who were travelling on a particular route/Crashed flight/Flight with a COVID infected patient",
    "10": "Names of all pilots who work for a given airline",
    "11": "Find most used aircraft across all airlines"
}


def analysis_display(cur, con, user_id):

    decorate("BLUE")
    print("Select option:\n")
    i = 0

    decorate("RED")
    for i in range(len(expose_analysis_funcs[user_id])):
        print(
            f"Press {i} for query {analysis_funcs_msg[expose_analysis_funcs[user_id][i]]}")
    decorate("RESET")

    choice_to_analysis = int(input("enter choice > "))
    if choice_to_analysis >= len(expose_analysis_funcs[user_id]) or choice_to_analysis < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        analysis_funcs_dict[expose_analysis_funcs[user_id]
                            [choice_to_analysis]](cur, con)


#########################################################################################

def dispatch(ch, cur, con, user_id):
    

    if (ch == 1):
        add_display(cur, con, user_id)
    elif (ch == 2):
        update_display(cur, con, user_id)
    elif (ch == 3):
        delete_display(cur, con, user_id)
    elif (ch == 4):
        read_display(cur, con, user_id)
    elif (ch == 5):
        analysis_display(cur, con, user_id)
    else:
        print("Error: Invalid Option")


def display_menu(cur, con, user_id):

    decorate("CYAN")
    print("Select operation you want to perform")
    print("1. Add new information")
    print("2. Update tables")
    print("3. Delete data")
    print("4. Read data")
    print("5. Analysis data")
    print("6. Logout")
    decorate("RESET")

    ch = int(input("Enter choice> "))
    if ch == 6:
        raise SystemExit
    else:
        dispatch(ch, cur, con, user_id)
        tmp = input("Enter any key to CONTINUE>")


# Global
while (1):
    
    tmp = sp.call('clear', shell=True)
    userName = input("UserName: ")
    password = input("Password: ")

    try:
        con = pymysql.connect(host='localhost',
                              port=3306,
                              user=userName,
                              password=password,
                              db='Airport_Database',
                              cursorclass=pymysql.cursors.DictCursor)

        tmp = sp.call('clear', shell=True)

        '''Return True if the connection is open'''
        
        if (con.open):
            print("Connected")
            
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        
        decorate("CYAN")
        print("Press 0 if you are airport_employee")
        print("Press 1 if you are airline_employee")
        print("Press 2 if you are passenger")
        decorate("RESET")

        user_id = int(input())

        with con.cursor() as cur:
            while (1):
                tmp = sp.call('clear', shell=True)
                display_menu(cur, con, user_id)

    except Exception as e:
        print("Connection Refused: Either userName or password is incorrect or user doesn't have access to database")
        print(">>>", e)
        tmp = input("Enter any key to CONTINUE>")
        
