from typing import Literal


type sensorStates = Literal['normal','alert']
type simulationStates = Literal['created','playing','standby','paused','stopped','restart']
type mapOptions = Literal['raw', 'beauty']
type summaryOptions = Literal['debug', 'production']