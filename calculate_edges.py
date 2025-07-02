import numpy as np
from scipy.ndimage import zoom
import matplotlib.pyplot as plt
import cv2

def calculate_edges(coeffs, L=3):
    print(coeffs[0].imag.shape)
    print(coeffs[1].imag.shape)
    print(coeffs[2].imag.shape)

    target_height, target_width, orientation = coeffs[L-1].imag.shape
    resized_scales = []

    for i in range(L):
        array = coeffs[i].imag
        height, width, o = array.shape

        zoom_factors = (target_height / height, # Use bilinear interpolation to resize (H,W,O).
                        target_width / width, 
                        1)
        resized = zoom(array, zoom_factors, order=1)
        resized_scales.append(resized)
        

        """plt.figure(2, figsize=(10, 5))
        for i in range(6):
            plt.subplot(2, 3, i+1)
            plt.imshow(resized[:,:,i], cmap='viridis')
            plt.title(f'Imag. Highpass dir {i+1}')
            plt.axis('off')
        plt.show()"""
    
    interscale_product = np.ones((target_height, target_width, orientation))

    for r in range(L):
        interscale_product *= resized_scales[r]
        #print(interscale_product)
    print(interscale_product.shape)


    threshold = 0.02 * np.max(np.abs(interscale_product))
    edge_map_before = np.abs(interscale_product) > threshold  # shape: (H, W, 6)

    # Reference Wf (resized to match target resolution)
    Wf = zoom(coeffs[0].imag, (target_height / coeffs[0].shape[0],
                            target_width / coeffs[0].shape[1], 1), order=1)

    # Optional: normalize interscale product to match Wf magnitude
    mean_CL = np.mean(np.abs(interscale_product))
    mean_Wf = np.mean(np.abs(Wf))
    CL_rescaled = interscale_product / (mean_CL + 1e-8) * mean_Wf

    # Pixel-wise adaptive threshold
    edge_maps = np.abs(CL_rescaled) > np.abs(Wf)


    plt.figure(2, figsize=(10, 5))
    degrees = [15, 45, 75, 105, 135, 165]
    for i in range(6):
        plt.subplot(2, 3, i+1)
        plt.imshow(edge_maps[:,:,i], cmap='gray')
        plt.title(f'Imag. HP ({degrees[i]}°)')
        plt.axis('off')

    plt.show()

    combined_edge_map = np.any(edge_maps, axis=2)
    zoom_factors = (600 / target_height, 800 / target_width)
    edge_map = zoom(combined_edge_map.astype(float), zoom_factors, order=1)

    return edge_map, edge_maps


def add_label(image, label, font_scale=0.2, thickness=1):
    labeled = image.copy()
    cv2.putText(labeled, label, (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, (255,), thickness, lineType=cv2.LINE_AA)
    return labeled