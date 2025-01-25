# mover-by-days
Ejecutar rsync con días de antigüedad y teniendo en cuenta hardlinks.

### Instalación plantilla en Unraid.
- Nos vamos a una ventana de terminal en nuestro Unraid, pegamos esta línea y enter:
```sh
wget -O /boot/config/plugins/dockerMan/templates-user/my-mover-by-days.xml https://raw.githubusercontent.com/unraiders/mover-by-days/refs/heads/main/my-mover-by-days.xml
```
- Nos vamos a DOCKER y abajo a la izquierda tenemos el botón "AGREGAR CONTENEDOR" hacemos click y en seleccionar plantilla seleccionamos mover-by-days y rellenamos las variables de entorno necesarias, tienes una explicación en cada variable en la propia plantilla.

---
