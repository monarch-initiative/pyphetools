import abc
import os
from typing import List
from .individual import Individual
from .metadata import MetaData


class AbstractEncoder(metaclass=abc.ABCMeta):
    """
    Abstract superclass for all chort encoder classes

    :param metadata: A pyphetools MetaData object (from which a GA4GH MetaData  object can be constructed).
    :type metadata: MetaData
    """

    def __init__(self, metadata:MetaData) -> None:
        if metadata is None:
            raise ValueError("Must pass a metadata object to constructor")
        # the following workaround is needed because isinstance gets confused about the two following classes
        elif str(type(metadata)) == "<class 'pyphetools.creation.metadata.MetaData'>":
            self._metadata = metadata
        else:
            raise ValueError(F"metadata argument must be pyphetools MetaData but was {type(metadata)}")

    def output_phenopackets(self, outdir:str="phenopackets"):
        """Output data about all individuals as GA4GH phenopackets

        :param outdir: name of directory to write phenopackets (default: 'phenopackets')
        :type outdir: str
        """
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        individual_list = self.get_individuals()
        written = Individual.output_individuals_as_phenopackets(individual_list=individual_list,
                                                                metadata=self._metadata.to_ga4gh(),
                                                                outdir=outdir)
        print(f"Wrote {written} phenopackets to {outdir}")

    @abc.abstractmethod
    def get_individuals(self) -> List[Individual]:
        """Get a list of all Individual objects in the cohort

        :returns: a list of all Individual objects in the cohort
        :rtype: List[Individual]
        """
        raise NotImplementedError("Need to implement in subclass")
