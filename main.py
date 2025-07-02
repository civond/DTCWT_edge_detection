from dtcwt import Transform2d
from skimage.feature import canny
import cv2
import matplotlib.pyplot as plt
from calculate_edges import *

# The 6 orientation within the DTCWT are roughly: 15, 45, 75, 105, 135, 165 degrees
path = "./figures/lines.jpg"
img = cv2.imread(path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape)


# Perform 3-level Dual Tree Complex Wavelet Transform
transform = Transform2d()
coeffs = transform.forward(img, nlevels=3)
edge_map, wavelet_edge_maps = calculate_edges(coeffs.highpasses)

edge_map_canny = canny(edge_map, sigma=1.0)
original_canny = canny(img, sigma=1.0)


edge_map = cv2.normalize(np.abs(edge_map), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
edge_map_canny = (edge_map_canny.astype(np.uint8)) * 255
original_canny = (original_canny.astype(np.uint8)) * 255

# Add image labels
img = add_label(img, "original")
edge_map  = add_label(edge_map,  "wavelet edge detection")
edge_map_canny   = add_label(edge_map_canny,   "wavelet canny")
original_canny   = add_label(original_canny,   "original canny")

# Merge images and save
top_row = np.hstack((img, edge_map))
bottom_row = np.hstack((original_canny, edge_map_canny))
merged = np.vstack((top_row, bottom_row))
cv2.imwrite("merged.jpg", merged)

# edge map
degrees = [15, 45, 75, 105, 135, 165]
edge_map1 = wavelet_edge_maps[:,:,0].astype(np.uint8) * 255
edge_map2 = wavelet_edge_maps[:,:,1].astype(np.uint8) * 255
edge_map3 = wavelet_edge_maps[:,:,2].astype(np.uint8) * 255
edge_map4 = wavelet_edge_maps[:,:,3].astype(np.uint8) * 255
edge_map5 = wavelet_edge_maps[:,:,4].astype(np.uint8) * 255
edge_map6 = wavelet_edge_maps[:,:,5].astype(np.uint8) * 255

edge_map1 = add_label(edge_map1, f"{degrees[0]} degrees")
edge_map2 = add_label(edge_map2, f"{degrees[1]} degrees")
edge_map3 = add_label(edge_map3, f"{degrees[2]} degrees")
edge_map4 = add_label(edge_map4, f"{degrees[3]} degrees")
edge_map5 = add_label(edge_map5, f"{degrees[4]} degrees")
edge_map6 = add_label(edge_map6, f"{degrees[5]} degrees")

top_row = np.hstack((edge_map1, edge_map1, edge_map3))
bottom_row = np.hstack((edge_map4, edge_map5, edge_map6))
merged = np.vstack((top_row, bottom_row))
cv2.imwrite("merged2.jpg", merged)


"""plt.figure(2, figsize=(10, 5))
    for i in range(6):
        plt.subplot(2, 3, i+1)
        plt.imshow(edge_maps[:,:,i], cmap='gray')
        plt.title(f'Imag. Highpass dir {i+1}')
        plt.axis('off')

    plt.show()"""