import os


def get_corners(x1, y1, x2, y2):
    """Given two diagonally opposite corners of a box, return the top left and
    bottom right corners

    Parameters
    ----------
    x1 : float
    y1 : float
    x2 : float
    y2 : float

    Returns
    -------
    tuple
    """
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return (x1, y1), (x2, y2)


def unique_file_name(path, base, suffix):
    """Return a unique file name by using numerical suffixes

    Parameters
    ----------
    path : str
        Path to create the file in
    base : str
        Base file name
    suffix : str
        File name suffix

    Returns
    -------
    str
        A unique file name, with the path prepended and suffix appended
    """
    base_name = os.path.join(path, base)
    file_name = base_name + suffix
    if os.path.exists(file_name):
        count = 1
        while os.path.exists(base_name + "-" + str(count) + suffix):
            count += 1
        file_name = base_name + "-" + str(count) + suffix
    return file_name