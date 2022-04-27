from math import sqrt, atan2, degrees
from scipy.signal import butter,filtfilt


def pix_from_deg(h, d, res, size_in_deg, verbose=False):
    '''Obtain pixels from visual degrees.
    Parameters:
    h: Monitor height in cm
    d: Distance between monitor and participant in cm
    r: Vertical resolution of the monitor
    size_in_deg: The stimulus size in degrees
    verbose: If true, print information about the results

    Returns:
    size_in_px: Size of the stimuli in pixels.
    '''
    # Calculate the number of degrees that correspond to a single pixel. This will
    # generally be a very small value, something like 0.03.
    deg_per_px = degrees(atan2(.5 * h, d)) / (.5 * res)
    if verbose: print('%s degrees correspond to a single pixel' % deg_per_px)
    # Calculate the size of the stimulus in degrees
    size_in_px = size_in_deg / deg_per_px
    if verbose: print('The size of the stimulus is %s pixels and %s visual degrees' \
                      % (size_in_px, size_in_deg))
    return size_in_px


def deg_from_pix(h, d, res, size_in_px, verbose=False):
    '''Obtain visual degrees from pixels.
    Parameters:
    h: Monitor height in cm
    d: Distance between monitor and participant in cm
    r: Vertical resolution of the monitor
    size_in_deg: The stimulus size in degrees
    verbose: If true, print information about the results

    Returns:
    size_in_px: Size of the stimuli in pixels.
    '''
    # Calculate the number of degrees that correspond to a single pixel. This will
    # generally be a very small value, something like 0.03.
    deg_per_px = degrees(atan2(.5 * h, d)) / (.5 * res)
    if verbose: print('%s degrees correspond to a single pixel' % deg_per_px)
    # Calculate the size of the stimulus in degrees
    size_in_deg = size_in_px * deg_per_px
    if verbose: print('The size of the stimulus is %s pixels and %s visual degrees' \
                      % (size_in_px, size_in_deg))
    return size_in_deg


def butter_lowpass_filter(data, cutoff=1.2, fs=30, order=2):
    '''Returns the result of the filtering of the input data.
    Parameters:
    data: The data to be filtered
    cutoff: The cutoff frequency
    fs: The sample rate
    order: the order of the filter'''
    nyq = 0.5 * fs  # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y