from random import randint

from .utils import debug_print

# Warning: lazy load of cv2 and numpy via local imports

# TODO LH Decide on use of skimage's watershed
# Breaks pyinstaller build
# from skimage.morphology import watershed
USE_OPENCV_WATERSHED = True


def _right_sized(contour, image, container_filter=True, size_filter=True):
    """Checks if contour size and shape is that of an object of interest.

    Parameters
    ----------
    contour : cv2.Contour
        Contour to be analysed.
    image_size : tuple
        Dimensions of operating image.
    container_filter : boolean
        Filters with simple heuristic for container contours. These are
        contours containing other segments such as insect cabinet subdivisions.
    size_filter : boolean
        Filters large objects.

    Returns
    -------
    result : boolean
        Object is of correct sizing.
    """
    import cv2

    image_size = image.shape
    x, y, w, h = cv2.boundingRect(contour)
    area = image_size[0] * image_size[1]
    if w > h:
        ratio = float(w) / h
    else:
        ratio = float(h) / w

    # compares contour area to bounding rectangle area
    fill_ratio = cv2.contourArea(contour) / (w * h)
    # filter very long narrow objects and small objects
    is_right_shape = ratio < 8 and w * h > area / 8E3
    # filter to remove containers that are a) large and b) contains
    # too much or too little contour area in bounding box
    is_container = (not 0.1 < fill_ratio < 0.8 and
                    (w > image_size[1] * 0.35 or
                     h > image_size[0] * 0.35))
    is_too_large = (w > image_size[1] * 0.85 and h > image_size[0] * 0.85)
    debug = False
    if debug and (w > image_size[1] * 0.35 or h > image_size[0] * 0.35):
        debug_print(w, h, fill_ratio, is_container)
        cv2.imshow('im', image[y:y+h, x:x+w])
        cv2.waitKey(0)

    return is_right_shape and not (container_filter and is_container) and \
        not (size_filter and is_too_large)


def _process_contours(image, contours, hierarchy, callback, index=0,
                      size_filter=True):
    """Traverse a hierachy of contours (contours containing contours) and
    returns bounding boxes of the smallest possible objects that still remain
    of interest.

    Parameters
    ----------
    image : ndarray
        Operating image.
    contours : list of cv2.Contour
        List of contours.
    hierarchy : ndarray
        Hierarchy of contours.
    callback: Callable
        A callable that will be called at regular intervals.
    index : int
        Start of contour index.
    size_filter : boolean
        Filters large objects.
    """
    import cv2

    result = []
    while index >= 0:
        callback()
        next, previous, child, parent = hierarchy[0][index]
        if _right_sized(contours[index], image, size_filter=size_filter):
            rect = cv2.boundingRect(contours[index])
            rect += (contours[index],)
            result.append(rect)
        else:
            if child != -1:
                rects = _process_contours(image, contours, hierarchy,
                                          callback, index=child,
                                          size_filter=size_filter)
                result.extend(rects)
        index = next
    return result


# alternate process, may be useful if we abandon hierarchical contours later
def _process_contours_iterate(image, contours, hierarchy, index=0,
                              size_filter=True):
    import cv2

    result = []
    for contour in contours:
        if right_sized(contour, image.shape, size_filter=size_filter):
            rect = cv2.boundingRect(contour)
            rect += (contour,)
            result.append(rect)
    return result


def remove_lines(image):
    """Removes long horizontal and vertical edges. Operates on the vertical and
    horizontal sobel images.

    Parameters
    ----------
    image : (M, N, 3) array
        Operating image.

    Returns
    -------
    mask : (M, N) array
        Mask of image without lines.
    """
    import cv2
    import numpy as np

    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    v_edges = cv2.Sobel(gray, cv2.CV_32F, 1, 0, None, 1)
    h_edges = cv2.Sobel(gray, cv2.CV_32F, 0, 1, None, 1)
    mag = np.abs(v_edges)
    mask = np.zeros(gray.shape, dtype=np.uint8)
    # set line width as 20th of the average image width-height
    linewidth = ((image.shape[0] + image.shape[1]) / 2) / 20
    threshold = 20
    mag2 = (255*mag/np.max(mag)).astype(np.uint8)
    _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
    contours, hierarchy = cv2.findContours(mag2.copy(),
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        _, _, w, h = cv2.boundingRect(contour)
        if h > image.shape[0] / 4 and w < linewidth:
            cv2.drawContours(mask, [contour], -1, 255, -1)
    mag = np.abs(h_edges)
    mag2 = (255*mag/np.max(mag)).astype(np.uint8)
    _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
    contours, hierarchy = cv2.findContours(mag2.copy(),
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        _, _, w, h = cv2.boundingRect(contour)
        if w > image.shape[1] / 4 and h < linewidth:
            cv2.drawContours(mask, [contour], -1, 255, -1)
    return mask


# Values passed to segment_edges() before iss102 reorganisation
# variance_threshold=100, resize=(5000, 5000), size_filter=1, line_filter=1
def segment_edges(image, window=None, threshold=12, lab_based=True,
                  variance_threshold=100, resize=False, size_filter=1,
                  line_filter=1, callback=None):
    """Segments an image based on edge intensities.

    Parameters
    ----------
    image : (M, N, 3) array
        Image to process.
    window : tuple, (x, y, w, h)
        Optional subwindow in image.
    lab_based: boolean
        Considers edges in the LAB colour space, else in the gray scale.
    variance_threshold : float
        Color variance limit for detected regions.
    size_filter: Boolean
        Reject large objects.
    line_filter: Boolean
        Remove long line segment edges.
    callback: Callable or None
        If given, should be a callable that takes no arguments. It will be
        polled at regular intervals.

    Returns
    -------
    (rects, display) : list, (M, N, 3) array
        Region results and visualization image.
    """
    import cv2
    import numpy as np

    if not callback:
        def swallow(*args, **kwargs):
            pass
        callback = swallow

    callback('Preparing to segment')

    if window:
        subimage = np.array(image)
        x, y, w, h = window
        image = subimage[y:y + h, x:x + w]

    original_height, original_width = image.shape[:2]
    if resize:
        image = cv2.resize(image, resize)

    callback()

    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 3)
    display = gray.copy()
    if not lab_based:
        v_edges = cv2.Sobel(gray, cv2.CV_32F, 1, 0, None, 1)
        h_edges = cv2.Sobel(gray, cv2.CV_32F, 0, 1, None, 1)
        mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        mag2 = (255*mag/np.max(mag)).astype(np.uint8)
        _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
    else:
        image2 = cv2.GaussianBlur(image, (3, 3), 3)
        lab_image = cv2.cvtColor(image2, cv2.cv.CV_BGR2Lab)
        # L component

        callback()

        channel = np.array(lab_image[:, :, 0])
        v_edges = cv2.Sobel(channel, cv2.CV_32F, 1, 0, None, 1)
        h_edges = cv2.Sobel(channel, cv2.CV_32F, 0, 1, None, 1)
        mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        mag0 = (255*mag/np.max(mag)).astype(np.uint8)
        threshold = 10

        callback()

        _, mag0 = cv2.threshold(mag0, threshold, 255, cv2.cv.CV_THRESH_BINARY)
        # B component
        channel = np.array(lab_image[:, :, 2])
        v_edges = cv2.Sobel(channel, cv2.CV_32F, 1, 0, None, 1)
        h_edges = cv2.Sobel(channel, cv2.CV_32F, 0, 1, None, 1)

        callback()

        mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        mag2 = (255*mag/np.max(mag)).astype(np.uint8)
        threshold = 40
        _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
        mag2 = mag0 | mag2
    if line_filter:
        mask = remove_lines(image)
        mag2[mask == 255] = 0

    callback('Detecting contours')

    display = np.dstack((mag2, mag2, mag2))
    contours, hierarchy = cv2.findContours(mag2.copy(),
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    callback('Processing contours')

    rects = _process_contours(display, contours, hierarchy,
                              callback, size_filter=size_filter)

    callback()

    if variance_threshold:
        new_rects = []
        for rect in rects:
            im = gray[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
            if np.var(im) > variance_threshold:
                new_rects.append(rect)
        rects = new_rects
    if window:
        new_rects = []
        for rect in rects:
            new_rect = (rect[0] + x, rect[1] + y, rect[2], rect[3])
            new_rects.append(new_rect)
        rects = new_rects

    if resize:
        display = cv2.resize(display, (original_width, original_height))
        new_rects = []
        for rect in rects:
            fx = float(original_width) / resize[0]
            fy = float(original_height) / resize[1]
            new_rect = (rect[0] * fx, rect[1] * fy, rect[2] * fx, rect[3] * fy)
            new_rects.append(new_rect)
        rects = new_rects

    # Reverse order so that boxes at the top left are towards the start
    # and boxes at the bottom right are towards the end
    # TODO LH This is crummy - need a way to order rects
    rects = list(reversed(rects))

    return rects, display


def segment_intensity(image, window=None):
    import cv2
    import numpy as np

    if window:
        subimage = np.array(image)
        x, y, w, h = window
        image = subimage[y:y + h, x:x + w]
    mask = remove_lines(image)
    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (25, 25), 9)
    (k, threshold) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV |
                                   cv2.THRESH_OTSU)
    threshold[mask == 255] = 0
    contours, hierarchy = cv2.findContours(threshold.copy(),
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(c) for c in contours]
    if window:
        new_rects = []
        for rect in rects:
            dx = rect[2] / 2
            dy = rect[3] / 2
            dx, dy = 0, 0
            new_rect = (rect[0] + x - dx, rect[1] + y - dy,
                        rect[2] + 2 * dx, rect[3] + 2 * dy)
            new_rects.append(new_rect)
        rects = new_rects
    display = np.dstack(3 * [threshold])
    return rects, display


def segment_grabcut(image, window=None, seeds=[]):
    """Segments an image using grabcut technique. Initialised with edges.

    Parameters
    ----------
    image : (M, N, 3) array
        Image to process.
    window : tuple, (x, y, w, h)
        Optional subwindow in image.

    Returns
    -------
    (rects, display) : list, (M, N, 3) array
        Region results and visualization image.
    """
    import cv2
    import numpy as np

    if window:
        subimage = np.array(image)
        x, y, w, h = window
        image = subimage[y:y + h, x:x + w]
    rects, display = segment_edges(image, variance_threshold=100,
                                   line_filter=0, size_filter=0)
    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    (k, mag0) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV |
                              cv2.THRESH_OTSU)

    h, w = image.shape[:2]
    initial = np.zeros((h, w), np.uint8)
    initial[:] = cv2.GC_BGD
    initial[mag0 == 255] = cv2.GC_FGD
    for i, rect in enumerate(rects):
        cv2.drawContours(initial, [rect[4]], -1, int(cv2.GC_FGD), -1)

    initial[display[:, :, 0] > 0] = cv2.GC_PR_FGD
    bgmodel = np.zeros((1, 65), np.float64)
    fgmodel = np.zeros((1, 65), np.float64)
    mask = initial
    rect = None
    cv2.grabCut(image, mask, rect, bgmodel, fgmodel, 1, cv2.GC_INIT_WITH_MASK)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    contours, hierarchy = cv2.findContours(mask2.copy(),
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(c) for c in contours]

    display = np.dstack(3 * [255 * mask2.astype(np.uint8)])
    if seeds:
        distance = cv2.distanceTransform(mask2, cv2.cv.CV_DIST_L2, 3)
        markers = np.zeros(mask2.shape, dtype=np.int32)
        markers[mask2 == 0] = 255
        for i, seed in enumerate(seeds):
            sx, sy = seed
            markers[sy, sx] = i + 1
        if USE_OPENCV_WATERSHED:
            cv2.watershed(display, markers)
        else:
            markers = watershed(mask2, markers, mask=mask2)
        new_rects = []
        for i, seed in enumerate(seeds):
            mask = np.array(markers == i + 1, dtype=np.uint8)
            contours, _ = cv2.findContours(mask,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                contours.sort(lambda x, y:
                              cmp(cv2.contourArea(y), cv2.contourArea(x)))
                new_rects.append(cv2.boundingRect(contours[0]))
                colour = [randint(100, 255), randint(100, 255), 0]
                cv2.drawContours(display, [contours[0]], -1, colour, -1)
        rects = new_rects
    if window:
        new_rects = []
        gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
        for rect in rects:
            dx, dy = 0, 0
            new_rect = (rect[0] + x - dx, rect[1] + y - dy,
                        rect[2] + 2 * dx, rect[3] + 2 * dy)

            im = gray[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
            if np.var(im) > 200 and rect[2] * rect[3] > w * h / 4E3:
                new_rects.append(new_rect)
        rects = new_rects
    return rects, display


def segment_watershed(image, window=None):
    """Segments an image using watershed technique.

    Parameters
    ----------
    image : (M, N, 3) array
        Image to process.
    window : tuple, (x, y, w, h)
        Optional subwindow in image.

    Returns
    -------
    (rects, display) : list, (M, N, 3) array
        Region results and visualization image.
    """
    import cv2
    import numpy as np

    if window:
        subimage = np.array(image)
        x, y, w, h = window
        image = subimage[y:y + h, x:x + w]
    rects, display = segment_edges(image, variance_threshold=100,
                                   size_filter=0)
    h, w = image.shape[:2]
    initial = np.zeros((h, w), np.int32)
    for i, rect in enumerate(rects):
        cv2.drawContours(initial, [rect[4]], -1, 1, -1)
    display = np.zeros(initial.shape, dtype=np.uint8)

    segment_rects = []
    for i, rect in enumerate(rects):
        regions = np.zeros(initial.shape, dtype=np.uint8)
        cv2.drawContours(regions, [rect[4]], -1, 2, -1)
        regions = cv2.erode(regions, None)
        regions = cv2.erode(regions, None)
        markers = initial.copy()
        markers[regions == 2] = 2
        cv2.watershed(image, markers)
        display[markers == 2] = 255
        contours, hierarchy = cv2.findContours(regions.copy(),
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        segment_rects.extend([cv2.boundingRect(c) for c in contours])

    if window:
        new_rects = []
        for rect in segment_rects:
            dx, dy = 0, 0
            new_rect = (rect[0] + x - dx, rect[1] + y - dy,
                        rect[2] + 2 * dx, rect[3] + 2 * dy)
            new_rects.append(new_rect)
        segment_rects = new_rects
    return segment_rects, np.dstack(3 * [display])


if __name__ == "__main__":
    import cv2
    import numpy as np

    image = cv2.imread("../../data/drawer.jpg")
    scaled = 1.0
    image = cv2.resize(image, (int(image.shape[1] * scaled),
                               int(image.shape[0] * scaled)))
    test_grabcut = False
    if test_grabcut:
        seeds = [[800, 400], [820, 740], [830, 840], [630, 240], [560, 270]]
        rects, display = segment_grabcut(image, seeds=seeds)
        display = np.array(display[:, :, 0])
        display = cv2.distanceTransform(display, cv2.cv.CV_DIST_L2, 5)
        cv2.imshow("disp", (display).astype(np.uint8))
    else:
        rects, display = segment_edges(image,
                                       window=None,
                                       resize=(5000, 5000),
                                       variance_threshold=100,
                                       size_filter=1)
        cv2.imshow("disp", (display).astype(np.uint8))

    while cv2.waitKey(0) != 27:
        pass
