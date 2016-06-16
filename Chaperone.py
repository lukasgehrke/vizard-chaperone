import viz, vizact, vizshape, vizproximity


class Chaperone(object):

    def __init__(self, path, step, radius, bemobil, trackers):
        """
        Fade a visible grid in and out when subjects move close to a boundary wall and back up subsequently.

        To toggle the visibility of the path proximity sensor, use the 'd' button.

        Args:
            path: path along defined points defining the proximity sensor shape. Should be the bounding room shape.
            step: distance between each line building the grid
            radius: distance to the wall at which the proximity sensor should be triggered
            bemobil: if true, then path area will be fixed to [(3, 6.5), (-3, 6.5), (-3, -6.5), (3, -6.5), (3, 6.5)].
            trackers: tracker objects to make as proximity targets. Can take multiple trackers and adds them
                to the proximity manager.
        """

        self.grids = []

        if bemobil:
            self.path = [(3, 6.5), (-3, 6.5), (-3, -6.5), (3, -6.5), (3, 6.5)]
        else:
            path = [(1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
            # todo create path through parameters provided to the Chaperone constructor (__init__).

        self.grid1 = self.add_grid([13, 3], [0, 0, 0], [3, 1.5, 0], step)
        self.grids.append(self.grid1)

        self.grid2 = self.add_grid([6, 3], [90, 0, 0], [0, 1.5, 6.5], step)
        self.grids.append(self.grid2)

        self.grid3 = self.add_grid([13, 3], [0, 0, 0], [-3, 1.5, 0], step)
        self.grids.append(self.grid3)

        self.grid4 = self.add_grid([6, 3], [90, 0, 0], [0, 1.5, -6.5], step)
        self.grids.append(self.grid4)

        for grid in self.grids:
            grid.addAction(vizact.fadeTo(0, time=3))
            grid.color(viz.GREEN)

        self.path_sensor = self.add_path_sensor(self.path, radius)

        self.path_manager = vizproximity.Manager()
        self.path_manager.addSensor(self.path_sensor)

        if trackers:
            for tracker in trackers:
                self.path_manager.addTarget(tracker)
        else:
            self.path_manager.addTarget(viz.MainView)

        self.path_manager.setDebug(viz.ON)
        vizact.onkeydown('d', self.path_manager.setDebug, viz.TOGGLE)

        self.path_manager.onEnter(self.path_sensor, self.enter_grid, self.grids)
        self.path_manager.onExit(self.path_sensor, self.exit_grid, self.grids)

    @staticmethod
    def add_grid(dimensions, euler, position, stepsize):
        """
        Creates a 4-walled vertical grid for the chaperone.

        Args:
            dimensions: dimensions (length/height) of one grid/wall for the chaperone
            euler: orientation in euler angles of grid.
            position: position of the grid in x, y, z coordinates
            stepsize: distance between the lines in the grid in meters

        Returns: A grid wall.

        """

        grid = vizshape.addGrid(dimensions, stepsize, 0, vizshape.AXIS_X)
        grid.setEuler(euler)
        grid.setPosition(position)

        return grid

    @staticmethod
    def add_path_sensor(points, radius):
        """
        Create a vizproximity sensor object as a path area shape.

        Args:
            points: A list of points that defines the centerline of the path.
            radius: Distance from the path centerline to path edge.

        Returns: vizproximity pathArea sensor object.

        """

        return vizproximity.Sensor(vizproximity.PathArea(points, radius), None)

    @staticmethod
    def enter_grid(e, grids):
        """
        Fades in a grid when a proximity target enters the chaperone path area.

        Args:
            e: triggered sensor event.
            grids: 4 side walls (visible as grids) at the bounding position of the room space.

        """

        print(e.sensor, "entered by proximity target")
        for grid in grids:
            grid.visible(viz.ON)
            grid.addAction(vizact.fadeTo(1, time=0.25))

    @staticmethod
    def exit_grid(e, grids):
        """
        Fades out a grid when a proximity target leaves the chaperone path area.

        Args:
            e: triggered sensor event.
            grids: 4 side walls (visible as grids) at the bounding position of the room space.

        """

        print(e.sensor, "left by proximity target")
        for grid in grids:
            grid.visible(viz.ON)
            grid.addAction(vizact.fadeTo(0, time=0.25))