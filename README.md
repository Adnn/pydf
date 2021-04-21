# pydf
Assemble images into a multipage PDF document, without altering images quality.

## Installation

Clone the project and install the requirements in a virtual environment:

    $ git clone git@github.com:Adnn/pydf.git
    $ cd pydf/
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
    $ deactivate

Symlink the wrapper into a binary folder on your path.

Example on _macos_:

    $ ln -s $(pwd)/pydf /usr/local/bin/

## Usage

    $ ls -l
    image1.jpg
    image2.jpg
    manifest.txt

    $ cat manifest.txt
    image1.jpg 100   # 100 dpi for both dimensions (could otherwise be given as x_dpi y_dpi)
    image2.jpg       # no explicit dpi value provided, assumes dpi info is embedded into image metadata

    $ pydf.py manifest.txt document.pdf

