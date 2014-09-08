import cv2
import numpy as np
from skimage.feature.blob import blob_log


def segment_blobs(image):
    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    blobs = blob_log(gray, min_sigma=0.001, max_sigma=5)
    print blobs


def right_sized(contour, image_size, size_filter=True):
    x, y, w, h = cv2.boundingRect(contour)
    area = image_size[0] * image_size[1]
    if w > h:
        ratio = float(w) / h
    else:
        ratio = float(h) / w
    return ratio < 8 and w * h > area / 8E3 and \
        not (size_filter and
             (w > image_size[1] * 0.35 or h > image_size[0] * 0.35)) and \
        not ((w == image_size[0]) and h == image_size[1])


def process_contours(image, contours, hierarchy, index=0, size_filter=True):
    result = []
    while index >= 0:
        next, previous, child, parent = hierarchy[0][index]
        if right_sized(contours[index], image.shape, size_filter=size_filter):
            rect = cv2.boundingRect(contours[index])
            x, y, w, h = rect
            result.append(rect)
        else:
            if child != -1:
                rects = process_contours(image, contours, hierarchy, child,
                                         size_filter=size_filter)
                result.extend(rects)
        index = next
    return result


def segment_edges(image, window=None, threshold=12,
                  variance_threshold=None, size_filter=True):
    """Segments an image based on edge intensities.

    Parameters
    ----------
    image : (M, N, 3) array
        Image to process.
    window : tuple, (x, y, w, h)
        Optional subwindow in image.
    variance_threshold : float
        Color variance limit for detected regions.
    size_filter: Boolean
        Reject large objects.

    Returns
    -------
    (rects, display) : list, (M, N, 3) array
        Region results and visualization image.

    """
    if window:
        subimage = np.array(image)
        x, y, w, h = window
        image = subimage[y:y + h, x:x + w]

    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 3)
    display = gray.copy()
    v_edges = cv2.Sobel(gray, cv2.CV_32F, 1, 0, None, 1)
    h_edges = cv2.Sobel(gray, cv2.CV_32F, 0, 1, None, 1)
    mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
    mag2 = (255*mag/np.max(mag)).astype(np.uint8)
    _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
    display = np.dstack((mag2, mag2, mag2))

    contours, hierarchy = cv2.findContours(mag2.copy(),
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    contour_areas = [(cv2.contourArea(contour), contour)
                     for contour in contours]
    contour_areas.sort(lambda a, b: cmp(b[0], a[0]))
    _, mag2 = cv2.threshold(v_edges, 5, 255, cv2.cv.CV_THRESH_BINARY)
    mag2 = (255*mag2/np.max(mag2)).astype(np.uint8)

    rects = process_contours(display, contours, hierarchy,
                             size_filter=size_filter)
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

    return rects, display


def segment_intensity(image, window=None):
    if window:
        subimage = np.array(image)
        x, y, w, h = window
        image = subimage[y:y + h, x:x + w]
    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (25, 25), 9)
    threshold = 255 * (gray < 150).astype(np.uint8)
    contours, hierarchy = cv2.findContours(threshold.copy(),
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(c) for c in contours]
    if window:
        new_rects = []
        for rect in rects:
            dx = rect[2] / 2
            dy = rect[3] / 2
            new_rect = (rect[0] + x - dx, rect[1] + y - dy,
                        rect[2] + 2 * dx, rect[3] + 2 * dy)
            new_rects.append(new_rect)
        rects = new_rects
    display = np.dstack(3 * [threshold])
    return rects, display


if __name__ == "__main__":
    image = cv2.imread("../data/Plecoptera_Accession_Drawer_4.jpg")
    scaled = 0.5
    scaled = 1.0
    image = cv2.resize(image, (int(image.shape[1] * scaled),
                               int(image.shape[0] * scaled)))

    cv2.imshow("main", image)
    rects = segment_edges(image,
                          window=(100, 100, 2000, 2000),
                          threshold=12, size_filter=1)
    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    for rect in rects:
        im = gray[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
        print np.var(im)
        cv2.imshow("main", im)
        if cv2.waitKey(0) == 27:
            break

    # segment_blobs(image)
    while cv2.waitKey(0) != 27:
        pass
