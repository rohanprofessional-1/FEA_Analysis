import numpy as np
from ansys.mapdl.core import launch_mapdl

# Launch MAPDL
def script_execute(ilength, iwidth, iheight, imaterial, imodulus, iratio):
    mapdl = launch_mapdl()

    # Clear any previous data
    mapdl.clear()

    # Define the beam material properties
    E = imodulus  # Young's modulus in Pascals (Steel)
    nu = iratio   # Poisson's ratio

    # Beam geometry (in meters)
    length = ilength  # Length of the cantilever beam
    width = iwidth  # Width of the beam
    height = iheight # Height of the beam

    # Create the geometry
    mapdl.prep7()

    # Define the material
    mapdl.mp('EX', imaterial, E)    # Young's modulus for material number 1
    mapdl.mp('PRXY', imaterial, nu) # Poisson's ratio for material number 1

    # Define element type (SOLID185 for 3D solid)
    mapdl.et(1, 185)

    # Define beam dimensions (create a block)
    mapdl.block(0, length, 0, width, 0, height)

    # Mesh the geometry
    mapdl.esize(0.05)  # Set element size
    mapdl.vmesh('ALL') # Mesh the entire volume

    # Apply boundary conditions
    # Fixed support at one end of the beam (cantilever condition)
    mapdl.nsel('S', 'LOC', 'X', 0) # Select nodes where X=0 (left end)
    mapdl.d('ALL', 'ALL')          # Fix all degrees of freedom at selected nodes

    # Apply a load at the free end of the beam
    mapdl.nsel('S', 'LOC', 'X', length) # Select nodes at X = length (right end)
    force = 1000  # Apply a force of 1000 N
    mapdl.f('ALL', 'FY', -force)  # Apply load in the Y direction

    # Solve the problem
    mapdl.allsel()  # Select all nodes and elements
    mapdl.run('/SOLU') # Switch to the solution mode
    mapdl.solve()      # Solve

    # Post-processing
    mapdl.post1()      # Enter post-processing
    mapdl.set(1)       # First result set

    # Get the nodal displacements
    node_numbers, displacements = mapdl.result.nodal_displacement(0)  # Get displacements for all nodes

    # Convert displacements to a NumPy array
    displacements = np.array(displacements)

    # Get the maximum displacement in the Y direction (2nd column, index 1)
    max_disp = displacements[:, 1].max()  # Displacement in the Y direction
    print(f"Maximum displacement (Y): {max_disp:.6f} meters")


    # Plot the equivalent stress (von Mises stress)
    mapdl.post_processing.plot_nodal_eqv_stress()
    displacement = mapdl.post_processing.nodal_displacement('Y') # might need to change, based on GPT
    stress = mapdl.post_processing.element_stress() # might need to change, based on GPT
    mapdl.exit()
    return displacement, stress

    # Close the MAPDL session


