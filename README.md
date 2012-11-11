# Minimal GUI for controlling Google TV from your PC. #

## Installation ##

    # Install M2Crypto (required for pairing)
    sudo easy_install m2crypto
    
    # Install pybonjour
    sudo easy_install pybonjour 

    # Install [googletv-anymote](https://github.com/stevenle/googletv-anymote) (library that makes pairing with GTV easy)
    git clone https://github.com/stevenle/googletv-anymote.git 
    cd googletv-anymote 
    sudo python setup.py install 

    # Download Hivequeen
    git clone git@github.com:powerje/Hivequeen.git 
    cd Hivequeen.git 
    python hivequeen.py 

## Notes ##

The interface is terrible as I just whipped this up for personal use, but figured someone else might find it useful.

## Acknowledgements ##

Thanks to Steven Le for doing most of the work here by creating his googletv-anymote lib.
