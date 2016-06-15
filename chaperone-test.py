import viz

from Chaperone import Chaperone

viz.go()

world = viz.add('ground.osgb')
chaperone = Chaperone(None, 0.1, 0.5, True, None)