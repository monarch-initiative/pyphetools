import abc
import os
from typing import List
from .individual import Individual


class AbstractEncoder(metaclass=abc.ABCMeta):
    """
    Abstract superclass for all chort encoder classes
    """

    def __init__(self, metadata) -> None:
        if metadata is None:
            raise ValueError("Must pass a metadata object to constructor")
        # the following workaround is needed because isinstance gets confused about the two following classes
        elif str(type(metadata)) == "<class 'phenopackets.schema.v2.core.meta_data_pb2.MetaData'>":
            self._metadata = metadata
        elif str(type(metadata)) == "<class 'pyphetools.creation.metadata.MetaData'>":
            self._metadata = metadata.to_ga4gh()
        else:
            raise ValueError(F"Malformed metadata argument of type {type(metadata)}")

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
                                                                outdir=outdir)
        print(f"Wrote {written} phenopackets to {outdir}")

    @abc.abstractmethod
    def get_individuals(self) -> List[Individual]:
        """Get a list of all Individual objects in the cohort

        :returns: a list of all Individual objects in the cohort
        :rtype: List[Individual]
        """
        raise NotImplementedError("Need to implement in subclass")
