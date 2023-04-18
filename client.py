import socket
import pickle
import numpy as np
import cv2

def zigzag(img)->list[int]:
    h, w = img.shape
    vector = []
    for i in range(h + w - 1):
        if i % 2 == 0:
            for j in range(max(0, i - h + 1), min(w, i + 1)):
                vector.append(img[i - j, j])
        else:
            for j in range(max(0, i - w + 1), min(h, i + 1)):
                vector.append(img[j, i - j])
    return vector

def rle(nums)->list[tuple]:
    res = []
    count = 0
    prev = nums[0]
    for num in nums:
        if num == prev:
            count += 1
        else:
            res.append([prev, count])
            count = 1
            prev = num
    res.append([prev, count])
    return np.array(res)

# Load image
img = cv2.imread('SampleImage.tif', cv2.IMREAD_GRAYSCALE)

## Transform
# Converting image into 8x8 blocks
blocks = [img[i:i+8, j:j+8] for i in range(0, img.shape[0], 8) for j in range(0, img.shape[1], 8)]

# Taking DCT of each block
dct_blocks = [cv2.dct(np.float32(block)) for block in blocks]

for L in range(8):
    # Quantization matrix
    Q = np.array([[1 if 0<=i<(L+1) and 0<=j<(L+1) else 0 for i in range(8)] for j in range(8)])

    # Quantizing each dct block
    dctq_blocks = [block*Q for block in dct_blocks]

    # Performing zigzag RLE of each dctq block
    rle_encoded_blocks = [rle(zigzag(block)) for block in dctq_blocks]

    ## Setting up the connection with server
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # connect the client to the server
    client_socket.connect((socket.gethostname(), 9999))

    # Serialize the image
    data = pickle.dumps(rle_encoded_blocks)
    
    # Transmitting the image
    client_socket.send(data)

    # Closing the connection
    client_socket.close()

    print("-> ", L+1, "Compressed image transmitted successfully!")