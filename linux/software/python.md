# Installing Python packages

- APT
    - Some Python packages can be found in the Raspbian archives, and can be installed using APT, for example:
    ```
    sudo apt-get update
    sudo apt-get install python-picamera
    ```
    
- Pip
    - Some Python packages are installed using ```pip```:
    ```
    sudo apt-get install python-pip
    sudo pip install simplejson
    ```