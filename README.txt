======
ZigZag
======

ZigZag provides functions for identifying the peaks and valleys of a time
series. Additionally, it provides a function for computing the maximum drawdown.

If numba can be imported, it will be used to greatly accelerate the execution 
time at the cost of a small initial compile. On my machine, the JIT'd code 
executed about 38 times faster than the pure Python code. Numba is not an 
install_requires package because numba can be a pain to install for some people. 
`Learn more about numba here <http://numba.pydata.org/>`_.

For fastest understanding, `view the IPython notebook demo tutorial <http://nbviewer.ipython.org/github/jbn/ZigZag/blob/master/zigzag_demo.ipynb>`_.

Contributing
------------
This is an admittedly small project. Still, if you have any contributions, 
please `fork this project on github <https://github.com/jbn/ZigZag>`_ and
send me a pull request. You can email me, 
`John B Nelson <http://blog.johnbnelson.com/>`_, at 
`jbn@pathdependent.com <mailto:jbn@pathdependent.com>`_ with any questions. 
