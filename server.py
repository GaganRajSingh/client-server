import socket
import pickle
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import os

def rev_rle(nums)->list:
    res = []
    for num in nums:
        res += [num[0]] * int(num[1])
    return np.array(res)

def rev_zz(nums):
    left = 0
    img = np.zeros((8, 8))
    h, w = img.shape
    for i in range(h + w - 1):
        if i % 2 == 0:
            for j in range(max(0, i - h + 1), min(w, i + 1)):
                img[i - j, j] = nums[left]
                left += 1
        else:
            for j in range(max(0, i - w + 1), min(h, i + 1)):
                img[j, i - j] = nums[left]
                left += 1
    return img

def reconstruct(blocks):
    image = np.zeros((256, 256))

    # Compute the number of blocks in each row/column
    blocks_per_row = 256 // 8

    # Reconstruct the image from the blocks
    for i, block in enumerate(blocks):
        row = i // blocks_per_row
        col = i % blocks_per_row
        image[row*8:(row+1)*8, col*8:(col+1)*8] = block

    return image

# Loading original image
og_image = np.array(cv2.imread('SampleImage.tif', cv2.IMREAD_GRAYSCALE))

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host and a port
server_socket.bind((socket.gethostname(), 9999))

# become a server socket
server_socket.listen()
print('Waiting for a client to connect...')

# Receiving the image
images = []
num_bytes = []

while True:
    
    client_socket, addr = server_socket.accept()
    print('Connection from: ', addr)
    
    image_bytes = b''
    bytes = 0
    while True:    
        msg = client_socket.recv(4096)
        if not msg:
            break
        image_bytes += msg
        bytes += len(msg)
    
    encoded_img = pickle.loads(image_bytes)
    
    print("Received the encoded image")
    images.append(encoded_img)
    num_bytes.append(bytes)
    if len(images) == 8:
        break

print("All images received")

client_socket.close()
server_socket.close()

x, y = [], []

## Decompressing all images
for i in range(8):
    
    # Perform reverse Run Length Encoding
    images[i] = [rev_rle(block) for block in images[i]]

    # Perform Inverse zig zag operation
    images[i] = [rev_zz(block) for block in images[i]]

    # Perform Inverse DCT on each block
    images[i] = [cv2.idct(block) for block in images[i]]

    # Merge the blocks back into a single image
    images[i] = reconstruct(images[i])

    x.append(i+1)
    y.append(mean_squared_error(og_image, images[i]))

# Making the images folder
if not os.path.exists('Images'):
    os.mkdir('Images')

# Saving each image
for i, image in enumerate(images):
    plt.imsave('./Images/image_L' + str(i+1) + '.png', image, cmap='gray')

## Displaying all decompressed images in one figure
# Create a 2x4 grid of subplots
fig, axes = plt.subplots(nrows=2, ncols=4)

# Display each image in a subplot
for i, ax in enumerate(axes.flat):
    ax.imshow(images[i], cmap='gray')
    ax.set_axis_off()
    ax.set_title(f"L = {i+1}")
plt.show()

## Generating graphs
# Mean Squared Error
plt.plot(x, y)
plt.title("Mean Squared Error")
plt.show()

# Number of bytes
plt.plot(x, num_bytes)
plt.title("Number of Bytes Transferred")
plt.show()