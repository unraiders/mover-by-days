# mover-by-days

Utilidad para **Unraid** que mueve los ficheros de un pool al array según los días de antigüedad pasados en la variable, respetando en el movimiento los hardlinks existentes y con la función de pausar/reanudar los torrents sedeados en qBittorrent.


Funcionamiento:

- Pausa los torrents en qBittorrent según el valor de la variable DAYS_THRESHOLD.
- Busca los ficheros en el pool pasado en la variable ORIGEN según el valor de la variable DAYS_THRESHOLD.
- Mueve las carpetas y los ficheros seleccionados del pool pasado en la variable ORIGEN al array pasado en la variable DESTINO respetando los hardlinks existentes.
- Reanuda los torrents en qBittorrent según el valor de la variable DAYS_THRESHOLD.



## Configuración variables de entorno y rutas.

| CLAVE                | NECESARIO | VALOR                                                                                                                                 |
| :------------------- | :-------: | :------------------------------------------------------------------------------------------------------------------------------------ |
| QBITTORRENT_HOST     |     ✅     | Host y puerto de qBittorrent, ejemplo: 192.168.2.20:8090                                                                              |
| QBITTORRENT_USER     |     ✅     | Usuario de qBittorrent                                                                                                                |
| QBITTORRENT_PASSWORD |     ✅     | Contraseña de qBittorrent                                                                                                             |
| CACHE_MOUNT          |     ✅     | Ruta al almacenamiento caché dónde se verifican los torrents antes de resumir/pausar, normalmente en el pool, ejemplo: /mnt/calentito |
| ORIGEN               |     ✅     | Carpeta/Share origen desde dónde moverá los ficheros y carpetas.                                                                      |
| DESTINO              |     ✅     | Carpeta/Share destino dónde moverá los ficheros y carpetas.                                                                           |
| DAYS_THRESHOLD       |     ✅     | Número de días de antigüedad para ejecutar el proceso de movimiento.                                                                  |
| CRON_SCHEDULE        |     ✅     | Hora de ejecutar el script (formato crontab. ej., 0 7 * * * = 7:00 AM, visita https://crontab.guru/ para más info.)                   |
| DEBUG                |           | Habilita el modo Debug en el log. (0 = No / 1 = Si)                                                                                   |
| PRUEBA               |           | Habilita el modo Prueba, no realiza ninguna modificación. (0 = No / 1 = Si)                                                           |


  > [!IMPORTANT]
  > Se recomienda hacer uso de la variable PRUEBA = 1 antes de poner el Docker en producción, la ejecución de este Docker implica movimiento de ficheros y nos tenemos que asegurar que el proceso es correcto., con la variable PRUEBA a 1 NO realizará ningún movimiento de ficheros pero tendremos en el log el detalle de los ficheros que movería estando la variable PRUEBA a 0. 
  > 
  > Activando la variable DEBUG = 1 podemos tener un log detallado de los torrents que pausará/reanudará en qBittorrent y los ficheros que moverá del pool al array.
  > 
  > Una vez que compruebes que el funcionamiento sería el esperado después de la primera ejecución, comprueba que ha pasado los ficheros correctamente y que ha respetado los hardlinks entre ambos ficheros.

### Instalación plantilla en Unraid.

- Nos vamos a una ventana de terminal en nuestro Unraid, pegamos esta línea y enter:
```sh
wget -O /boot/config/plugins/dockerMan/templates-user/my-mover-by-days.xml https://raw.githubusercontent.com/unraiders/mover-by-days/refs/heads/main/my-mover-by-days.xml
```
- Nos vamos a DOCKER y abajo a la izquierda tenemos el botón "AGREGAR CONTENEDOR" hacemos click y en seleccionar plantilla seleccionamos mover-by-days y rellenamos las variables de entorno necesarias, tienes una explicación en cada variable en la propia plantilla.

---

