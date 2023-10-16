import abc
from typing import List
from .individual import Individual


class AbstractEncoder(metaclass=abc.ABCMeta):
    """
    Abstract superclass for all chort encoder classes
    """

    def __init__(self) -> None:
        pass


    def output_phenopackets(self, outdir="phenopackets"):
        """Output data about all individuals as GA4GH phenopackets

        :param outdir: name of directory to write phenopackets (default: 'phenopackets')
        :type outdir: str
        """
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        individual_list = self.get_individuals()
        written = Individual.output_individuals_as_phenopackets(individual_list=individual_list,
                                                                metadata=self._metadata,
                                                                pmid=self._pmid,
                                                                outdir=outdir)
        print(f"Wrote {written} phenopackets to {outdir}")

    @abc.abstractmethod
    def get_individuals(self) -> List[Individual]:
        """Get a list of all Individual objects in the cohort

        :returns: a list of all Individual objects in the cohort
        :rtype: List[Individual]
        """
        raise NotImplementedError("Need to implement in subclass")