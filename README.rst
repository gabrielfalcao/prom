Prom - Prometheus demo for MacOSX
=================================


Install Dependencies
--------------------

**Local Requirements:**

#. **go1.10.3** (with ``$GOPATH`` `pre-configured <https://github.com/golang/go/wiki/GOPATH>`_)
#. **python3.6**
#. `**pipenv** <https://docs.pipenv.org/>`_


.. code:: bash

   pipenv install --dev
   go get -u github.com/prometheus/prometheus/cmd/...
   go get -u github.com/prometheus/alertmanager/cmd/...
