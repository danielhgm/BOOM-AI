import yaml

# Leer el archivo environment.yml
with open('environment.yml', 'r') as file:
    env = yaml.safe_load(file)

# Crear el archivo requirements.txt
with open('requirements.txt', 'w') as file:
    for dep in env['dependencies']:
        if isinstance(dep, str):
            # Especificar paquetes que se pueden instalar con pip
            if dep.startswith("python=") or dep.startswith("pip="):
                continue  # Omitir versiones específicas de Python y pip
            file.write(dep + '\n')
        elif isinstance(dep, dict) and 'pip' in dep:
            # Escribir las dependencias de pip
            for pip_dep in dep['pip']:
                file.write(pip_dep + '\n')
