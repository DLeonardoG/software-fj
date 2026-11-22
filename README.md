# Software FJ

Programa de la fase 4 de Programación (213023). Lleva clientes, servicios y reservas de la empresa Software FJ. No usa base de datos: mientras el programa está abierto los datos viven en listas, y lo que pasa (bien o mal) queda en `logs/events.log`.

## Cómo ejecutarlo

Python 3.10 o más nuevo. En esta carpeta:

```
python main.py
```

No hay que instalar paquetes.

## Archivos

- `entity.py` — clase abstracta con identificador y nombre.
- `client.py` — cliente. Documento, correo y teléfono se validan al crear el objeto.
- `services.py` — servicio abstracto y tres tipos: sala, alquiler de equipos y asesoría. Cada uno arma el valor a su manera.
- `reservation.py` — reserva con estado pendiente, confirmada, cancelada o procesada.
- `registry.py` — las listas de clientes, servicios y reservas.
- `exceptions.py` — errores propios del sistema.
- `event_log.py` — escritura del log.
- `main.py` — 18 casos seguidos. Si uno falla, el siguiente igual corre.

## Precios

`calculate_cost(hours, discount=0, tax_rate=0.19)` es el cálculo completo. `calculate_cost_with_discount` no cobra IVA y `calculate_cost_with_tax` no aplica descuento.

La asesoría de 3 horas o más suma 40.000 COP antes de impuestos y no pasa de 8 horas. El alquiler multiplica la tarifa por las horas y por la cantidad de equipos.

## Entrega

Grupo 213023_182. El PDF está en `Fase4_Software_FJ.pdf`.
