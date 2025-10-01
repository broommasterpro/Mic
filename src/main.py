
from PIL import Image
import numpy as np

image_path = "/sample.png"


png_image = Image.open(image_path)
png_image.save('/output_image.bmp')

img = Image.open('/output_image.bmp')
img = img.convert("RGB")

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('/output_image.bmp')
plt.imshow(img)
plt.axis('off')
plt.show()

arr = np.array(img, dtype=np.uint8)
print("Arr shape:", arr.shape)
print("Arr dtype:", arr.dtype)

M=arr.shape[0]
N=arr.shape[1]

from math import pi

x_0=4
y_0= 4
K=83642643
L=1000

x_key=np.array(
    [
        np.floor(256*x_0/(2*pi)),
        np.floor(256*y_0/(2*pi)),
        np.floor(K%256),
        L%256
    ]
  )
x_key

XKey_img = np.zeros((M, N, 3), dtype=np.uint8)
print(M, N)

for i in range(M):
    for j in range(N):
        k = (i*N) + j
        XKey_img[i,j,0]=x_key[(3*k) % 4]
        XKey_img[i,j,1]=x_key[(3*k + 1) % 4]
        XKey_img[i,j,2]=x_key[(3*k + 2) % 4]

img = Image.fromarray(XKey_img)
img.save("/XKey_img.bmp")

img = mpimg.imread("/XKey_img.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()

from math import sin

def st_map(x_arg, y_arg):
  return (x_arg+(K*sin(y_arg)))%(2*pi), (y_arg + x_arg + K*sin(y_arg))%(2*pi)

x_0_dash, y_0_dash = 0, 0

for i in range(L):
  x_0_dash, y_0_dash=st_map(x_0, y_0)

chaotic_states=np.zeros((M*N, 2))

chaotic_states[0, 0] = x_0_dash
chaotic_states[0, 1] = y_0_dash

x_0_dash_new, y_0_dash_new = x_0_dash, y_0_dash

for i in range(1, M*N):
  x_0_dash_new, y_0_dash_new = st_map(x_0_dash_new, y_0_dash_new)
  chaotic_states[i, 0]=x_0_dash_new
  chaotic_states[i, 1]=y_0_dash_new

chaotic_states

def logistic_map(x_arg):
  return 4*x_arg*(1-x_arg)

logistic_states=np.zeros(M*N)

z_0 = (x_0_dash + y_0_dash)%1
z_0_dash = z_0
for i in range(L):
  z_0_dash = logistic_map(z_0_dash)

logistic_states[0]=z_0_dash

for i in range(1, M*N):
  logistic_states[i] = logistic_map(logistic_states[i-1])

logistic_states

CKS = np.zeros((M, N, 3), dtype=np.uint8)

def CKSR(k):
  return np.floor(256*chaotic_states[k-1, 0])/(2*pi)

def CKSG(k):
  return np.floor(256*chaotic_states[k-1, 1])/(2*pi)

def CKSB(k):
  return np.floor(256*logistic_states[k-1])

for i in range(M):
  for j in range(N):
    k = (i*N) + j + 1
    CKS[i,j,0]=CKSR(k)
    CKS[i,j,1]=CKSG(k)
    CKS[i,j,2]=CKSB(k)

img = Image.fromarray(CKS)  # no 'RGB' argument needed
img.save("/CKS.bmp")

img = mpimg.imread("/CKS.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()

"""
# All the encryption steps go below.

# **Confusion I**
"""

confusion_matrix = np.zeros((M, N, 3), dtype=np.uint8)

for k in range(M*N - 1):
  i = k//N
  j = (k%N)
  confusion_matrix[i,j,0] = arr[i, j, 0] ^ XKey_img[i, j, 0]
  confusion_matrix[i,j,1] = arr[i, j, 1] ^ XKey_img[i, j, 1]
  confusion_matrix[i,j,2] = arr[i, j, 2] ^ XKey_img[i, j, 2]

img = Image.fromarray(confusion_matrix)
img.save("/confusion_matrix.bmp")

img = mpimg.imread("/confusion_matrix.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()

"""# **Diffusion I**"""

diffusion_matrix = np.zeros((M, N, 3), dtype=np.uint8)

confusion_seed_pixel = confusion_matrix[0,0]

for k in range(1, M*N):
  i = k//N
  j = (k%N)
  i_dash = (k-1)//N
  j_dash = ((k-1)%N)
  diffusion_matrix[i_dash,j_dash,0] = confusion_matrix[i,j,0] ^ confusion_matrix[i_dash,j_dash,0]
  diffusion_matrix[i_dash,j_dash,1] = confusion_matrix[i,j,1] ^ confusion_matrix[i_dash,j_dash,1]
  diffusion_matrix[i_dash,j_dash,2] = confusion_matrix[i,j,2] ^ confusion_matrix[i_dash,j_dash,2]

img = Image.fromarray(diffusion_matrix)
img.save("/diffusion_matrix.bmp")

img = mpimg.imread("/diffusion_matrix.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()

"""# **DIFFUSION-II**

"""

diffusion_2_matrix = np.zeros((M, N, 3), dtype=np.uint8)
for k in range(M*N - 2, -1, -1):
  i =(k)%M
  j= ((k)//M)
  i_dash = (k+1)%M
  j_dash = ((k+1)//M)
  diffusion_2_matrix[i,j,0] = diffusion_matrix[i,j,0] ^ diffusion_2_matrix[i_dash,j_dash,1] ^ diffusion_2_matrix[i_dash,j_dash,2]
  diffusion_2_matrix[i,j,1] = diffusion_matrix[i,j,1] ^ diffusion_2_matrix[i_dash,j_dash,2] ^ diffusion_2_matrix[i_dash,j_dash,0]
  diffusion_2_matrix[i,j,2] = diffusion_matrix[i,j,2] ^ diffusion_2_matrix[i_dash,j_dash,0] ^ diffusion_2_matrix[i_dash,j_dash,1]

img = Image.fromarray(diffusion_2_matrix)
img.save("/diffusion_2_matrix.bmp")

img = mpimg.imread("/diffusion_2_matrix.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()

"""# **CONFUSION-II**"""

confusion_2_matrix = np.zeros((M, N, 3), dtype=np.uint8)
for k in range(0, M*N):
  i =(k)//N
  j= ((k)%N)
  confusion_2_matrix[i,j,0] = diffusion_2_matrix[i,j,0] ^ CKS[i,j,0]
  confusion_2_matrix[i,j,1] = diffusion_2_matrix[i,j,1] ^ CKS[i,j,1]
  confusion_2_matrix[i,j,2] = diffusion_2_matrix[i,j,2] ^ CKS[i,j,2]

img = Image.fromarray(confusion_2_matrix)
img.save("/confusion_2_matrix.bmp")

img.save("/encrypted_img.png")

img = mpimg.imread("/confusion_2_matrix.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()

"""# **Decryption Steps**

## **DIFFUSION-II REVERSAL**
"""

diffusion_2_revert_matrix = np.zeros((M, N, 3), dtype=np.uint8)
for k in range(0, M*N):
  i =(k)//N
  j= ((k)%N)
  diffusion_2_revert_matrix[i,j,0] = confusion_2_matrix[i,j,0] ^ CKS[i,j,0]
  diffusion_2_revert_matrix[i,j,1] = confusion_2_matrix[i,j,1] ^ CKS[i,j,1]
  diffusion_2_revert_matrix[i,j,2] = confusion_2_matrix[i,j,2] ^ CKS[i,j,2]

img = Image.fromarray(diffusion_2_revert_matrix)
img.save("/diffusion_2_revert_matrix.bmp")

img = mpimg.imread("/diffusion_2_revert_matrix.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()

"""# **DIFFUSION-1 REVERSAL**"""

diffusion_revert_matrix = np.zeros((M, N, 3), dtype=np.uint8)
for k in range(M*N - 2, -1, -1):
  i =(k)%M
  j= ((k)//M)
  i_dash = (k+1)%M
  j_dash = ((k+1)//M)
  diffusion_revert_matrix[i,j,0] = diffusion_2_revert_matrix[i,j,0] ^ diffusion_2_revert_matrix[i_dash,j_dash,1] ^ diffusion_2_revert_matrix[i_dash,j_dash,2]
  diffusion_revert_matrix[i,j,1] = diffusion_2_revert_matrix[i,j,1] ^ diffusion_2_revert_matrix[i_dash,j_dash,2] ^ diffusion_2_revert_matrix[i_dash,j_dash,0]
  diffusion_revert_matrix[i,j,2] = diffusion_2_revert_matrix[i,j,2] ^ diffusion_2_revert_matrix[i_dash,j_dash,0] ^ diffusion_2_revert_matrix[i_dash,j_dash,1]

img = Image.fromarray(diffusion_revert_matrix)
img.save("/diffusion_revert_matrix.bmp")

img = mpimg.imread("/diffusion_revert_matrix.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()

"""# **CONFUSION-I REVERSAL**"""

confusion_revert_matrix = np.zeros((M, N, 3), dtype=np.uint8)
confusion_revert_matrix[0, 0] = confusion_seed_pixel

for k in range(1, M * N):
  i = k // N
  j = k % N
  i_dash = (k - 1) // N
  j_dash = (k - 1) % N
  confusion_revert_matrix[i, j, 0] = diffusion_revert_matrix[i_dash, j_dash, 0] ^ confusion_revert_matrix[i_dash, j_dash, 0]
  confusion_revert_matrix[i, j, 1] = diffusion_revert_matrix[i_dash, j_dash, 1] ^ confusion_revert_matrix[i_dash, j_dash, 1]
  confusion_revert_matrix[i, j, 2] = diffusion_revert_matrix[i_dash, j_dash, 2] ^ confusion_revert_matrix[i_dash, j_dash, 2]

img = Image.fromarray(confusion_revert_matrix)
img.save("/confusion_revert_matrix.bmp")

img = mpimg.imread("/confusion_revert_matrix.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()

"""# **ARR REVERSAL**"""

arr_revert_matrix = np.zeros((M, N, 3), dtype=np.uint8)

for k in range(M*N - 1):
  i = k//N
  j = (k%N)
  arr_revert_matrix[i,j,0] = confusion_revert_matrix[i, j, 0] ^ XKey_img[i, j, 0]
  arr_revert_matrix[i,j,1] = confusion_revert_matrix[i, j, 1] ^ XKey_img[i, j, 1]
  arr_revert_matrix[i,j,2] = confusion_revert_matrix[i, j, 2] ^ XKey_img[i, j, 2]

img = Image.fromarray(arr_revert_matrix)
img.save("/arr_revert_matrix.bmp")

img = mpimg.imread("/arr_revert_matrix.bmp")
plt.imshow(img)
plt.axis('off')
plt.show()
