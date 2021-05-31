====================================================================================
Subsequential Time Series Clustering: Evidence of Temporal Patterns in Exchange Rate
====================================================================================

This is the official repository of the research poster **Clustering Subsecuencial de Series de Tiempo: Evidencia de Patrones Temporales en el tipo de cambio USD/MXN**, originally presented in its spanish version at the National Seminar *Escuela de Probabilidad y Estadística 2020* (`EPE2020`_). Its an academic event organized by `CIMAT`_ (A government-funded research institute, internationally renowned, which main focus is Mathematical Research).

.. _CIMAT: https://www.cimat.mx/en/
.. _EPE2020: https://epe2020.eventos.cimat.mx/

-------------
Poster
-------------

.. image:: https://github.com/IFFranciscoME/STSC-Temporal-Patterns/raw/master/poster/figures/Poster_ES.png
        :target: https://github.com/IFFranciscoME/STSC-Temporal-Patterns/raw/master/poster/figures/Poster_ES.png
        :alt: Final version of poster
        :align: center

-------------------------------
General Elements of the Project
-------------------------------

There are three types of content in this repository.

1. Data scraping, preparation and clustering: **Python**
2. Data analysis, synthesis and presentation: **R**
3. Tables, Figures, Formulas within the beamer poster: **LaTeX**

Project Execution
-----------------

In order to conduct a wide list of experiments variations with all *candidate trigger events* searching within all the historical prices, it was necessary to perform a parallelization of the project, mainly in the process where the *MASS* algorithm was used to search for subsequential patterns. 

MASS Algorithm
--------------

This work was aimed at testing the capabilities of the *Mueen's Algorithm for Similarity Search* (`MASS`_), we acknowledge the work of the original authors which can be consulted for further technical details.

.. _MASS: https://www.cimat.mx/en/https://www.cs.unm.edu/~mueen/FastestSimilaritySearch.html

mass-ts
-------

The python implementation that was utilized for this work is the `MASS-TS`_ python package, which can be found and installed at https://pypi.org/project/mass-ts/

.. `_MASS-TS`: https://github.com/matrix-profile-foundation/mass-ts

-----------------
Reproduce Results
-----------------

- Clone repository
  
Clone entire github project

    git@github.com:IFFranciscoME/STSC-Temporal-Patterns.git

(optional) create a virtual environment

    virtualenv venv

(optional) activate virtual environment

        source ~/venv/bin/activate

and then install dependencies

        pip install -r requirements.txt

------
Author
------

J.Francisco Munnoz - `IFFranciscoME`_ - Is an Associate Professor in the Mathematics and Physics Department, at `ITESO`_ University.

.. _ITESO: https://iteso.mx/
.. _IFFranciscoME: https://iffranciscome.com/

-------
License
-------

**GNU General Public License v3.0** 

*Permissions of this strong copyleft license are conditioned on making available 
complete source code of licensed works and modifications, which include larger 
works using a licensed work, under the same license. Copyright and license notices 
must be preserved. Contributors provide an express grant of patent rights.*

*Contact: For more information in reggards of this project, please contact francisco.me@iteso.mx*
