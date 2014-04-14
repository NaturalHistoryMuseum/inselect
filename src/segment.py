import cv2
import numpy as np
from sklearn import cluster
import skimage
from skimage.feature.blob import blob_dog, blob_log

def segment_blobs(image):
    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    blobs = blob_log(gray, min_sigma=0.001, max_sigma=5)
    print blobs


def right_sized(contour, image_size, size_filter=True):
    x, y, w, h = cv2.boundingRect(contour)
    area = image_size[0] * image_size[1]
    if w > h:
        ratio = float(w) / h;
    else:
        ratio = float(h) / w
    return ratio < 8 and w * h > area / 8E3 and \
        not (size_filter and (w > image_size[1] * 0.35 or h > image_size[0] * 0.35) ) and \
        not ((w == image_size[0]) and h == image_size[1]) 


def process_contours(image, contours, hierarchy, index=0, size_filter=True):
    result = []
    while index >= 0:
        # print index
        next, previous, child, parent = hierarchy[0][index]
        if right_sized(contours[index], image.shape, size_filter=size_filter):
            # print 'draw'
            color = 230 
            cv2.drawContours(image, contours, index, color, -1, cv2.CV_AA, hierarchy, -1)
            rect = cv2.boundingRect(contours[index])
            x, y, w, h = rect
            cv2.rectangle(image, (x, y), (x + w, y + h), 0)
            result.append(rect)
        else:
            if child != -1:
                rects = process_contours(image, contours, hierarchy, child, size_filter=size_filter)
                result.extend(rects)
        index = next
    return result


def segment_edges(image, window=None, threshold=10, variance_threshold=None, size_filter=True):
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
    # element = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
    # element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # mag2 = cv2.erode(mag,element)
    mag2 = (255*mag/np.max(mag)).astype(np.uint8)
    _, mag2 = cv2.threshold(mag2, threshold, 255, cv2.cv.CV_THRESH_BINARY)

    contours, hierarchy = cv2.findContours(mag2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours0, hierarchy = cv2.findContours( mag2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

    contour_areas = [(cv2.contourArea(contour), contour) for contour in contours]
    contour_areas.sort(lambda a, b: cmp(b[0], a[0]))
    # cv2.drawContours(vis, contours, -1, (255,0,255), -1, cv2.CV_AA, hierarchy, 1 )
    # vis = cv2.erode(vis, element)
    # cv2.imshow("vis", vis)
    # for area, contour in contour_areas:
    #     print area 
    #     cv2.waitKey(0)
    #     cv2.drawContours(vis, [contour], 0, (0, 255, 0), 3, cv2.CV_AA)
    #     cv2.imshow("vis", vis)
    # rect = cv2.boundingRect(contour_areas[1][1])
    # for contour in contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     if w * h > 200 and not (w > 700 or h > 700) and not (w < 10 or h < 10):
    #         cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0))

    rects = process_contours(display, contours, hierarchy, size_filter=size_filter)
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

    # image[:,:,2] = display

    # print visited.shape
    # for hcontours in hierarchy:

    #     print hcontours
    #     for contour in hcontours:
    #         print contour
    #         cv2.drawContours(vis, contour, -1, (255, 255, 255), -1, cv2.CV_AA)

    #         if right_sized(contours):
    #             cv2.drawContours(vis, contour, -1, (255, 255, 255), -1, cv2.CV_AA)
    #             break
    # cv2.imshow("vis", image) 
    # cv2.waitKey(0)

    # vis[:, :, 0] = mag/100
    # cv2.drawContours(vis, contours, -1, (255,255,255), 2, cv2.CV_AA, hierarchy, 8)
    # focus = mag2[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    # focus = cv2.erode(focus ,element)

    # focus_vis = vis[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2], :]
    # Y, X = np.mgrid[0:focus.shape[0], 0:focus.shape[1]]
    # Y = Y[focus == 255]
    # X = X[focus == 255]
    # init_points = [(98, 7), (413, 20), (500, 54), (494, 244), (432, 267), (381, 302), (157, 315), 
    #     (253, 71), (400, 138), (252, 239), (103, 163)]
    # init_points = [(253, 71), (400, 138), (252, 239), (103, 163)]
    # init_arr = np.vstack([[x[1] for x in init_points], [x[0] for x in init_points]]).T
    # # kmeans = cluster.MiniBatchKMeans(n_clusters=11, max_iter=100, init=init_arr)
    # kmeans = cluster.MiniBatchKMeans(n_clusters=5, max_iter=500, init=init_arr)
    # K = np.vstack([X, Y]).T
    # labels = kmeans.fit(K).labels_
    # N = labels.max()
    # # Display all clusters
    # cols = [(100,100,100), (100,0,0), (0,100,0), (0,0,100), (0,100,100), (0, 50, 100), (100,50,0), (50,50,0),
    #     (50, 100, 0), (200, 200, 200), (200, 0, 0), (200, 200, 0)]
    # for i in range(N):
    #     mask = (labels == i)
    #     focus_vis[Y[mask], X[mask], :] = cols[i] 
    # cv2.imshow('focus', focus_vis)
    # cv2.imshow('vis', vis)
    # cv2.imshow('vis2', image)
    return rects

def segment_intensity(image, window=None):
    if window:
        subimage = np.array(image)
        x, y, w, h = window
        image = subimage[y:y + h, x:x + w]
    gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (25, 25), 9) 
    threshold = 255 * (gray < 150).astype(np.uint8)
    # cv2.imshow("main", gray)
    # cv2.imshow("threshold", threshold)
    # cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(c) for c in contours]
    if window:
        new_rects = []
        for rect in rects:
            new_rect = (rect[0] + x, rect[1] + y, rect[2], rect[3])
            new_rects.append(new_rect)
        rects = new_rects 
    return rects

if __name__ == "__main__":
    image = cv2.imread("../data/Plecoptera_Accession_Drawer_4.jpg")

    image = cv2.imread("../data/drawer.jpg")
    # image = image[250:image.shape[1]-500, 280:image.shape[0]-100]
    scaled = 0.5
    scaled = 1.0 
    image = cv2.resize(image, (int(image.shape[1] * scaled), int(image.shape[0] * scaled)))

    cv2.imshow("main", image)
    # rects = segment_edges(image, window=(100, 100, 100, 100), size_filter=False)
    # rects = segment_intensity(image, window=(100, 100, 100, 100))
    rects = segment_intensity(image)
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