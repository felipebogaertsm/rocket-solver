"""
Test suite for generating .eng files for motor simulation software 
(e.g., OpenRocket, RASAero).

Requirements for an .eng file:
---------------------------------
1. **File Header**:
   - The first non-comment line in the file must follow this format:
     `"MotorName OuterDiameter(mm) ChamberLength(mm) P InitialPropellantMass(kg)
     TotalMass(kg) Manufacturer"`
     - **MotorName**: Name of the motor.
     - **OuterDiameter**: Outer diameter of the motor, in millimeters, with four
       decimal places.
     - **ChamberLength**: Length of the motor's chamber, in millimeters, with four
       decimal places.
     - **P**: Indicates that this is a solid motor.
     - **InitialPropellantMass**: The initial mass of the propellant, in kilograms,
       with four decimal places.
     - **TotalMass**: The total mass of the motor (propellant + motor dry mass),
       in kilograms, with four decimal places.
     - **Manufacturer**: The name of the motor's manufacturer.

2. **Time and Thrust Data**:
   - After the header, time and thrust data are presented as two columns:
     - **Time (s)**: Time in seconds, starting from 0, with two decimal places.
     - **Thrust (N)**: Thrust in Newtons, with no decimal places.
   - The time values must be strictly increasing and must begin at 0.
   - The thrust values must be non-negative.

3. **File Formatting**:
   - The file should not contain any trailing whitespace at the end of lines.
   - The file must end with a semicolon (`;`).

4. **Data Resolution**:
   - The number of time and thrust data points in the file is controlled by the
     user-defined resolution (e.g., `eng_res`).
   - The thrust data is interpolated to match the desired number of time steps.

5. **General Requirements**:
   - The .eng file must begin with comments that describe the file's origin 
     (e.g., "Generated by Machwave program").
   - The content of the file should adhere to the specific structure required
     by simulation software.
"""

import pytest
import numpy as np

from machwave.services.export_formats import generate_eng_file_content


@pytest.fixture
def payload_data():
    """
    Fixture to set up common test data used in all test cases.
    """
    return {
        "time": np.linspace(0, 5, 100),  # Simulated time data
        "thrust": np.linspace(0, 500, 100),  # Simulated thrust data
        "propellant_mass": np.linspace(
            10, 0, 100
        ),  # Simulated propellant mass data
        "burn_time": 5,
        "chamber_length": 0.5,
        "outer_diameter": 0.1,
        "motor_mass": 5.0,
        "manufacturer": "TestManufacturer",
        "name": "TestMotor",
        "eng_res": 25,
    }


def test_eng_header_format(payload_data):
    """
    Test if the header in the .eng file is formatted correctly.
    """
    content = generate_eng_file_content(
        time=payload_data["time"],
        thrust=payload_data["thrust"],
        propellant_mass=payload_data["propellant_mass"],
        burn_time=payload_data["burn_time"],
        chamber_length=payload_data["chamber_length"],
        outer_diameter=payload_data["outer_diameter"],
        motor_mass=payload_data["motor_mass"],
        manufacturer=payload_data["manufacturer"],
        name=payload_data["name"],
        eng_res=payload_data["eng_res"],
    )

    # Extract the header (first line after the comments)
    lines = content.strip().split("\n")
    header = lines[1]  # 2nd line after comments

    # Check the format of the header
    expected_start = f"{payload_data['name']} {payload_data['outer_diameter'] * 1e3:.4f} {payload_data['chamber_length'] * 1e3:.4f} P"
    initial_mass = f"{payload_data['propellant_mass'][0]:.4f}"
    total_mass = f"{payload_data['propellant_mass'][0] + payload_data['motor_mass']:.4f}"
    assert header.startswith(
        expected_start
    ), "Header start format is incorrect."
    assert (
        initial_mass in header
    ), "Initial propellant mass is missing or incorrect."
    assert total_mass in header, "Total mass is missing or incorrect."
    assert (
        payload_data["manufacturer"] in header
    ), "Manufacturer name is missing."


def test_eng_data_format(payload_data):
    """
    Test if the time and thrust data in the .eng file are formatted correctly.
    """
    content = generate_eng_file_content(
        time=payload_data["time"],
        thrust=payload_data["thrust"],
        propellant_mass=payload_data["propellant_mass"],
        burn_time=payload_data["burn_time"],
        chamber_length=payload_data["chamber_length"],
        outer_diameter=payload_data["outer_diameter"],
        motor_mass=payload_data["motor_mass"],
        manufacturer=payload_data["manufacturer"],
        name=payload_data["name"],
        eng_res=payload_data["eng_res"],
    )

    # Extract the data lines (after the header)
    lines = content.strip().split("\n")
    data_lines = [line for line in lines if not line.startswith(";")][
        1:
    ]  # Skip header

    # Check that time and thrust are formatted correctly
    for line in data_lines:
        time_value, thrust_value = line.split()
        assert (
            len(time_value.split(".")[1]) == 2
        ), "Time must have two decimal places."
        assert (
            len(thrust_value.split(".")) == 1
        ), "Thrust must have zero decimal places."


def test_eng_data_values(payload_data):
    """
    Test if the time and thrust values in the .eng file meet the required constraints:
    - Time must be increasing and start from 0.
    - Thrust must be non-negative.
    """
    content = generate_eng_file_content(
        time=payload_data["time"],
        thrust=payload_data["thrust"],
        propellant_mass=payload_data["propellant_mass"],
        burn_time=payload_data["burn_time"],
        chamber_length=payload_data["chamber_length"],
        outer_diameter=payload_data["outer_diameter"],
        motor_mass=payload_data["motor_mass"],
        manufacturer=payload_data["manufacturer"],
        name=payload_data["name"],
        eng_res=payload_data["eng_res"],
    )

    # Extract the data lines (after the header)
    lines = content.strip().split("\n")
    data_lines = [line for line in lines if not line.startswith(";")][
        1:
    ]  # Skip header

    times = []
    thrusts = []

    # Parse the time and thrust values from the data lines
    for line in data_lines:
        time_value, thrust_value = line.split()
        times.append(float(time_value))
        thrusts.append(float(thrust_value))

    # Ensure time is increasing and starts from 0
    assert times[0] == 0, "Time must start from 0."
    assert all(
        t2 > t1 for t1, t2 in zip(times, times[1:])
    ), "Time must be strictly increasing."

    # Ensure thrust values are non-negative
    assert all(t >= 0 for t in thrusts), "Thrust must be non-negative."


def test_eng_file_ends_with_semicolon(payload_data):
    """
    Test if the .eng file ends with a semicolon.
    """
    content = generate_eng_file_content(
        time=payload_data["time"],
        thrust=payload_data["thrust"],
        propellant_mass=payload_data["propellant_mass"],
        burn_time=payload_data["burn_time"],
        chamber_length=payload_data["chamber_length"],
        outer_diameter=payload_data["outer_diameter"],
        motor_mass=payload_data["motor_mass"],
        manufacturer=payload_data["manufacturer"],
        name=payload_data["name"],
        eng_res=payload_data["eng_res"],
    )

    # Check that the file ends with a semicolon
    assert content.strip().endswith(
        ";"
    ), "The .eng file must end with a semicolon."


if __name__ == "__main__":
    pytest.main()
