import fem as gf
import numpy as np
import pandas as pd

# Parameters for the beam
length = 1.0  # Length of the beam in meters
height = 0.1  # Height of the beam in meters
width = 0.05  # Width of the beam in meters

# Material properties
young_modulus = 210e9  # Young's modulus in Pascals
poisson_ratio = 0.3    # Poisson's ratio
force = 1000           # Force in Newtons applied at the free end

# Mesh for a 3D cantilever beam
mesh = gf.Mesh('cartesian',
               np.linspace(0, length, 20),  # X-axis divisions
               np.linspace(0, width, 5),    # Y-axis divisions
               np.linspace(0, height, 5))   # Z-axis divisions

# Assign finite element method for 3D displacement
mfu = gf.MeshFem(mesh, 3)  # 3D problem requires 3D FEM
mfu.set_fem(gf.Fem('FEM_QK(3,1)'))

# Assign finite element method for stresses
mfs = gf.MeshFem(mesh, 6)  # For stress components in 3D
mfs.set_fem(gf.Fem('FEM_QK(3,1)'))

# Define the model
model = gf.Model('real')

# Add linear elasticity brick for 3D
model.add_fem_variable('u', mfu)
model.add_initialized_data('cmu', [young_modulus / (2 * (1 + poisson_ratio))])
model.add_initialized_data('clambda', [young_modulus * poisson_ratio / ((1 + poisson_ratio) * (1 - 2 * poisson_ratio))])
model.add_isotropic_linearized_elasticity_brick('displacement', 'u', 'clambda', 'cmu')

# Boundary conditions: Fix one end of the beam (cantilever support)
left_boundary = mesh.outer_faces_with_direction([-1, 0, 0])
model.add_Dirichlet_condition_with_multipliers('u', mfu, left_boundary)

# Apply force on the opposite end (free end)
right_boundary = mesh.outer_faces_with_direction([1, 0, 0])
model.add_source_term_brick('volume', 'u', right_boundary, [0, 0, -force])

# Solve the problem
model.solve()

# Extract results
displacement = model.variable('u')
print("Displacement field: ", displacement)

# Compute the stress tensor (Von Mises)
vm_stress = gf.asm('compute Von Mises or Tresca', mfs, 'clambda', 'cmu', displacement)
print("Von Mises Stress field: ", vm_stress)
