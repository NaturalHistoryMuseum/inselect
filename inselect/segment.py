import cv2
import numpy as np
from skimage.feature.blob import blob_log
from skimage import io, color


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

    # compares contour area to bounding rectangle area
    fill_ratio = cv2.contourArea(contour) / (w * h)

    return ratio < 8 and w * h > area / 8E3 and (0.1 < fill_ratio < 0.9 or \
        (w < image_size[1] * 0.35 and h < image_size[0] * 0.35)) and \
        not (size_filter and
             (w > image_size[1] * 0.35 or h > image_size[0] * 0.35)) and \
        not ((w == image_size[0]) and h == image_size[1])


def process_contours(image, contours, hierarchy, index=0, size_filter=True):
    result = []
    while index >= 0:
        next, previous, child, parent = hierarchy[0][index]
        if right_sized(contours[index], image.shape, size_filter=size_filter):
            rect = cv2.boundingRect(contours[index])
            result.append(rect)
        else:
            if child != -1:
                rects = process_contours(image, contours, hierarchy, child,
                                         size_filter=size_filter)
                result.extend(rects)
        index = next
    return result

# def process_contours(image, contours, hierarchy, index=0, size_filter=True):
#     result = []
#     for contour in contours:
#         rect = cv2.boundingRect(contour)
#         x, y, w, h = rect
#         result.append(rect)
#     return result

def remove_lines(image):
    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    v_edges = cv2.Sobel(gray, cv2.CV_32F, 1, 0, None, 1)
    h_edges = cv2.Sobel(gray, cv2.CV_32F, 0, 1, None, 1)
    mag = np.abs(v_edges)
    mask = np.zeros(gray.shape, dtype=np.uint8)                                     
    threshold = 20
    mag2 = (255*mag/np.max(mag)).astype(np.uint8)
    _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
    contours, hierarchy = cv2.findContours(mag2.copy(),
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        _, _, w, h = cv2.boundingRect(contour)
        if h > image.shape[0] / 4 and w < 50:
            cv2.drawContours(mask, [contour], -1, 255, -1)
    mag = np.abs(h_edges)
    mag2 = (255*mag/np.max(mag)).astype(np.uint8)
    _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
    contours, hierarchy = cv2.findContours(mag2.copy(),
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        _, _, w, h = cv2.boundingRect(contour)
        if w > image.shape[1] / 4 and h < 50:
            cv2.drawContours(mask, [contour], -1, 255, -1)
    return mask

def segment_edges(image, window=None, threshold=12, return_contours=False,
                  variance_threshold=None, size_filter=1, line_filter=1):
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
    line_filter: Boolean
        Remove long line segment edges.

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
    if 0:
        v_edges = cv2.Sobel(gray, cv2.CV_32F, 1, 0, None, 1)
        h_edges = cv2.Sobel(gray, cv2.CV_32F, 0, 1, None, 1)
        mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        mag2 = (255*mag/np.max(mag)).astype(np.uint8)
        _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
    else:
        image2 = cv2.GaussianBlur(image, (3, 3), 3)
        lab_image = cv2.cvtColor(image2, cv2.cv.CV_BGR2Lab)
        threshold = 10 
        v_edges = cv2.Sobel(np.array(lab_image[:, :, 0]), cv2.CV_32F, 1, 0, None, 1)
        h_edges = cv2.Sobel(np.array(lab_image[:, :, 0]), cv2.CV_32F, 0, 1, None, 1)
        mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        mag0 = (255*mag/np.max(mag)).astype(np.uint8)
        threshold = 10 
        _, mag0 = cv2.threshold(mag0, threshold, 255, cv2.cv.CV_THRESH_BINARY)

        # v_edges = cv2.Sobel(gray, cv2.CV_32F, 1, 0, None, 1)
        # h_edges = cv2.Sobel(gray, cv2.CV_32F, 0, 1, None, 1)
        # mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        # mag1 = (255*mag/np.max(mag)).astype(np.uint8)
        # threshold = 12
        # _, mag1 = cv2.threshold(mag1, threshold, 255, cv2.cv.CV_THRESH_BINARY)

        # v_edges = cv2.Sobel(np.array(lab_image[:, :, 1]), cv2.CV_32F, 1, 0, None, 1)
        # h_edges = cv2.Sobel(np.array(lab_image[:, :, 1]), cv2.CV_32F, 0, 1, None, 1)
        # mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        # mag1 = (255*mag/np.max(mag)).astype(np.uint8)
        # threshold = 40 
        # _, mag1 = cv2.threshold(mag1, threshold, 255, cv2.cv.CV_THRESH_BINARY)

        v_edges = cv2.Sobel(np.array(lab_image[:, :, 2]), cv2.CV_32F, 1, 0, None, 1)
        h_edges = cv2.Sobel(np.array(lab_image[:, :, 2]), cv2.CV_32F, 0, 1, None, 1)
        mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        mag2 = (255*mag/np.max(mag)).astype(np.uint8)
        threshold = 40 
        _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
        # mag2 = mag0 | mag1 | mag2
        mag2 = mag0 | mag2 

    if line_filter:
        mask = remove_lines(image)
        mag2[mask == 255] = 0
    display = np.dstack((mag2, mag2, mag2))
    contours, hierarchy = cv2.findContours(mag2.copy(),
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)


    # contours2, hierarchy2 = cv2.findContours(mag2.copy(),
    #                                        cv2.RETR_LIST,
    #                                        cv2.CHAIN_APPROX_SIMPLE)
    # contour_areas = [(cv2.contourArea(contour), contour)
    #                  for contour in contours2]
    # contour_areas.sort(lambda a, b: cmp(b[0], a[0]))
    # contours2 = [c[1] for c in contour_areas]

    # display = np.zeros(gray.shape, dtype=np.uint8)
    # for contour in contours2:
    #     _, _, w, h = cv2.boundingRect(contour)
    #     ratio = cv2.contourArea(contour) / (w * h)
    #     if ratio < 0.9:
    #         cv2.drawContours(display, [contour], -1, 255, -1)
    # display = np.dstack((display, display, display))

    # dist_transform = cv2.distanceTransform(display, cv2.cv.CV_DIST_L2, 5)
    # ret, display = cv2.threshold(dist_transform, 0.1*dist_transform.max(), 255, 0)
    # display = dist_transform/np.max(display)*255
    # display = np.uint8(display)

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

    if return_contours:
        return rects, display, contours
    else:
        return rects, display


def segment_intensity(image, window=None):
    if window:
        subimage = np.array(image)
        x, y, w, h = window
        image = subimage[y:y + h, x:x + w]
    mask = remove_lines(image)
    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (25, 25), 9)
    # threshold = 255 * (gray < 150).astype(np.uint8)
    # threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 55, 0)
    (k, threshold) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
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

def segment_watershed(image):
    rects, display = segment_edges(image, size_filter=0)
    # rects, display = segment_edges(image, return_contours=True)
    # contour_areas = [(cv2.contourArea(rect[5]), rect)
    #              for rect in rects]
    # contour_areas.sort(lambda a, b: cmp(b[0], a[0]))
    # contours2 = [c[1] for c in contour_areas]
    h, w = image.shape[:2]
    initial = np.zeros((h, w), np.int32)
    for i, rect in enumerate(rects):
        cv2.drawContours(initial, [rect[4]], -1, 1, -1)

    for i, rect in enumerate(rects):
        regions = np.zeros(initial.shape, dtype=np.uint8)
        cv2.drawContours(regions, [rect[4]], -1, 2, -1)
        regions = cv2.erode(regions, None)
        markers = initial.copy()
        markers[regions == 2] = 2
        cv2.imshow("dis", markers.astype(np.uint8) * 128)
        cv2.waitKey(0)
        cv2.watershed(image, markers)
        im = image.copy()
        im[markers == 2] = [255, 0, 0]
        print markers

        cv2.imshow("dis", markers.astype(np.uint8))
        cv2.imshow("im", im)
        cv2.waitKey(0)


if __name__ == "__main__":
    # image = cv2.imread("../data/Plecoptera_Accession_Drawer_4.jpg")
    # image = image[0:1000, 0:3000, :]
    image = cv2.imread("../data/drawer.jpg")
    scaled = 0.5
    scaled = 1.0
    image = cv2.resize(image, (int(image.shape[1] * scaled),
                               int(image.shape[0] * scaled)))
    if 1:
        segment_watershed(image)
        while cv2.waitKey(0) != 27: pass
    elif 0:
        rects, display = segment_intensity(image)
        cv2.imshow("main", display)
        while cv2.waitKey(0) != 27: pass
    else:
        mask = remove_lines(image)
        # cv2.waitKey(0)
        image = cv2.GaussianBlur(image, (3, 3), 3)

        lab_image = cv2.cvtColor(image, cv2.cv.CV_BGR2Lab)

        v_edges = cv2.Sobel(np.array(lab_image[:, :, 0]), cv2.CV_32F, 1, 0, None, 1)
        h_edges = cv2.Sobel(np.array(lab_image[:, :, 0]), cv2.CV_32F, 0, 1, None, 1)

        mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        # print np.max(mag)
        mag0 = (255*mag/np.max(mag)).astype(np.uint8)
        # mag0 = mag.astype(np.uint8) 
        threshold = 10 
        _, mag0 = cv2.threshold(mag0, threshold, 255, cv2.cv.CV_THRESH_BINARY)

        # v_edges = cv2.Sobel(np.array(lab_image[:, :, 1]), cv2.CV_32F, 1, 0, None, 1)
        # h_edges = cv2.Sobel(np.array(lab_image[:, :, 1]), cv2.CV_32F, 0, 1, None, 1)
        # mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        # mag1 = (255*mag/np.max(mag)).astype(np.uint8)
        # threshold = 5 
        # _, mag1 = cv2.threshold(mag, threshold, 255, cv2.cv.CV_THRESH_BINARY)

        v_edges = cv2.Sobel(np.array(lab_image[:, :, 2]), cv2.CV_32F, 1, 0, None, 1)
        h_edges = cv2.Sobel(np.array(lab_image[:, :, 2]), cv2.CV_32F, 0, 1, None, 1)
        mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        mag2 = (255*mag/np.max(mag)).astype(np.uint8)
        threshold = 40 
        _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)
        # mag2 = mag0.astype(np.uint8) |  mag2.astype(np.uint8) |  mag1.astype(np.uint8)

        mag0[mask == 255] = 0
        mag2 = mag0 #| mag2 
        # mag2 = mag0 | mag1 | mag2

        cv2.imshow("im", image)
        cv2.imshow("edge", mag2)
        while cv2.waitKey(0) != 27: pass
        qwer

        v_edges = cv2.Sobel(gray, cv2.CV_32F, 1, 0, None, 1)
        h_edges = cv2.Sobel(gray, cv2.CV_32F, 0, 1, None, 1)
        mag = np.sqrt(v_edges ** 2 + h_edges ** 2)
        mag2 = (255*mag/np.max(mag)).astype(np.uint8)

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
