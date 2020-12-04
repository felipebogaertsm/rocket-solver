import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs


def motor_to_eng(t, F, dt, V_prop_CP, D_out, L_chamber, eng_res, pp, m_motor, manufacturer, name):
    """Exports an eng file to the directory 'outputs' inside the program folder. """

    # Forming a new time vector that has exactly 'eng_res' points (independent on time step input):
    t_out = np.linspace(0, t[-1] + dt, eng_res)
    # Interpolating old thrust-time data into new time vector:
    F_out = np.interp(t_out, t, F, left=0, right=0)
    # Interpolating the Propellant volume with the new time vector (to find propellant. mass with t):
    m_prop_out = pp * np.interp(t_out, t, V_prop_CP, right=0)

    # Writing to the ENG file:
    eng_header = f'{name} {D_out * 1e3:.4f} {L_chamber * 1e3:.4f} P ' \
        f'{m_prop_out[0]:.4f} {m_prop_out[0] + m_motor:.4f} {manufacturer}\n'
    saveFile = open(f'output/{name}.eng', 'w')
    saveFile.write(
        '; Generated by SRM Solver program written by Felipe Bogaerts de Mattos\n; Juiz de Fora, Brasil\n')
    saveFile.write(eng_header)
    for i in range(eng_res):
        saveFile.write('   %.2f %.0f\n' % ((t_out[i]), (F_out[i])))
    saveFile.write(';')
    saveFile.close()


def pressure_plot(t, P0):
    """ Returns plotly figure with pressure data. """
    data = [go.Scatter(x=t,
                       y=P0 * 1e-6,
                       mode='lines',
                       name='lines',
                       marker={'color': '#009933'}
                       )]
    layout = go.Layout(title='Pressure-time curve',
                       xaxis=dict(title='Time [s]'),
                       yaxis=dict(title='Pressure [MPa]'),
                       hovermode='closest')
    figure_plotly = go.Figure(data=data, layout=layout)
    figure_plotly.add_shape(
        type='line',
        x0=0,
        y0=np.mean(P0) * 1e-6,
        x1=t[-1],
        y1=np.mean(P0) * 1e-6,
        line={'color': '#ff0000', }
    )
    return figure_plotly


def thrust_plot(t, F):
    """ Returns plotly figure with pressure data. """
    data = [go.Scatter(x=t,
                       y=F,
                       mode='lines',
                       name='lines',
                       marker={'color': '#6a006a'}
                       )]
    layout = go.Layout(title='Thrust-time curve',
                       xaxis=dict(title='Time [s]'),
                       yaxis=dict(title='Pressure [MPa]'),
                       hovermode='closest')
    figure_plotly = go.Figure(data=data, layout=layout)
    figure_plotly.add_shape(
        type='line',
        x0=0,
        y0=np.mean(F),
        x1=t[-1],
        y1=np.mean(F),
        line={'color': '#ff0000', }
    )
    return figure_plotly


def height_plot(t, y):
    """ Returns plotly figure with altitude data. """
    data = [go.Scatter(x=t,
                       y=y,
                       mode='lines',
                       name='lines',
                       marker={'color': '#6a006a'}
                       )]
    layout = go.Layout(title='Altitude (AGL)',
                       xaxis=dict(title='Time [s]'),
                       yaxis=dict(title='Altitude [m]'),
                       hovermode='closest')
    figure_plotly = go.Figure(data=data, layout=layout)
    return figure_plotly


def velocity_plot(t, v):
    """ Returns plotly figure with velocity data. """
    data = [go.Scatter(x=t,
                       y=v,
                       mode='lines',
                       name='lines',
                       marker={'color': '#6a006a'}
                       )]
    layout = go.Layout(title='Velocity plot',
                       xaxis=dict(title='Time [s]'),
                       yaxis=dict(title='Velocity [m/s]'),
                       hovermode='closest')
    figure_plotly = go.Figure(data=data, layout=layout)
    return figure_plotly


def performance_plot(F, P0, t):
    """ Plots the chamber pressure and thrust in the same figure, saves to 'output' folder. """
    fig1, ax1 = plt.subplots()

    ax1.set_xlim(0, t[-1])
    ax1.set_ylim(0, 1.05 * np.max(F))
    ax1.set_ylabel('Thrust [N]', color='#6a006a')
    ax1.set_xlabel('Time [s]')
    ax1.grid(linestyle='-', linewidth='.4')
    ax1.plot(t, F, color='#6a006a', linewidth='1.5')
    ax1.tick_params(axis='y', labelcolor='k')

    ax2 = ax1.twinx()
    ax2.set_ylim(0, 1.15 * np.max(P0) * 1e-6)
    ax2.set_ylabel('Chamber Pressure [MPa]', color='#008141')
    ax2.plot(t, P0 * 1e-6, color='#008141', linewidth='1.5')
    ax2.tick_params(axis='y', labelcolor='k')

    fig1.tight_layout()
    fig1.set_size_inches(10, 7, forward=True)
    fig1.savefig('output/pressure_thrust.png', dpi=300)


def main_plot(t, F, P0, Kn, m_prop):
    """ Returns pyplot figure and saves motor plots to 'output' folder. """
    main_figure = plt.figure(3)
    main_figure.suptitle('Motor Data', size='xx-large')
    gs1 = gs.GridSpec(nrows=2, ncols=2)

    ax1 = plt.subplot(gs1[0, 0])
    ax1.set_ylabel('Thrust [N]')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylim(0, np.max(F) * 1.05)
    ax1.set_xlim(0, t[-1])
    ax1.grid(linestyle='-', linewidth='.4')
    ax1.plot(t, F, color='#6a006a', linewidth='1.5')

    ax2 = plt.subplot(gs1[0, 1])
    ax2.set_ylabel('Pressure [MPa]')
    ax2.yaxis.set_label_position('right')
    ax2.set_xlabel('Time [s]')
    ax2.set_ylim(0, np.max(P0) * 1e-6 * 1.05)
    ax2.set_xlim(0, t[-1])
    ax2.grid(linestyle='-', linewidth='.4')
    ax2.plot(t, P0 * 1e-6, color='#008141', linewidth='1.5')

    ax3 = plt.subplot(gs1[1, 0])
    ax3.set_ylabel('Klemmung')
    ax3.set_xlabel('Time [s]')
    ax3.set_ylim(0, np.max(Kn) * 1.05)
    ax3.set_xlim(0, t[-1])
    ax3.grid(linestyle='-', linewidth='.4')
    ax3.plot(t, Kn, color='b', linewidth='1.5')

    ax4 = plt.subplot(gs1[1, 1])
    ax4.set_ylabel('Propellant Mass [kg]')
    ax4.yaxis.set_label_position('right')
    ax4.set_xlabel('Time [s]')
    ax4.set_ylim(0, np.max(m_prop) * 1.05)
    ax4.set_xlim(0, t[-1])
    ax4.grid(linestyle='-', linewidth='.4')
    ax4.plot(t, m_prop, color='r', linewidth='1.5')

    main_figure.set_size_inches(12, 8, forward=True)
    main_figure.savefig('output/motor_plots.png', dpi=300)
    return main_figure


def mass_flux_plot(t, grain_mass_flux):
    """ Plots and saves figure of the mass flux for all the grain segments """
    N, index = grain_mass_flux.shape
    mass_flux_figure = plt.figure()
    for i in range(N):
        plt.plot(t, grain_mass_flux[i, :] * 1.42233e-3)
    plt.ylabel('Mass Flux [lb/s-in-in]')
    plt.xlabel('Time [s]')
    plt.ylim(0, np.max(grain_mass_flux) * 1.42233e-3 * 1.05)
    plt.xlim(0, t[-1])
    plt.grid(linestyle='-', linewidth='.4')
    mass_flux_figure.savefig('output/grain_mass_flux.png', dpi=300)
    return mass_flux_figure


def print_results(grain, structure, propellant, ib_parameters, structural_parameters):
    print('\nResults generated by SRM Solver program, by Felipe Bogaerts de Mattos')

    print('\nBURN REGRESSION')
    if ib_parameters.m_prop[0] > 1:
        print(f' Propellant initial mass {ib_parameters.m_prop[0]:.3f} kg')
    else:
        print(f' Propellant initial mass {ib_parameters.m_prop[0] * 1e3:.3f} g')
    print(' Mean Kn: %.2f' % np.mean(ib_parameters.Kn))
    print(f' Initial to final Kn ratio: {ib_parameters.initial_to_final_kn:.3f}')
    print(f' Volumetric efficiency: {(ib_parameters.V_prop[0] * 100 / ib_parameters.V_empty):.3f} %')
    print(f' Grain length for neutral profile vector: {ib_parameters.optimal_grain_length}')

    print(' Burn profile: ' + ib_parameters.burn_profile)
    print(f' Initial port-to-throat (grain #{grain.N:d}): {ib_parameters.initial_port_to_throat:.3f}')
    print(' Motor L/D ratio: %.3f' % (np.sum(grain.L_grain) / grain.D_grain))
    print(f' Max initial mass flux: {np.max(ib_parameters.grain_mass_flux):.3f} kg/s-m-m or '
          f'{np.max(ib_parameters.grain_mass_flux) * 1.42233e-3:.3f} lb/s-in-in')

    print('\nCHAMBER PRESSURE')
    print(f' Maximum, average chamber pressure: {(np.max(ib_parameters.P0) * 1e-6):.3f}, '
          f'{(np.mean(ib_parameters.P0) * 1e-6):.3f} MPa')

    print('\nTHRUST AND IMPULSE')
    print(f' Maximum, average thrust: {np.max(ib_parameters.F):.3f}, {np.mean(ib_parameters.F):.3f} N')
    print(f' Total, specific impulses: {ib_parameters.I_total:.3f} N-s, {ib_parameters.I_sp:.3f} s')
    print(f' Burnout time, thrust time: {ib_parameters.t_burnout:.3f}, {ib_parameters.t[-1]:.3f} s')

    print('\nNOZZLE DESIGN')
    print(f' Average opt. exp. ratio: {np.mean(ib_parameters.E):.3f}')
    print(f' Nozzle exit diameter: {structure.D_throat * np.sqrt(np.mean(ib_parameters.E)) * 1e3:.3f} mm')
    print(f' Average nozzle efficiency: {np.mean(ib_parameters.n_cf) * 100:.3f} %')

    print('\nPRELIMINARY STRUCTURAL PROJECT')
    print(f' Casing safety factor: {structural_parameters.casing_sf:.2f}')
    print(f' Minimal nozzle convergent, divergent thickness: {structural_parameters.nozzle_conv_t * 1e3:.3f}, '
          f'{structural_parameters.nozzle_div_t * 1e3:.3f} mm')
    print(f' Minimal bulkhead thickness: {structural_parameters.bulkhead_t * 1e3:.3f} mm')
    print(f' Optimal number of screws: {structural_parameters.optimal_fasteners + 1:d}')
    print(f' Shear, tear, compression screw safety factors: '
          f'{structural_parameters.shear_sf[structural_parameters.optimal_fasteners]:.3f}, '
          f'{structural_parameters.tear_sf[structural_parameters.optimal_fasteners]:.3f}, '
          f'{structural_parameters.compression_sf[structural_parameters.optimal_fasteners]:.3f}')
    print('\nDISCLAIMER: values above shall not be the final dimensions.')
    print('Critical dimensions shall be investigated in depth in order to guarantee safety.')

    print('\n')


def output_eng_csv(ib_parameters, structure, propellant, eng_res, dt, manufacturer, name):
    """
    This program exports the motor data into three separate files.
    The .eng file is compatible with most rocket ballistic simulators such as openRocket and RASAero.
    The output .csv file contains thrust, time, propellant mass, Kn, chamber pressure, web thickness and burn rate data.
    The input .csv file contains all info used in the input section.
    """
    # Writing the ENG file:
    motor_to_eng(ib_parameters.t, ib_parameters.F, dt, ib_parameters.V_prop, structure.D_out,
                 structure.L_chamber, eng_res, propellant.pp, structure.m_motor, manufacturer, name)
    # Writing to output CSV file:
    motor_data = {'Time': ib_parameters.t, 'Thrust': ib_parameters.F, 'Prop_Mass': ib_parameters.m_prop}
    motor_data_df = pd.DataFrame(motor_data)
    motor_data_df.to_csv(f'output/{name}.csv', decimal='.')
