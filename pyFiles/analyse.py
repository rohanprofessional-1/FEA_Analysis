from ansys.mapdl.core import launch_mapdl
import numpy as np
import os
import shutil
from flask import jsonify


def run_analysis(Ym, Pr, L, W, H, F):
    # Launch MAPDL in non-interactive mode
    mapdl = launch_mapdl(additional_switches='-b')  # '-b' flag for batch mode (no GUI)

    try:
        # Clear previous data and setup model
        mapdl.clear()
        E = Ym  # Young's modulus in Pascals (Steel)
        nu = Pr  # Poisson's ratio
        length = L # Beam length (meters)
        width, height = W, H  # Beam width and height (meters)
        force = F  # Load in Newtons

        # Create geometry, material properties, and mesh
        mapdl.prep7()
        mapdl.mp('EX', 1, E)
        mapdl.mp('PRXY', 1, nu)
        mapdl.et(1, 185)
        mapdl.block(0, length, 0, width, 0, height)
        mapdl.esize(0.05)
        mapdl.vmesh('ALL')

        # Boundary conditions
        mapdl.nsel('S', 'LOC', 'X', 0)
        mapdl.d('ALL', 'ALL')
        mapdl.nsel('S', 'LOC', 'X', length)
        mapdl.f('ALL', 'FY', -force)

        # Solve
        mapdl.allsel()
        mapdl.run('/SOLU')
        mapdl.solve()

        # Post-processing to retrieve results
        mapdl.post1()
        mapdl.set(1)

        # Get displacement and stress results
        _, displacements = mapdl.result.nodal_displacement(0)
        max_disp = np.abs(np.array(displacements)[:, 1]).max()  # Max absolute Y displacement

        _, principal_stresses = mapdl.result.principal_nodal_stress(0)
        max_stress = np.abs(np.array(principal_stresses)[:, 0]).max()  # Max absolute principal stress

        # Prepare the results in JSON format
        results = {
            "Poisson's Ratio" : nu,
            "Young's modulus" : E,
            "Maximum Absolute Displacement (m)": max_disp,
            "Maximum Absolute Principal Stress (MPa)": max_stress / 1e6  # Convert Pa to MPa
        }

    finally:
        # Ensure MAPDL session closes after completion

        mapdl.exit()
        delete_directory_contents('x')
        delete_directory_contents('y')
        delete_directory_contents('z')


    return max_disp, max_stress
def delete_directory_contents(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The directory {directory_path} does not exist.")

