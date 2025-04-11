from ase import Atoms
from ase.io import read, write
from ase.visualize import view
import spglib

# Read the CIF file
print("Reading the CIF file...")
atoms = read('./material_projects_strucutre/TiO.cif')
print(f"Original structure: {len(atoms)} atoms, cell parameters: {atoms.cell.cellpar()}")

# View the original structure
cell = atoms.get_cell()
positions = atoms.get_scaled_positions()
numbers = atoms.get_atomic_numbers()

lattice, scaled_positions, numbers = spglib.find_primitive(
    (cell, positions, numbers), symprec=1e-5
)

primitive_atoms = Atoms(numbers=numbers, 
    scaled_positions=scaled_positions, cell=lattice,pbc=True)

# View the primitive cell
print("Displaying the primitive structure...")
view(primitive_atoms)

# Save the primitive cell to a new CIF file
write('./TiO_primitive.cif', primitive_atoms)
print("Primitive cell saved to TiO_primitive.cif")

# Print additional information about the structures
print("\nDetailed information:")
print("Original structure:")
print(f"Chemical formula: {atoms.get_chemical_formula()}")
print(f"Cell volume: {atoms.get_volume():.3f} Å³")
print(f"Cell vectors (Å):")
for i, vector in enumerate(atoms.cell):
    print(f"  a{i+1}: [{vector[0]:.4f}, {vector[1]:.4f}, {vector[2]:.4f}]")

print("\nPrimitive structure:")
print(f"Chemical formula: {primitive_atoms.get_chemical_formula()}")
print(f"Cell volume: {primitive_atoms.get_volume():.3f} Å³")
print(f"Cell vectors (Å):")
for i, vector in enumerate(primitive_atoms.cell):
    print(f"  a{i+1}: [{vector[0]:.4f}, {vector[1]:.4f}, {vector[2]:.4f}]")