# Airport Management System 


The database is a **CENTRAL AIRPORTS DATABASE MANAGEMENT** and its users are the personnel at the airport, the air travellers and their relatives. This database is well-connected to the rest of the airport modules: airline databases, revenue management, and air traffic management. 

This database has or can be extended to have a lot of functionality like:

* Keeping track of flight status and schedules for the travellers to know about flight cancellation, flight delays
* Supervision of aircraft landing and take off, airport traffic management, runway status management
* Retrieval of information regarding airport finances: staff payrolls, etc
* Baggage tagging from the  time the baggage is loaded and its tracking until the destination is reached and the bag is returned to the owners.
* Keeping a record of a passenger’s journey from passenger processing (check-in, boarding) and baggage handling (dropping and handling) to the moment he boards the aircraft
* Retrieving information for different segments of users: passengers, airport staff, crew, or members of specific departments, authorities, business partners, or police.

File structure : 
#### `airport_bd.py`
* contains the non-CRUD functional operations to be performed on the database
* prints the tables in a tabulated manner
* performs update operations on the database
* contains main loop and connections to pymysql. Also contains function headers 2)
       
* adds tuples in various tables
* deletes tuples in various tables
### ` airport_db.sql`
* create all tables in Airport Data base

### Install pymySql
```
$ python3 -m pip install PyMySQL
```

# Instructions to run
```
$ python3 airport_db.py
```

# User-menu
We have divided the prospective users into three categories and have exposed parts of the database depending on the category of the user. Eg-> A passenger does not have permissions to change the scheduled departure time of a particular flight.

* Airport employees/Employees of The Airports Authority of India or AAI
* Airline employees
* Passengers

# NOTE
Whenever you change the status of a ROUTE as `Flight Arrived`, then automatically the ROUTE hrs are added to `number of flying hrs` of the pilot who piloted the flight. The distance covered in the journey also gets added to the `aircraft's total distance covered`.

## Commanads Extecuted in Video
### update:
   1) update the name of airport whose IATA code is "DEL"
   2) update the name,year of experience,salary,nationality,employer,gender of airport crew whose Addhar number is "774572687679"
   3) update the name,gender,nd address of passenger whose Aadhar card no is "999096482163"

### others:
  1) find the most aircraft across all airlines;
  2) find the pilot with max no of flying hours;
  3) RANK most used aircraft by sorting as per the no of boarding passess essued for thst aircraft since data collection began;
  4) display all the flights between "DEL" and "MUM" on "2022-10-06";
  5) all passengers whose name contains "si" as a substring
  6)name all the airlines whose flight crew is >=5 ;



## OPERATIONS ON DATABASE
# Retrieval Operations

## SELECTION
* Retrieve complete data tuples of PILOTS who work for a particular AIRLINE.
* Retrieve complete data tuples of PASSENGERS who were travelling on a particular crashed flight
* Display all flights between two airports on a given date

## Projection Query
* Names of all passengers who have WHEELCHAIR ASSISTANCE as a special service in their BOARDING PASS
* NAMES OF ALL AIRLINES whose flight crew is >=x where `x` is inputted by user

## AGGREGATE :
* Find the PILOT who has the maximum number of FLYING HOURS on record.
* Find most used aircraft across all airlines

## SEARCH
* Search for all PASSENGERS whose name contains `user inputted substring`

## ANALYSIS : 
* RANK BUSIEST AIRPORTS by number of scheduled flight departures on a particular day
* RANK most used airline by sorting as per the number of boarding passes issued for that airline since data collection began
* Feedback of flight crew

# Modification Operations

## Insertion Operations(also checking integrity constraint)

* Addition of a new employee [check SSN format]
* Addition of a newly constructed runway [check between 0 and 36]
* Addition of baggage to a particular boarding pass
* Addition of a new aircraft

## Update Operations
* Update flight status information based on time delay
* Update statistics regarding total number of kms travelled by airplane, total number of flying hours of a pilot
* Update status of runway

## Delete Operations
* Deletion of a plane which is no longer active
* Deletion of an inactive/fired employee

## Project by `TEAM-43`
- Abhinay Maurya (2021101132)
- Shiva koti reddi (2021101136)
- Kadali Nirmala (2021101126)
