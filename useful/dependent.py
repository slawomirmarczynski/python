#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Obliczanie, metodą Monte Carlo, niepewności pomiarów pośrednich.

Do obliczania niepewności pomiarowej pomiarów pośrednich zwykle jest używana
albo metoda pochodnej logarytmicznej, albo metoda różniczki zupełnej (prawo
przenoszenia wariancji). Bardziej zaawansowaną, a co ciekawe obecnie łatwą
w użyciu, jest metoda Monte Carlo, której używa ten program. Choć tym razem
liczymy w nim niepewność określenia pola trójkąta za pomocą wzoru Herona,
to łatwo może być on przystosowany do obliczania niepewności w każdym innym
praktycznym problemie.

CC-BY-NC-ND 2024 Sławomir Marczyński
"""

import math
from functools import lru_cache

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm, t

N = 1000000


def mean_and_stddev(values):
    """
    Calculate the mean and standard deviation of a list of values.

    This function computes the arithmetic mean and the standard deviation
    of the given list of values. The standard deviation is calculated with
    Bessel's correction (ddof=1) and adjusted using the critical value from
    the Student's t-distribution for the number of observations.

    Args:
        values (list or array-like): A list or array of numerical values.

    Returns:
        tuple: A tuple containing the mean and the adjusted standard deviation.

    Example:
        >>> values = [1, 2, 3, 4, 5]
        >>> mean, stddev = mean_and_stddev(values)
        >>> print(f"Mean: {mean}, Standard Deviation: {stddev}")
        Mean: 3.0, Standard Deviation: 1.5811388300841898
    """

    # Number of elements in the 'values' list
    #
    n = len(values)

    # Calculating the arithmetic mean of the 'values' list
    #
    mean = np.mean(values)

    # Getting the critical value from the Student's t-distribution
    # for n - 1 observations.
    #
    t_coefficient = student_distribution_critical_value(n - 1)

    # Calculating the standard deviation with Bessel's correction (ddof=1).
    # Then dividing by the square root of the number of observations
    # and multiplying by the t coefficient.
    #
    deviation = np.std(values, ddof=1) / math.sqrt(n) * t_coefficient

    # Returning the mean and standard deviation
    #
    return mean, deviation


def gauss(x, x0, sigma):
    """
    Calculate the value of the Gaussian function (normal distribution).

    This function computes the value of the Gaussian function for a given
    x, with a specified center x0 and standard deviation sigma.

    Args:
        x (float or array-like): The input value(s) for which to calculate
            the Gaussian function.
        x0 (float): The center of the Gaussian distribution.
        sigma (float): The standard deviation of the Gaussian distribution.

    Returns:
        float or array-like: The value(s) of the Gaussian function
            at the given x.

    Example:
        >>> x = 0
        >>> x0 = 0
        >>> sigma = 1
        >>> result = gauss(x, x0, sigma)
        >>> print(result)
        0.3989422804014327
    """
    return 1.0 / np.sqrt(2.0 * np.pi) / sigma * np.exp(
        -(x - x0) ** 2 / 2.0 / sigma ** 2)


@lru_cache
def student_distribution_critical_value(
        degrees_of_freedom,
        confidence_level=(norm.cdf(1) - norm.cdf(-1))):
    """
    Student's t coefficient for the standard confidence level.

    The default confidence level is calculated on the fly and, as I checked,
    it was 0.6826894921370859  during the program test runs (last digit was
    inaccurate). This gives the significance level, i.e. alpha value, equal
    to 0.31731050786291415. See also Wolfram Alpha results for more digits:
    1/2 * (Erf((1)/Sqrt[2]) - Erf((-1)/Sqrt[2])) ==
    0.6826894921370858971704650912640758449558259334532087819747889004,
    1 - 1/2 * (Erf((1)/Sqrt[2]) - Erf((-1)/Sqrt[2])) ==
    0.3173105078629141028295349087359241550441740665467912180252110995.

    Args:
        degrees_of_freedom: number of degrees of freedom.
        confidence_level: confidence level beta.

    Returns:
        Student's t coefficient.
    """

    # Calculating the exact value of the significance level alpha for one
    # sigma, where sigma is the standard deviation of the normal distribution.
    #
    alpha_one_sigma = 1 - confidence_level  # significance level

    # Calculating the Student's t coefficient
    #
    t_value = t.ppf(1 - alpha_one_sigma / 2, degrees_of_freedom)
    t_value = float(t_value)  # convert np.float to plain vanilla float
    return t_value


def compute_triangle_area(a, b, c):
    """
    Calculate the area of a triangle using Heron's formula.

    This function computes the area of a triangle given the lengths of its
    three sides using Heron's formula.

    Args:
        a (float): The length of the first side of the triangle.
        b (float): The length of the second side of the triangle.
        c (float): The length of the third side of the triangle.

    Returns:
        float: The area of the triangle.

    Example:
        >>> a = 3
        >>> b = 4
        >>> c = 5
        >>> area = compute_triangle_area(a, b, c)
        >>> print(area)
        6.0
    """

    # Calculate the semi-perimeter of the triangle
    #
    p = (a + b + c) / 2

    # Calculate the area using Heron's formula
    #
    s = np.sqrt(p * (p - a) * (p - b) * (p - c))

    # Return the computed area
    #
    return s


def main():

    a_values = [10.00, 10.01, 10.03, 9.98, 10.02]
    b_values = [11.02, 10.99, 11.01, 11.01]
    c_values = [12.03, 12.03, 12.02, 12.04, 12.03, 12.01, 12.03]

    # Calculate the mean and standard deviation for each side of the triangle
    #
    a_mean, a_stddev = mean_and_stddev(a_values)
    b_mean, b_stddev = mean_and_stddev(b_values)
    c_mean, c_stddev = mean_and_stddev(c_values)

    # Generate random samples for each side based on the normal distribution
    #
    a = np.random.normal(a_mean, a_stddev, N)
    b = np.random.normal(b_mean, b_stddev, N)
    c = np.random.normal(c_mean, c_stddev, N)

    # Compute the area for each set of sides using the Monte Carlo method
    #
    s = compute_triangle_area(a, b, c)

    # Compute the area using the mean values of the sides
    #
    s_mean = compute_triangle_area(a_mean, b_mean, c_mean)

    # Calculate the mean and standard deviation of the areas
    # from the Monte Carlo simulation
    #
    s_monte_carlo_mean = np.mean(s)
    s_monte_carlo_stddev = np.std(s)

    # Print the means and standard deviations.
    # The format specifier after the colon (:) is used to format the number
    # .2f means floating-point number with 2 decimal places
    #
    print()
    print(f"bok a = {a_mean:.2f} ± {a_stddev:.2f} m")
    print(f"bok b = {b_mean:.2f} ± {b_stddev:.2f} m")
    print(f"bok c = {c_mean:.2f} ± {c_stddev:.2f} m")
    print()
    print(f"surface area = {s_mean:.3f} ± {s_monte_carlo_stddev:.3f} m²")
    print()

    # Create a figure and axis for the plot
    #
    fig, ax = plt.subplots()
    ax.minorticks_on()  # Enable minor ticks on the axis
    ax.grid(which='minor', linestyle="--")  # Set minor grid with dashed style
    ax.grid(which='major')  # Set major grid lines with default style
    plt.title("Oszacowanie niepewności")  # Set the title of the plot
    plt.xlabel("pole powierzchni trójkąta, metry")  # Set the x-axis label
    plt.ylabel("pdf")  # Set the y-axis label
    bins = 500 if N > 1000 else 50 if N > 100 else None
    ax.hist(s, bins=bins, density=True)  # Plot the histogram

    # Add text annotation with the mean and standard deviation
    #
    plt.text(0.05, 0.95,
             f"pole powierzchni trójkąta = {s_mean:.3f}"
             f" ± {s_monte_carlo_stddev:.3f} m²",
             fontsize=16,
             transform=ax.transAxes)

    # Define the number of points for the probability density function plot
    #
    M = 1000

    # Get the current x-axis limits. Create a linear space for the x-axis.
    # Calculate the Gaussian PDF values. Plot the PDF with a solid black line.
    lo, hi = ax.get_xlim()
    s_space = np.linspace(lo, hi, M)
    pd_values = gauss(s_space, s_monte_carlo_mean, s_monte_carlo_stddev)
    ax.plot(s_space, pd_values, 'k-')

    # Plot a solid line at the mean surface area.
    # Plot a dashed line at one stddev above/below the mean.
    #
    style = {'color': 'red', 'linestyle': '--'}
    ax.axvline(s_mean, color='red', linestyle='-')
    ax.axvline(s_monte_carlo_mean, **style)
    ax.axvline(s_monte_carlo_mean - s_monte_carlo_stddev, **style)
    ax.axvline(s_monte_carlo_mean + s_monte_carlo_stddev, **style)

    # Save the plot as an image file
    #
    plt.savefig("probability_density_function.png")

    # Display the plot
    #
    plt.show()


if __name__ == "__main__":
    main()
