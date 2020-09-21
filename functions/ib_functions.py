import numpy as np


# Internal Ballistics related functions:


def getBurnProfile(A_burn: list):
    if A_burn[0] / A_burn[-1] > 1.02:
        burn_profile = 'Regressive'
    elif A_burn[0] / A_burn[-1] < 0.98:
        burn_profile = 'Progressive'
    else:
        burn_profile = 'Neutral'
    return burn_profile


class BATES:
    def __init__(self, wr: int, N: int, D_grain: float, D_core: np.array, L_grain: np.array):
        self.wr = wr
        self.N = N
        self.D_grain = D_grain
        self.D_core = D_core
        self.L_grain = L_grain

    def minCoreDiamIndex(self):
        """ Finds the smallest core diameter and its index 'j' """
        N, D_core = self.N, self.D_core
        D_core_min = np.amin(D_core)
        # If there is more than one one index where the initial core diameter is minimal, the for loop
        # only returns the first index where it happens.
        for j in range(N):
            if D_core[j] == D_core_min:
                D_core_min_index = j
                break
        return D_core_min_index

    def burnArea(self, x: float, j: int):
        """ Calculates the BATES burn area given the web distance and segment number """
        wr, N, D_grain, D_core, L_grain = self.wr, self.N, self.D_grain, self.D_core, self.L_grain
        Ab = np.pi * (((D_grain ** 2) - (D_core[j] + 2 * x) ** 2) / 2 + (L_grain[j] - 2 * x) * (D_core[j] + 2 * x))
        return Ab

    def grainVolume(self, x: float, j: int):
        """ Calculates the BATES grain volume given the web distance and segment number """
        wr, N, D_grain, D_core, L_grain = self.wr, self.N, self.D_grain, self.D_core, self.L_grain
        Vp = (np.pi / 4) * (((D_grain ** 2) - ((D_core[j] + 2 * x) ** 2)) * (L_grain[j] - 2 * x))
        return Vp

    def web(self):
        """ Returns the web thickness array for each grain"""

        # Finding the web thickness of each individual grain. The j index refers to the grain segment and i
        # refers to the web step (number of steps set by 'wr').
        wr, N, D_grain, D_core, L_grain = self.wr, self.N, self.D_grain, self.D_core, self.L_grain
        w = np.zeros((N, wr))
        for j in range(N):
            if 0.5 * (D_grain - D_core[j]) > L_grain[j]:
                w[j] = np.linspace(0, (L_grain[j] / 2), wr)
            elif 0.5 * (D_grain - D_core[j]) <= L_grain[j]:
                w[j] = np.linspace(0, 0.5 * (D_grain - D_core[j]), wr)
        return w

    def optimalLength(self):
        """ Returns the optimal length for each of the input grains """
        optimal_grain_length = 1e3 * 0.5 * (3 * self.D_grain + self.D_core)
        return optimal_grain_length

    def massFluxPerGrain(self, r: float, pp, x):
        """ Returns a numpy multidimensional array with the mass flux for each grain """
        grain_mass_flux = np.zeros((self.N, np.size(x)))
        grain_mass_flow = np.zeros((self.N, np.size(x)))
        accumulated_grain_Ab = np.zeros((self.N, np.size(x)))
        for j in range(self.N):
            for i in range(np.size(r)):
                for k in range(j + 1):
                    # print(j, i, k)
                    accumulated_grain_Ab[j, i] = accumulated_grain_Ab[j, i] + self.burnArea(x[i], k)
                grain_mass_flow[j, i] = (accumulated_grain_Ab[j, i] * pp * r[i])
                grain_mass_flux[j, i] = (grain_mass_flow[j, i]) / circle_area(self.D_core[j] + x[i])
        return grain_mass_flux


def CP_Seidel(P0: float, Pe: float, Ab: float, V0: float, At: float, pp: float,
              k: float, R: float, T0: float, r: float):
    """ Calculates the chamber pressure by solving Hans Seidel's differential equation """
    P_critical_ratio = (2 / (k + 1)) ** (k / (k - 1))
    if Pe / P0 <= P_critical_ratio:
        H = ((k / (k + 1)) ** 0.5) * ((2 / (k + 1)) ** (1 / (k - 1)))
    else:
        H = ((Pe / P0) ** (1 / k)) * (((k / (k - 1)) * (1 - (Pe / P0) ** ((k - 1) / k))) ** 0.5)
    dP0dt = ((R * T0 * Ab * pp * r) - (P0 * At * H * ((2 * R * T0) ** 0.5))) / V0
    return dP0dt


def circle_area(diameter: float):
    Area = np.pi * 0.25 * diameter ** 2
    return Area


def chamber_volume(L_cc: float, D_in: float, V_prop: np.array):
    """ Returns the instant and empty chamber volume for each web distance value """
    V_empty = np.pi * L_cc * (D_in ** 2) / 4
    V0 = V_empty - V_prop
    return V0, V_empty


def thrust_coefficient(P0, P_external, k_ex, n_cf):
    """ Returns value for thrust coefficient based on the chamber pressure and correction factor """
    Pr = P_external / P0
    Cf_ideal = np.sqrt(
        ((2 * k_ex ** 2) / (k_ex - 1)) * ((2 / (k_ex + 1)) **
                                        ((k_ex + 1) / (k_ex - 1))) * (1 - Pr ** ((k_ex - 1) / k_ex)))
    Cf = Cf_ideal * n_cf
    return Cf


def impulse(F_avg, t, m_prop):
    I_total = F_avg * t[-1]
    I_sp = I_total / (m_prop[0] * 9.81)
    return I_total, I_sp


def operational_correction_factors(P0: list, Pe: float, P0psi: list, Isp_frozen: float, Isp_shifting: float,
                                   E: float, Dt: float, qsi: float, index: int, critical_pressure_ratio: float,
                                   C1: float, C2: float, V0: float, M: float, t: list):
    """ Returns kinetic, two-phase and boundary layer correction factors based on a015140 """
    C7, termC2, E_cf = np.zeros(index), np.zeros(index), np.zeros(index)
    n_cf, n_kin, n_bl, n_tp = np.zeros(index), np.zeros(index), np.zeros(index), np.zeros(index)

    for i in range(index):

        # Kinetic losses
        if P0psi[i] >= 200:
            n_kin[i] = 33.3 * 200 * (Isp_frozen / Isp_shifting) / P0psi[i]
        else:
            n_kin[i] = 0

        # Boundary layer and two phase flow losses
        if Pe / P0[i] <= critical_pressure_ratio:

            termC2[i] = 1 + 2 * np.exp(-C2 * (P0psi[i]) ** 0.8 * t[i] / ((Dt / 0.0254) ** 0.2))
            E_cf[i] = 1 + 0.016 * E[i] ** -9
            n_bl[i] = C1 * ((P0psi[i] ** 0.8) / ((Dt / 0.0254) ** 0.2)) * (termC2[i]) * E_cf[i]

            C7[i] = 0.454 * (P0psi[i] ** 0.33) * ((qsi) ** 0.33) * (
                    1 - np.exp(-0.004 * (V0[1] / circle_area(Dt)) / 0.0254) * (1 + 0.045 * Dt / 0.0254))
            if 1 / M >= 0.9:
                C4 = 0.5
                if Dt / 0.0254 < 1:
                    C3, C5, C6 = 9, 1, 1
                elif 1 <= Dt / 0.0254 < 2:
                    C3, C5, C6 = 9, 1, 0.8
                elif Dt / 0.0254 >= 2:
                    if C7[i] < 4:
                        C3, C5, C6 = 13.4, 0.8, 0.8
                    elif 4 <= C7[i] <= 8:
                        C3, C5, C6 = 10.2, 0.8, 0.4
                    elif C7[i] > 8:
                        C3, C5, C6 = 7.58, 0.8, 0.33
            elif 1 / M < 0.9:
                C4 = 1
                if Dt / 0.0245 < 1:
                    C3, C5, C6 = 44.5, 0.8, 0.8
                elif 1 <= Dt / 0.0254 < 2:
                    C3, C5, C6 = 30.4, 0.8, 0.4
                elif Dt / 0.0254 >= 2:
                    if C7[i] < 4:
                        C3, C5, C6 = 44.5, 0.8, 0.8
                    elif 4 <= C7[i] <= 8:
                        C3, C5, C6 = 30.4, 0.8, 0.4
                    elif C7[i] > 8:
                        C3, C5, C6 = 25.2, 0.8, 0.33
            n_tp[i] = C3 * ((qsi * C4 * C7[i] ** C5) / (P0psi[i] ** 0.15 * E[i] ** 0.08 *
                                                        (Dt / 0.0254) ** C6))
        else:
            n_tp[i] = 0
            n_bl[i] = 0
    return n_kin, n_tp, n_bl


def expansion_ratio(Pe: float, P0: list, k: float, index: int, critical_pressure_ratio: float):
    """ Returns array of the optimal expansion ratio for each pressure ratio """
    E = np.zeros(index)

    for i in range(index):
        if Pe / P0[i] <= critical_pressure_ratio:
            pressure_ratio = Pe / P0[i]
            E[i] = (((k + 1) / 2) ** (1 / (k - 1)) * pressure_ratio ** (1 / k) * (
                    (k + 1) / (k - 1) * (1 - pressure_ratio ** (
                    (k - 1) / k))) ** 0.5) ** -1
        else:
            E[i] = 1
    return E
