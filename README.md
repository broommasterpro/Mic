# chaotic_logistic_img_encryption
Cryptanalyzing image encryption scheme using chaotic logistic map

## Dependencies

Create a Python virtual environment 
```
python -m venv venv 
```


Activate the virtual environment 
```
source venv/bin/activate
```


Install Dependencies
```
pip install matplotlib numpy 
```


## Usage

Encrypt an image:
```
python src/encrypt.py -i /path/to/img -x float(0 to 2pi) -y float(0 to 2pi) -K float(>18) -L int(11<L<1100)
```



Decrypt an image:
```
python src/decrypt.py /path/to/img
```
