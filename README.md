# Advertencia. Este trabajo ha sido abandonado, pronto volvere para concluirlo pero de momento esta inactivo.
Lo dejo en público para que vean parte de mi trabajo en github, como manejo tecnologias, etc...

# Hola! Bienvenido al README de BOOM AI, aqui iremos documentando lo necesario!

# Diariamente se actualizan las librerias instalandas tanto en conda como en pip

1. Primero eliminar environment.yml y requirements.txt
2. Despues aplicar el siguiente comando a bash que es para pasar las librerias de conda actualizadas a .yml

conda env export --name conda1 > environment.yml

3. Ahora en el bash usamos:

python requirementymltotxt.py

Esto nos deja actualizadas las librerias para conda y pip dejando reproducibilidad, una buena practica!

# Para el uso de MYSQL

La documentacion extendida esta en trello pero allá vamos!

[Link para trello:](https://trello.com/c/2tCY6VfI/12-mysql-en-wsl-comandos)

Mañana continuo actualizando la documentación!

## Dia 12 de agosto del 2024

Actualizo este readme para mencionar que con este commit tambien añadire los cambios relacionados con el ISR, ayer habia hecho push pero hoy no aparece hecho este push, esta adicion de texto es simplemente para mencionar que ya hice push.

## Dia 16 de agosto del 2024

Ya cuando inicias sesion te redirige a otra pagina y esta constantemente actualizandose para verificar que seas tu, modularize en templates pero hace falta colocar en app.py las rutas, actualmente falta trabajar del login en el menu desplegable ya que se colisionan los diseños css
