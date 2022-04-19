# -*- coding: utf-8 -*-
# Author: Felipe Bogaerts de Mattos
# Contact me at felipe.bogaerts@engenharia.ufjf.br.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.

"""
Stores utility functions, used in various locations throughtout the 
application.
"""

import numpy as np
import pandas as pd


def motor_to_eng(
    t,
    F,
    dt,
    V_prop_CP,
    D_out,
    L_chamber,
    eng_res,
    pp,
    m_motor,
    manufacturer,
    name,
):
    """
    Exports an eng file to the directory 'outputs' inside the program folder.
    """

    # Making the received volume array the same length as the time vector.
    V_prop = np.zeros(np.size(t))
    for i, volume in enumerate(V_prop_CP):
        V_prop[i] += volume

    # Forming a new time vector that has exactly 'eng_res' points
    # (independent on time step input):
    t_out = np.linspace(0, t[-1] + dt, eng_res)
    # Interpolating old thrust-time data into new time vector:
    F_out = np.interp(t_out, t, F, left=0, right=0)
    # Interpolating the Propellant volume with the new time vector
    # (to find propellant. mass with t):
    m_prop_out = pp * np.interp(t_out, t, V_prop, right=0)

    # Writing to the ENG file:
    eng_header = (
        f"{name} {D_out * 1e3:.4f} {L_chamber * 1e3:.4f} P "
        f"{m_prop_out[0]:.4f} {m_prop_out[0] + m_motor:.4f} "
        f"{manufacturer}\n"
    )
    saveFile = open(f"output/{name}.eng", "w")
    saveFile.write(
        "; Generated by SRM Solver program written by Felipe Bogaerts de Mattos\n; Juiz de Fora, Brasil\n"
    )
    saveFile.write(eng_header)
    for i in range(eng_res):
        saveFile.write("   %.2f %.0f\n" % ((t_out[i]), (F_out[i])))
    saveFile.write(";")
    saveFile.close()


def print_results(
    grain,
    structure,
    ib_parameters,
    structural_parameters,
    ballistics,
    rocket,
):
    print(
        "\nResults generated by SRM Solver program, by Felipe Bogaerts de Mattos"
    )

    print("\nBURN REGRESSION")
    if ib_parameters.m_prop[0] > 1:
        print(f" Propellant initial mass {ib_parameters.m_prop[0]:.3f} kg")
    else:
        print(
            f" Propellant initial mass {ib_parameters.m_prop[0] * 1e3:.3f} g"
        )
    print(" Mean Kn: %.2f" % np.mean(ib_parameters.Kn))
    print(" Max Kn: %.2f" % np.max(ib_parameters.Kn))
    print(
        f" Initial to final Kn ratio: {ib_parameters.initial_to_final_kn:.3f}"
    )
    print(
        f" Volumetric efficiency: {(ib_parameters.V_prop[0] * 100 / ib_parameters.V_empty):.3f} %"
    )
    print(
        f" Grain length for neutral profile vector: {ib_parameters.optimal_grain_length}"
    )

    print(" Burn profile: " + ib_parameters.burn_profile)
    print(
        f" Initial port-to-throat (grain #{grain.segment_count:d}): {ib_parameters.initial_port_to_throat:.3f}"
    )
    print(
        " Motor L/D ratio: %.3f"
        % (np.sum(grain.segment_length) / grain.outer_diameter)
    )
    print(
        f" Max initial mass flux: {np.max(ib_parameters.grain_mass_flux):.3f} kg/s-m-m or "
        f"{np.max(ib_parameters.grain_mass_flux) * 1.42233e-3:.3f} lb/s-in-in"
    )

    print("\nCHAMBER PRESSURE")
    print(
        f" Maximum, average chamber pressure: {(np.max(ib_parameters.P0) * 1e-6):.3f}, "
        f"{(np.mean(ib_parameters.P0) * 1e-6):.3f} MPa"
    )

    print("\nTHRUST AND IMPULSE")
    print(
        f" Maximum, average thrust: {np.max(ib_parameters.T):.3f}, {ib_parameters.T_mean:.3f} N"
    )
    print(
        f" Total, specific impulses: {ib_parameters.I_total:.3f} N-s, {ib_parameters.I_sp:.3f} s"
    )
    print(
        f" Burnout time, thrust time: {ib_parameters.t_burnout:.3f}, {ib_parameters.t_thrust:.3f} s"
    )

    print("\nNOZZLE DESIGN")
    print(f" Average opt. exp. ratio: {np.mean(ib_parameters.E_opt):.3f}")
    print(
        f" Nozzle exit diameter: {structure.nozzle_throat_diameter * np.sqrt(np.mean(ib_parameters.E_opt)) * 1e3:.3f} mm"
    )
    print(
        f" Average nozzle efficiency: {np.mean(ib_parameters.nozzle_eff) * 100:.3f} %"
    )

    print("\nROCKET BALLISTICS")
    print(f" Apogee: {np.max(ballistics.y):.2f} m")
    print(f" Max. velocity: {np.max(ballistics.v):.2f} m/s")
    print(f" Max. Mach number: {np.max(ballistics.Mach):.3f}")
    print(f" Max. acceleration: {np.max(ballistics.acc) / 9.81:.2f} gs")
    print(f" Time to apogee: {ballistics.apogee_time:.2f} s")
    print(f" Velocity out of the rail: {ballistics.v_rail:.2f} m/s")
    print(f" Height at motor burnout: {ballistics.y_burnout:.2f} m")
    print(
        f" Liftoff mass: {structure.motor_structural_mass + ib_parameters.m_prop[0] + rocket.mass_wo_motor:.3f} kg"
    )
    print(f" Flight time: {ballistics.flight_time:.2f} s")

    print("\nPRELIMINARY STRUCTURAL PROJECT")
    print(f" Casing safety factor: {structural_parameters.casing_sf:.2f}")
    print(
        f" Minimal nozzle convergent, divergent thickness: {structural_parameters.nozzle_conv_t * 1e3:.3f}, "
        f"{structural_parameters.nozzle_div_t * 1e3:.3f} mm"
    )
    print(
        f" Minimal bulkhead thickness: {structural_parameters.bulkhead_t * 1e3:.3f} mm"
    )
    print(
        f" Optimal number of screws: {structural_parameters.optimal_fasteners + 1:d}"
    )
    print(
        f" Shear, tear, compression screw safety factors: "
        f"{structural_parameters.shear_sf[structural_parameters.optimal_fasteners]:.3f}, "
        f"{structural_parameters.tear_sf[structural_parameters.optimal_fasteners]:.3f}, "
        f"{structural_parameters.compression_sf[structural_parameters.optimal_fasteners]:.3f}"
    )
    print("\nDISCLAIMER: values above shall not be the final dimensions.")
    print(
        "Critical dimensions shall be investigated in depth in order to guarantee safety."
    )

    print("\n")


def output_eng_csv(
    ib_parameters, structure, propellant, eng_res, dt, manufacturer, name
):
    """
    This program exports the motor data into three separate files.
    The .eng file is compatible with most rocket ballistic simulators such as openRocket and RASAero.
    The output .csv file contains thrust, time, propellant mass, Kn, chamber pressure, web thickness and burn rate data.
    The input .csv file contains all info used in the input section.
    """
    # Writing the ENG file:
    index = np.where(ib_parameters.t == ib_parameters.t_burnout)
    time = ib_parameters.t[: index[0][0]]
    thrust = ib_parameters.T[: index[0][0]]
    prop_vol = ib_parameters.V_prop[: index[0][0]]
    motor_to_eng(
        time,
        thrust,
        dt,
        prop_vol,
        structure.casing_outer_diameter,
        structure.chamber_length,
        eng_res,
        propellant.pp,
        structure.motor_structural_mass,
        manufacturer,
        name,
    )
    # Writing to output CSV file:
    motor_data = {
        "Time": time,
        "Thrust": thrust,
        "Prop_Mass": prop_vol * propellant.pp,
    }
    motor_data_df = pd.DataFrame(motor_data)
    motor_data_df.to_csv(f"output/{name}.csv", decimal=".")