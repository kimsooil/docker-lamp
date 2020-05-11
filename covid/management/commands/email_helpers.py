def generate_email_body(username, password):
    return '''Welcome to the SEIRcast website. 

Instructions for using the SEIRcast website.

1) Navigate to the website as https://covid.crc.nd.edu/
2) Select either "Login to Portal", "Epidemic Tracking", "Hospital Resources", or "COVID-19 Case Map" and you will be presented with the sign in screen
3) Enter your login credentials for Identity and Password included in this email and click “Sign In”
    Your username: {}
    Your password: {}
    If you had already logged on and set a different password, use this one instead. All user account passwords have been reset to support automated user onboarding.
4) You can now navigate and explore the website.

The menu on the left hand side has options "EPIDEMIC", "RESOURCES" and "MAP",

EPIDEMIC
This page shows data for tracking and planning for the Epidemic and presents 5 Tabs containing various charts:
    Cumulative Cases.
        - Cumulative confirmed cases refers to the running total confirmed case count. This does not include undetected cases.
    Daily Infectious Cases
        - Active infectious cases refers to the total number of individuals who are capable of transmitting the virus on a given day. This includes asymptomatic and symptomatic individuals.
        - New infectious cases refers to the number of individuals who are entering the infectious stage of illness on a given day. This includes asymptomatic and symptomatic individuals.
    Daily Symptomatic Cases
        - Active infectious symptomatic cases refers to the total number of individuals who are capable of transmitting the virus on a given day and have developed symptoms.
        - New infectious symptomatic cases refers to the number of individuals who are entering the infectious stage of illness on a given day and have developed symptoms.
    Hospitalized Cases
        - Hospitalized cases refers to the total number of individuals requiring a hospital bed on a given day. This does not include those requiring an ICU bed.
    ICU Cases
        - ICU cases refers to the total number of individuals who are requiring an ICU bed on a given day.

RESOURCES
This page shows data for Hospital Resource Planning and presents 3 Tabs containing various charts:
    Med/Surg & PDU Bed Capacity
        - Hospitalized bed requirements refers to the total number of hospital beds required on a given day for covid-19 patients. This does not include ICU bed requirements. 
        - Capacity refers to an estimate of the total number of hospital beds available in the selected counties.
    ICU Bed Capacity
        - ICU bed requirements refers to the total number of ICU beds required on a given day for covid-19 patients. 
        - Capacity refers to an estimate of the total number of ICU beds available in the selected counties.
    Ventilator requirements, refers to the total number of ventilators required on a given day for covid-19 patients. 
        - Capacity refers to an estimate of the total number of ventilators available in the selected counties.

MAPS
Presents a map of the state with counties color coded by shades of red representing the number of confirmed cases in the county.
    Hovering over a county provides the following information,
        - County name, confirmed cases
        - Active Infectious cases detected, number/max/min
        - Active Infectious cases undetected, number/max/min
        - New Infectious cases detected, number/max/min
        - New Infectious cases undetected, number/max/min
    '''.format(username, password)