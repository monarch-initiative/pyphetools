.. _threshold_column_mapper:

=====================
ThresholdColumnMapper
=====================


This mapper can be used for columns that have numerical data whereby being above or below a certain threshold is abnormal and 
can be represented by an HPO term. For instance, if "Age at head control (months)" is over 4 months, we would call Persistent head lag HP:0032988.



.. code-block:: python
  :linenos:

  headLagMapper = ThresholdedColumnMapper(hpo_id="HP:0032988", hpo_label="Persistent head lag", 
                                        threshold=4, call_if_above=True)
  headLagMapper.preview_column(dft["Age at head control (months)"])


This might lead to a result such as the following, in which only the individual in the fourth row required more than 4 months to display head control.


+-----------------------------------+----------+
| term                              | status   |
+===================================+==========+
| Persistent head lag (HP:0032988)  | excluded |
| Persistent head lag (HP:0032988)  | excluded | 
| Persistent head lag (HP:0032988)  | excluded |
| Persistent head lag (HP:0032988)  | observed |
| Persistent head lag (HP:0032988)  | excluded |  
+-----------------------------------+----------+



ThresholdedColumnMapper - special code
######################################

In some cases, phrases such as 'not attained' are used to denote that a child has not attained a certain milestone at the time of last examination and this this constitutes an abnormal finding. In this case, the optional argument ''observed_code'' should be used.

.. code-block:: python
  :linenos:

  delayedSittingMapper =  ThresholdedColumnMapper(hpo_id="HP:0025336", hpo_label="Delayed ability to sit", 
                                        threshold=9, call_if_above=True, observed_code='Not acquired')
