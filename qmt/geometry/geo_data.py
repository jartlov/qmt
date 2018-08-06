import pickle
from qmt.task_framework import Data

class Geo1DData(Data):
    def __init__(self):
        """
        Class for holding a 1D geometry specification.
        """
        super(Geo1DData, self).__init__()
        self.parts = {}

    def add_part(self, part_name, start_point, end_point, overwrite=False):
        """
        Add a part to this geometry.
        :param str part_name: Name of the part to create
        :param float start_point: Position of the start of the part
        :param float end_point: Position of the end of the part
        :param bool overwrite: Should we allow this to overwrite?
        """
        start, end = sorted([start_point, end_point])
        if (part_name in self.parts) and (not overwrite):
            raise ValueError("Attempted to overwrite the part " + part_name + ".")
        else:
            self.parts[part_name] = (start, end)

    def remove_part(self, part_name, ignore_if_absent=False):
        """
        Remove a part from this geometry.
        :param str part_name: Name of part to remove
        :param bool ignore_if_absent: Should we ignore an attempted removal if the part name
        is not found?
        """
        if part_name in self.parts:
            del self.parts[part_name]
        else:
            if not ignore_if_absent:
                raise ValueError(
                    "Attempted to remove the part " + part_name + ", which doesn't exist.")
            else:
                pass


class Geo2DData(Data):
    def __init__(self):
        """
        Class for holding a 2D geometry specification. This class holds two main dicts:
            - parts is a dictionary of shapely Polygon objects
            - edges is a dictionary of shapely LineString objects
        Parts are intended to be 2D domains, while edges are used for setting boundary conditions
        and surface conditions.
        """
        super(Geo2DData, self).__init__()
        self.parts = {}
        self.edges = {}
        self.build_order = []

    def add_part(self, part_name, part, overwrite=False):
        """
        Add a part to this geometry.
        :param str part_name: Name of the part to create
        :param Polygon part: Polygon object from shapely.geometry. This must be a valid Polygon.
        :param bool overwrite: Should we allow this to overwrite?
        """
        if not part.is_valid:
            raise ValueError("Part " + part_name + " is not a valid polygon.")
        if (part_name in self.parts) and (not overwrite):
            raise ValueError("Attempted to overwrite the part " + part_name + ".")
        else:
            self.parts[part_name] = part
            self.build_order += [part_name]

    def remove_part(self, part_name, ignore_if_absent=False):
        """
        Remove a part from this geometry.
        :param str part_name: Name of part to remove
        :param bool ignore_if_absent: Should we ignore an attempted removal if the part name
        is not found?
        """
        if part_name in self.parts:
            del self.parts[part_name]
            self.build_order.remove(part_name)
        else:
            if not ignore_if_absent:
                raise ValueError(
                    "Attempted to remove the part " + part_name + ", which doesn't exist.")
            else:
                pass

    def add_edge(self, edge_name, edge, overwrite=False):
        """
        Add an edge to this geometry.
        :param str edge_name: Name of the edge to create
        :param LineString edge: LineString object from shapely.geometry.
        :param bool overwrite: Should we allow this to overwrite?
        """
        if (edge_name in self.edges) and (not overwrite):
            raise ValueError("Attempted to overwrite the edge " + edge_name + ".")
        else:
            self.edges[edge_name] = edge
            self.build_order += [edge_name]

    def remove_edge(self, edge_name, ignore_if_absent=False):
        """
        Remove an edge from this geometry.
        :param str edge_name: Name of part to remove
        :param bool ignore_if_absent: Should we ignore an attempted removal if the part name
        is not found?
        """
        if edge_name in self.edges:
            del self.edges[edge_name]
            self.build_order.remove(edge_name)
        else:
            if not ignore_if_absent:
                raise ValueError(
                    "Attempted to remove the edge " + edge_name + ", which doesn't exist.")
            else:
                pass

class Geo3DData(Data):
    def __init__(self):
        """
        Class for a 3D geometry specification. It holds:
            - parts is a dict of Part3D objects, keyed by the label of each Part3D object.
            - build_order is a list of strings indicating the construction order.
        """
        super(Geo3DData, self).__init__()
        self.build_order = []
        self.parts = {}
        # ~ self.serial_FCdoc
        # ~ self.parts = {label: part}

    def get_parts():
        return self.parts
        # ~ parts[0].label == build_order[0]
        # TODO with only part names: self.build_order

    # TODO: serialisation

    def add_part(self, part_name, part, overwrite=False):
        """
        Add a part to this geometry.
        :param str part_name: Name of the part to create
        :param Part3D part: Part3D object.
        :param bool overwrite: Should we allow this to overwrite?
        """
        if (part_name in self.parts) and (not overwrite):
            raise ValueError("Attempted to overwrite the part " + part_name + ".")
        else:
            self.parts[part_name] = part


    def remove_part(self, part_name, ignore_if_absent=False):
        """
        Remove a part from this geometry.
        :param str part_name: Name of part to remove
        :param bool ignore_if_absent: Should we ignore an attempted removal if the part name
        is not found?
        """
        if part_name in self.parts:
            del self.parts[part_name]
        else:
            if not ignore_if_absent:
                raise ValueError(
                    "Attempted to remove the part " + part_name + ", which doesn't exist.")
            else:
                pass

    def write_fcstd(self, file_path=None):
        """Write geometry to a fcstd file.

        Returns the fcstd file path.
        """
        if file_path == None:
            file_path = self.label + '.fcstd'
        data = pickle.loads(self.serial_fcdoc)
        with open(file_path, 'wb') as of:
            of.write(data)
        return file_path
