import numpy as np


def generate_eng_file_content(
    time: np.ndarray,
    thrust: np.ndarray,
    propellant_mass: np.ndarray,
    burn_time: float,
    chamber_length: float,
    outer_diameter: float,
    motor_mass: float,
    manufacturer: str,
    name: str,
    eng_res: int = 25,
) -> str:
    """
    Generates a string containing the content of an .eng file for use in rocket
    simulation software.

    Args:
        time (np.ndarray): Time array (in seconds).
        thrust (np.ndarray): Thrust array (in Newtons).
        propellant_mass (np.ndarray): Propellant mass array at different times
            (in kg).
        burn_time (float): Total burn time (in seconds).
        chamber_length (float): Length of the chamber (in meters).
        outer_diameter (float): Outer diameter of the motor (in meters).
        motor_mass (float): Mass of the motor (in kg).
        manufacturer (str): Manufacturer name.
        name (str): Name of the motor.
        eng_res (int): Resolution of the .eng file (number of time steps to
            output). Default is 25.

    Returns:
        str: The content of the .eng file as a string.
    """
    # Trim data to burn time
    burn_index = np.where(time <= burn_time)[0]
    time = time[burn_index]
    thrust = thrust[burn_index]
    propellant_mass = propellant_mass[burn_index]

    # Form a new time vector with exactly 'eng_res' points
    t_out = np.linspace(0, time[-1], eng_res)

    # Interpolate thrust and propellant mass for the new time vector
    thrust_out = np.interp(t_out, time, thrust, left=0, right=0)
    propellant_mass_out = np.interp(t_out, time, propellant_mass, right=0)

    # Create the header
    eng_header = (
        f"{name} {outer_diameter * 1e3:.4f} {chamber_length * 1e3:.4f} P "
        f"{propellant_mass_out[0]:.4f} {propellant_mass_out[0] + motor_mass:.4f} "
        f"{manufacturer}\n"
    )

    # Generate the content for the .eng file
    eng_content = "; Generated by Machwave program\n" + eng_header
    for i in range(eng_res):
        eng_content += f"   {t_out[i]:.2f} {thrust_out[i]:.0f}\n"
    eng_content += ";"

    return eng_content