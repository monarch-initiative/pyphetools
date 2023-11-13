import os



EMPTY_CELL = ""

class HpoaTableCreator:
    """
    Create an HPO "small file" with the following columns
    1. #diseaseID
    2. diseaseName
    3. phenotypeID
    4. phenotypeName
    5. onsetID
    6. onsetName
    7. frequency
    8. sex
    9. negation
    10. modifier
    11. description
    12. publication
    13. evidence
    14. biocuration
    These should be tab separate fields.

    """

    def __init__(self, phenopacket_dir) -> None:
        pass