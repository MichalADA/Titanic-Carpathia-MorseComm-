# Titanic-Carpathia-MorseComm-



A historical simulation of Morse code radio communication between RMS Titanic and RMS Carpathia during the tragic events of April 14-15, 1912.
Project Overview
This application simulates the wireless telegraph communication between the Titanic and Carpathia ships during the Titanic disaster. The system recreates the Morse code transmissions that occurred as Titanic sent distress signals and Carpathia responded, ultimately leading to the rescue of survivors.
The simulation consists of two separate applications that communicate with each other over a network connection:

Titanic Radio Station: Simulates the radio room on the Titanic, sending distress signals
Carpathia Radio Station: Simulates the radio room on the Carpathia, responding to the emergency

Historical Context
On April 14, 1912, RMS Titanic struck an iceberg in the North Atlantic Ocean and began to sink. The ship's radio operators, Jack Phillips and Harold Bride, sent distress signals using both the newer "SOS" and the traditional "CQD" Morse code signals.
The RMS Carpathia, captained by Arthur Rostron, received these distress calls and immediately changed course to assist. Despite being 58 nautical miles away, Carpathia raced to the scene at full speed, arriving approximately 4 hours after Titanic had sunk. Carpathia managed to rescue 705 survivors from Titanic's lifeboats.
This was one of the first major maritime disasters where radio played a crucial role in rescue operations, demonstrating the importance of wireless communication at sea.
Features

Authentic Radio Communication: Simulation of Morse code transmission and reception
Historical Accuracy: Pre-defined messages based on actual historical transcripts
Visual Signal Representation: Blinking indicator representing Morse code signals
Communication Log: Record of all transmitted and received messages
Network Communication: Applications communicate via TCP/IP to simulate radio transmission
Period-Accurate Interface: UI styled to resemble early 20th century equipment
Simulated Radio Interference: Random noise and delays to represent historical radio conditions

Technical Details

Built with Python and Tkinter for the graphical interface
Uses socket programming for network communication
Implements Morse code translation and sound generation
Runs on Windows, macOS, and Linux

Requirements

Python 3.6 or newer
Tkinter (usually included with Python)
Network connectivity between the two applications (can run on the same computer)

Future Development Plans

Add sound effects for telegraph operations
Implement more historical messages and scenarios
Create a single-application mode with AI-controlled responses
Add educational information about the historical event
Improve visual effects for signal transmission

Educational Value
This simulator serves as an educational tool to:

Demonstrate historical communication methods
Illustrate the challenges of early wireless technology
Provide insight into the Titanic disaster timeline
Teach Morse code in an engaging, historical context

Acknowledgments
This project was created as an extension of a Morse code translator. It aims to provide an interactive way to experience a pivotal moment in maritime and communication history.

Note: This is a simulation for educational purposes. The content is based on historical records, but some artistic license has been taken to create an engaging experience.
