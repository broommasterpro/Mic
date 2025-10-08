# Image encryption using chaotic and logistic maps
This project implements an image encryption scheme using the chaotic logistic map, inspired by research on how simple nonlinear dynamical equations can produce complex, unpredictable behavior.

It also illustrates how, when implemented digitally, the stable distribution of chaotic states can lead to potential weaknesses — providing insight into both the power and pitfalls of chaos-based cryptography.

### Overview
- Uses the logistic map to generate chaotic sequences.

- Applies these sequences for pixel permutation and diffusion.

- Saves all intermediate step images to visualize each transformation in the encryption process.

- Highlights how statistical regularities in chaotic outputs can reduce cryptographic security.

- Designed as a research and educational demo of chaos–encryption interaction.


## Results

| Original | Encrypted |
|:-----------:|:--------:|
| ![Original](assets/sample.png) | ![Encrypted](assets/encrypted_img.png) |



|X_key generation | CKS generation | Confusion 1 |
|:---------:|:------------:|:---------:|
| ![1](assets/1.bmp) | ![2](assets/2.bmp) | ![3](assets/3.bmp) |

| Diffusion 1 | Diffusion 2 | Confusion 2 |
|:--------------------:|:---------------------:|:----------------:|
| ![4](assets/4.bmp) | ![5](assets/5.bmp) | ![6](assets/6.bmp) |



## Dependencies
Run the following command to activate virtual environment and install all Dependencies:
```
source prepare.sh
```

NOTE: Executing the above script wouldn't work.
Please source it in current BASH instance.

## Usage
Encrypt an image:
```
python src/encrypt.py -i /path/to/img -x float(0 to 2pi) -y float(0 to 2pi) -K float(>18) -L int(11<L<1100)
```

Decrypt an image:
```
python src/decrypt.py /path/to/img
```
