class Pirep():
    
    def __init__(self,url="",pirep_id=""):
        if url != "":
            self.URL = url
            self.ID = Get_ID_From_URL(url)
        elif pirep_id != "":
            self.ID = pirep_id
            self.URL = Get_URL_From_ID(pirep_id)
        else:
            self.URL = url
            self.ID = pirep_id
            
        self.Airline_Code = ""
        self.Flight_Number = ""
        self.Leg_Number = ""
        self.Pilot = {"ID": "", "Rank": "", "Program": ""}
        self.Status = {"ID": "", "Raw": "", "Approver": "", "Date": "", "Flight_Assignment": ""}
        self.Submitted_Date = ""
        self.Origin = ""
        self.Departure_Route = ""
        self.Arrival = ""
        self.Arrival_Route = ""
        self.Simulator = ""
        self.Other_Information = ""
        self.Counts_Promotion = ""
        self.Distance = ""
        self.Logged_Time = ""
        self.Passengers_Carried = ""
        self.Load_Factor = ""
        self.ACARS_Flight_ID = ""
        self.Num_Position_Records = ""
        self.Data_Recorder = ""
        self.FDE_File = ""
        self.Aircraft_SDK = ""
        self.Times = {"Start": "", "Taxi_from_Gate": "", "Takeoff": "", "Landing": "", "Arrival": ""}
        self.Cruise_Altitude = ""
        self.Total_Fuel_Used = ""
        self.Payload_Weight = {"Passengers": "", "Cargo": ""}
        self.Flight_Time = ""
        self.Time_Paused = ""
        self.Flight_Time_1X = ""
        self.Route = ""
        self.Dispatch = {"Used": "", "Dispatcher": ""}
        self.Network = ""
        return

def Get_ID_From_URL(url):
    index = url.find("id=")
    pirep_id = url[index+3:]
    return pirep_id


def Get_URL_From_ID(pirep_id):
    url = "https://www.deltava.org/pirep.do?id=" + pirep_id
    return url
