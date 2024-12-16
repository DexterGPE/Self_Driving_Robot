import time
import BrickPi3

# Initialize the BrickPi3 object
BP = BrickPi3.BrickPi3()

# Set up motor ports (Motor A, Motor B, etc.)
motor_port = BP.PORT_A
#rechts poort A
#links poort B
# Function to control the motor and collect data
def collect_data(duration, motor_speed):
    # Open a text file to save the data
    with open('motor_data.txt', 'w') as f:
        # Write the header line
        f.write('time (s)\tinput_voltage (V)\tmeasured_rotation (deg)\n')
        
        # Start time
        start_time = time.time()

        # Set the motor speed (input command)
        BP.set_motor_power(motor_port, motor_speed)

        # Collect data for the specified duration
        while time.time() - start_time < duration:
            # Read the motor encoder value (measured rotation)
            measured_rotation = BP.get_motor_encoder(motor_port)
            
            # In practice, you might need to scale the motor speed to an actual voltage value
            # For simplicity, we'll use the motor speed directly (in percentage)
            input_voltage = motor_speed  # This is a simplification; actual voltage might need adjustment
            
            # Get the current time since start
            current_time = time.time() - start_time
            
            # Write the data to the file (tab-separated)
            f.write(f'{current_time:.2f}\t{input_voltage:.2f}\t{measured_rotation}\n')
            
            # Sleep for a short time to avoid excessive CPU usage and to control the sampling rate
            time.sleep(0.1)

# Example: Run the data collection for 10 seconds with a motor speed of 50
collect_data(duration=5, motor_speed=50)

print('Data collection complete. Data saved to motor_data.txt')
