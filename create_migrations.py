import os

# Create migrations directory
migrations_dir = os.path.join('courses', 'migrations')
if not os.path.exists(migrations_dir):
    os.makedirs(migrations_dir)

# Create __init__.py
init_file = os.path.join(migrations_dir, '__init__.py')
if not os.path.exists(init_file):
    with open(init_file, 'w') as f:
        pass

print("Migrations directory and __init__.py created successfully!") 