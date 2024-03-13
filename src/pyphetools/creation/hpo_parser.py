import os
import typing

import hpotk

from .hpo_cr import HpoConceptRecognizer
from .hpo_exact_cr import HpoExactConceptRecognizer


class HpoParser:
    """
    Class to retrieve and parse the HPO JSON file using the HPO-Toolkit

    Users probably will want to set the `release` option (e.g. `v2024-03-06` for the last release
    as of the time of this writing) or pass the path to the `hp.json` file via `hpo_json_file` option.

    Both options are optional, and the last HPO release will be used by default. The `release` has a priority
    over `hpo_json_file`.

    :param hpo_json_file: a `str` with a URL pointing to a remote `hp.json` (only ``http`` and ``https`` protocols
    are supported (no ``file``, ``ftp``)) or a path to a local `hp.json` file.
    :param release: an optional `str` with the HPO release tag or `None` if the latest HPO release should be used.
    """
    # TODO: consider deprecating this class. It is not too useful after adding `OntologyStore` API to `hpo-toolkit>=0.5.0`.

    def __init__(
            self,
            hpo_json_file: typing.Optional[str] = None,
            release: typing.Optional[str] = None,
    ):
        if release is not None:
            store = hpotk.configure_ontology_store()
            self._ontology = store.load_hpo(release=release)
        elif hpo_json_file is not None:
            if not hpo_json_file.startswith('http') and not os.path.isfile(hpo_json_file):
                raise FileNotFoundError(f"Could not find hp.json file at {hpo_json_file}")
            self._ontology = hpotk.load_ontology(hpo_json_file)
        else:
            store = hpotk.configure_ontology_store()
            self._ontology = store.load_hpo()

    def get_ontology(self) -> hpotk.Ontology:
        """
        :returns: a reference to the HPO
        """
        return self._ontology

    def get_label_to_id_map(self) -> typing.Mapping[str, str]:
        """
        Create a map from a lower case version of HPO labels to the corresponding HPO id
        only include terms that are descendants of PHENOTYPE_ROOT

        :returns: a map from lower-case HPO term labels to HPO ids
        """
        label_to_id_d = {}
        for term in self._ontology.terms:
            hpo_id = term.identifier
            if not self._ontology.graph.is_ancestor_of(hpotk.constants.hpo.base.PHENOTYPIC_ABNORMALITY, hpo_id):
                continue
            label_to_id_d[term.name.lower()] = hpo_id.value
            # Add the labels of the synonyms
            if term.synonyms is not None and len(term.synonyms) > 0:
                for synonym in term.synonyms:
                    lc_syn = synonym.name.lower()
                    # only take synonyms with length at least 5 to avoid spurious matches
                    if len(lc_syn) > 4:
                        label_to_id_d[lc_syn] = hpo_id.value

        return label_to_id_d

    def get_id_to_label_map(self) -> typing.Mapping[str, str]:
        """
        :returns: a map from HPO term ids to HPO labels
        :rtype: Dict[str,str]
        """
        id_to_label_d = {}

        for term in self._ontology.terms:
            id_to_label_d[term.identifier.value] = term.name

        return id_to_label_d

    def get_hpo_concept_recognizer(self) -> HpoConceptRecognizer:
        return HpoExactConceptRecognizer(
            label_to_id=self.get_label_to_id_map(),
            id_to_primary_label=self.get_id_to_label_map(),
        )

    def get_version(self) -> typing.Optional[str]:
        return self._ontology.version
