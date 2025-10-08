from PIL import Image
import numpy as np
import pickle
import sys

image_path = sys.argv[1]


png_image = Image.open(image_path)
png_image.save('enc_image.bmp')

img = Image.open('enc_image.bmp')

img = img.convert("RGB")
confusion_2_matrix = np.array(img, dtype=np.uint8)
print("Arr shape:", confusion_2_matrix.shape)

M=confusion_2_matrix.shape[0]
N=confusion_2_matrix.shape[1]

from math import pi



class Secret:
    def __init__(self, x_0, y_0, K, L, pixel_seed):
        self.x_0 = x_0
        self.y_0 = y_0
        self.K = K
        self.L = L
        self.pixel_seed = pixel_seed

with open("secret.key", "rb") as f:
    s = pickle.load(f)

x_0= s.x_0
y_0= s.y_0
K=s.K
L=s.L

confusion_seed_pixel = s.pixel_seed




x_key=np.array(
    [
        np.floor(256*x_0/(2*pi)),
        np.floor(256*y_0/(2*pi)),
        np.floor(K%256),
        L%256
    ]
  )

XKey_img = np.zeros((M, N, 3), dtype=np.uint8)
print(M, N)

for i in range(M):
    for j in range(N):
        k = (i*N) + j
        XKey_img[i,j,0]=x_key[(3*k) % 4]
        XKey_img[i,j,1]=x_key[(3*k + 1) % 4]
        XKey_img[i,j,2]=x_key[(3*k + 2) % 4]

img = Image.fromarray(XKey_img)
img.save("XKey_img.bmp")

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
img.save("CKS.bmp")

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
img.save("diffusion_2_revert_matrix.bmp")

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
img.save("diffusion_revert_matrix.bmp")

"""# **CONFUSION-I REVERSAL**"""

confusion_revert_matrix = np.zeros((M, N, 3), dtype=np.uint8)

#confusion_seed_pixel = np.load("confusion_seed_pixel.npy")

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
img.save("confusion_revert_matrix.bmp")
"""# **ARR REVERSAL**"""

arr_revert_matrix = np.zeros((M, N, 3), dtype=np.uint8)

for k in range(M*N - 1):
  i = k//N
  j = (k%N)
  arr_revert_matrix[i,j,0] = confusion_revert_matrix[i, j, 0] ^ XKey_img[i, j, 0]
  arr_revert_matrix[i,j,1] = confusion_revert_matrix[i, j, 1] ^ XKey_img[i, j, 1]
  arr_revert_matrix[i,j,2] = confusion_revert_matrix[i, j, 2] ^ XKey_img[i, j, 2]

img = Image.fromarray(arr_revert_matrix)
img.save("arr_revert_matrix.bmp")
img.save("decrypted_img.png")
