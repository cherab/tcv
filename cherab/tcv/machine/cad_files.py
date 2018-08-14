
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.


import os

from raysect.primitive import Mesh, import_stl
from raysect.optical.spectralfunction import ConstantSF
from raysect.optical.material import AbsorbingSurface, Lambert
from raysect.optical.library.metal import RoughTungsten, RoughBeryllium


try:
    CADMESH_PATH = os.environ['CHERAB_CADMESH']
except KeyError:
    if os.path.isdir('/projects/cadmesh/'):
        CADMESH_PATH = '/projects/cadmesh/'
    else:
        raise ValueError("CHERAB's CAD file path environment variable 'CHERAB_CADMESH' is"
                         "not set.")


tungsten_roughness = 0.2
lambertian_roughness = 0.25


# Carbon Tiles
TILES_HFS = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_tiles_hfs.stl'), Lambert(ConstantSF(lambertian_roughness)))]
TILES_LFS = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_tiles_lfs.stl'), Lambert(ConstantSF(lambertian_roughness)))]
TILES_ROOF = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_tiles_roof.stl'), Lambert(ConstantSF(lambertian_roughness)))]
TILES_FLOOR = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_tiles_floor.stl'), Lambert(ConstantSF(lambertian_roughness)))]
CARBON_TILES = TILES_HFS + TILES_LFS + TILES_ROOF + TILES_FLOOR

# Vessel structures
PORTS_FLOOR = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_ports_floor.stl'), RoughTungsten(tungsten_roughness))]
PORTS_ROOF = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_ports_roof.stl'), RoughTungsten(tungsten_roughness))]
PORTS_LFS = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_ports_lfs.stl'), RoughTungsten(tungsten_roughness))]
VESSEL_FLOOR = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_vessel_floor.stl'), RoughTungsten(tungsten_roughness))]
VESSEL_ROOF = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_vessel_roof.stl'), RoughTungsten(tungsten_roughness))]
VESSEL_HFS = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_vessel_hfs.stl'), RoughTungsten(tungsten_roughness))]
VESSEL_LFS = [(os.path.join(CADMESH_PATH, 'tcv/mesh/medium_vessel_lfs.stl'), RoughTungsten(tungsten_roughness))]
VESSEL = PORTS_FLOOR + PORTS_ROOF + PORTS_LFS + VESSEL_FLOOR + VESSEL_ROOF + VESSEL_HFS + VESSEL_LFS


# Complete TCV mesh for first wall reflection calculations
TCV_MESH = CARBON_TILES + VESSEL


def import_tcv_mesh(world, material=None, tungsten_material=None, carbon_material=None):

    for mesh_item in TCV_MESH:

        mesh_path, default_material = mesh_item

        if material:
            pass
        elif tungsten_material and isinstance(default_material, RoughTungsten):
            material = tungsten_material
        elif carbon_material and isinstance(default_material, Lambert):
            material = carbon_material
        else:
            material = default_material

        print("importing {}  ...".format(os.path.split(mesh_path)[1]))
        directory, filename = os.path.split(mesh_path)
        mesh_name, ext = filename.split('.')
        mesh = import_stl(mesh_path, scaling=0.001, parent=world, material=material, name=mesh_name)
