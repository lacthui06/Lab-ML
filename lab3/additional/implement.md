Problem: Segment a given image into K clusters using the K-means algorithm
Dataset: You can use any image of your choice. For example, a natural image like a landscape or a portrait.
![alt text](image.png)

### Discussion: 4 Types of Image Segmentation
1. **Semantic Segmentation**: Classifies every pixel into a predefined category (e.g., sky, road, rock) without separating distinct object instances.
2. **Instance Segmentation**: Detects and delineates each individual object instance of interest separately (e.g., distinguishing "Rock 1" and "Rock 2").
3. **Panoptic Segmentation**: Integrates both semantic (class labels for background regions like sky/sea) and instance segmentation (separate labels for countable objects).
4. **Color-based / Clustering-based Segmentation**: Segments pixels purely on color similarity (using algorithms like K-Means) without any semantic object awareness.

### Discussion: Image Selection for K-Means Color Segmentation
* **Recommended Images (Good for K-Means)**:
  - High contrast with distinct, flat color regions (e.g., logos, cartoon art, simple objects on solid backgrounds).
  - Limited color palettes where the number of segments ($K$) is clear.
* **Not Recommended Images (Difficult for K-Means)**:
  - Smooth gradients (e.g., sunsets, smooth skies). K-Means creates hard boundaries (banding artifacts) because it partitions continuous gradients into discrete clusters.
  - Complex, noisy textures (e.g., leaves, sand). Since K-Means only clusters by color value (ignoring spatial pixel coordinates), it yields a noisy, speckled output.

Task:
1. Load the Image:
• Read the image using OpenCV or PIL.
• Convert the image to a suitable color space (e.g., RGB, HSV, or LAB).
2. Preprocess the Image:
• Resize the image to a smaller size for faster processing.
• Flatten the image into a 2D array of pixels, where each pixel is represented as a feature vector (e.g., RGB values).
3. Apply K-Means Clustering:
• Run K-Means with K ranging from 1 to 8.
• Plot the Elbow curve (Inertia vs K) to determine the optimal number of color segments.
• Initialize K random centroids, each representing the mean color of a cluster.
• Assign each pixel to the nearest centroid based on Euclidean distance.
• Update the centroids as the mean of the pixels assigned to each cluster.
• Repeat the assignment and update steps until convergence.
4. Segment the Image:
• Replace each pixel with the color of its assigned cluster centroid.
• Reshape the segmented image back to its original dimensions.
5. Visualize the Results:
• Display the original and segmented images side-by-side.
6. Practical Demo of the 4 Segmentation Types:
• Differentiate the 4 types of segmentation (Color-based, Semantic, Instance, Panoptic) by mapping K-Means clusters and labeling separate rock instances.