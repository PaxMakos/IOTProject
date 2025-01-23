#Mqtt connection constants
CONNECTION_CANAL = "parking/entrace"
BROKER = "localhost"


#Mqtt messages
CONNECTED_MESSAGE = "Connected at "
DISCONNECTED_MESSAGE = "Disconnected at "

ENTRANCE_MESSAGE_1 = "Car entered at "
ENTRANCE_MESSAGE_2 = "Card read UID: "

EXIT_MESSAGE_1 = "Car exited at: "
EXIT_MESSAGE_2 = "; Card read UID: "


#Time constants
DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
DEBOUNCE_TIME = 5.0


#Oled constants
WELCOME_MESSAGE = "Welcome to/the parking/gate system!"
GOODBYE_MESSAGE = "Goodbye from/the parking/gate system!"
SECOND_ENTRY_MESSAGE = "Second entry/not allowed!"
SECOND_EXIT_MESSAGE = "Second exit/not allowed!"
ERROR_MESSAGE = "Error/reading card!"