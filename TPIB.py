import scipy.stats as stats
import numpy as np


def transformationPeakIterativeBaseline(x, y, x_left, x_right,
                                        numOfIteractions=10,
                                        peakIsPointingDown=False,
                                        normalizePeakArea=True):

    """
    Compute an iterative baseline for a transformation peak

    Returns the x- and y-coordinates of a transformation peak with
    subtracted baseline following the same algorithm developed by
    Reis and co-authors [1] [2]. Also returns an interpolated
    function of the peak.

    Parameters
    ----------
    x : 1-D array of floats or list of floats
        The x-coordinates of the peak. Must contain data before and after
        the peak.

    y : 1-D array of floats or list of floats
        The y-coordinates of the peak.

    x_left : tuple with two values (a, b)
        These are two values for the x-coordinate that are left and outside
        the peak. A linear regression will be done for all the x values
        that are between a and b.

    x_right : tuple with two values (c, d)
        These are two values for the x-coordinate that are located right and
        outside the peak. A linear regression will be done for all the x
        values that are between c and d.

    numOfIteractions : int
        Number of iteractions to perform for the baseline.

    peakIsPointingDown : boolean
        True if the peak is pointing down and False otherwise.

    normalizePeakArea : boolean
        If True then the final peak area will be normilazied to one.

    Returns
    -------
    x_final : 1-D array of floats
        The x-coordinates of the peak after the subtraction of the
        iterative baseline. Values in crescent order.

    y_final : 1-D array of floats
        The y-coordinates of the peak after the subtraction of the
        iterative baseline.

    peakFun : one parameter function
        This function takes one parameter (x) and returns an
        interpolated value of the y-coordinate of the peak. This
        may come in hand when integrating the peak or comparing
        with other peaks.

    References
    ----------

    [1] Reis, R.M.C.V. (2012). Assessments of viscous sintering
    models and determination of crystal growth rate and crystallized
    fraction in glasses. Ph.D. thesis. Universidade Federal de São Carlos.
    (in portuguese)


    [2] Reis, R.M.C.V., Fokin, V.M., and Zanotto, E.D. (2016). Determination
    of Crystal Growth Rates in Glasses Over a Temperature Range Using a
    Single DSC Run. Journal of the American Ceramic Society 99, 2001–2008.
    """

    def robustLinFun(x, y):
        slope, intercept, _, _ = stats.theilslopes(y, x)

        def linfun(x):
            return intercept + slope*x

        return linfun

    def lineEquation(xy1, xy2):
        x1 = xy1[0]
        x2 = xy2[0]
        y1 = xy1[1]
        y2 = xy2[1]
        m = (y1 - y2)/(x1 - x2)
        b = y1 - m*x1

        def fun(x):
            return m*x + b

        return fun

    # x must be in crescent order
    x, y = zip(*sorted(zip(x, y)))
    x = np.array(x)
    y = np.array(y)

    # Data is cut to the region of interest
    logic = np.logical_and(x >= x_left[0], x <= x_right[1])
    x, y = x[logic], y[logic]

    if peakIsPointingDown:
        y = y*-1

    # xM is the temperature where y is maximum
    xM = x[max(range(len(y)), key=y.__getitem__)]

    # Linear baselines functions
    bl_left = robustLinFun(x[x <= x_left[1]], y[x <= x_left[1]])
    bl_right = robustLinFun(x[x >= x_right[0]], y[x >= x_right[0]])

    # Find the start of the peak
    # The start of the peak must be below xM
    x_, y_ = x[x <= xM], y[x <= xM]
    x_, y_ = x_[::-1], y_[::-1]  # this reverses the list

    # For each (x,y) value from the peak maximum to the left ...
    for a, b in zip(x_, y_):
        # ... check if it crosses with the left linear baseline
        if b - bl_left(a) <= 0:
            # The point that crosses is the start of the peak
            x_start, y_start = a, b
            break

    # Find the end of the peak
    # The start of the peak must be below xM
    x_, y_ = x[x >= xM], y[x >= xM]

    # For each (x,y) value from the peak maximum to the right ...
    for a, b in zip(x_, y_):
        # ... check if it crosses with the left linear baseline
        if b - bl_right(a) <= 0:
            # The point that crosses is the start of the peak
            x_end, y_end = a, b
            break

    # Peak range
    logic = np.logical_and(x >= x_start, x <= x_end)
    x_peak, y_peak = x[logic], y[logic]

    # Iterative baseline
    firstBaseline = lineEquation([x_start, y_start], [x_end, y_end])
    baseline = firstBaseline(x_peak)

    # This is the iteractive method proposed in references [1] and [2]
    for n in range(numOfIteractions):
        area = np.trapz(y_peak - baseline, x_peak)
        bl = []

        for i in range(len(y_peak)):
            alpha = np.trapz(y_peak[:i] - baseline[:i], x_peak[:i])/area
            base = bl_left(x_peak[i])*(1-alpha) + bl_right(x_peak[i])*alpha
            bl.append(base)

        baseline = np.array(bl)

    # Final peak calculations
    x_final = x_peak
    y_final = y_peak - baseline

    if normalizePeakArea:
        peak_area = np.trapz(y_final, x_final)
        y_final = y_final/peak_area

    def peakFun(xval):
        return np.interp(xval, x_final, y_final, left=0, right=0)

    return x_final, y_final, peakFun
