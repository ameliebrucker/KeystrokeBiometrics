from enum import Enum

class Feature (Enum):
    """
    A class for representing features as constants

    Attributes (Class)
    M : string, representing the feature monograph
    DD : string, representing the feature down down
    UD : string, representing the feature up down
    DU : string, representing the feature down up
    UU : string, representing the feature up up
    """

    M = "MONOGRAPH"
    DD = "DOWN_DOWN"
    UD = "UP_DOWN"
    DU = "DOWN_UP"
    UU = "UP_UP"