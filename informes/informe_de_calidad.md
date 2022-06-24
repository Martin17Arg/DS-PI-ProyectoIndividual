# Informe de calidad del dato

## *Tabla:* Proveedores
*Archivo:* Proveedores.csv

| Columnas | Descripción |
| --- | --- |
| **IDProveedor** | Identificación única del proveedor |
| **Nombre** | Nombre del proveedor |
| **Address** | Domicilio del proveedor |
| **City** | Localidad del proveedor |
| **State** | Provincia del proveedror |
| **Country** | Pais del proveedor |
| **departamen** | Municipio o departamento del proveedor |

## Calidad del dato

![Proveedores](/img/bar-Proveedores.jpg)

## Observaciones

**departament**: Esta columna no aporta información extra y puede llevar a confusiones o datos inconsistentes si hay un error de carga.

**Valores faltantes en columna Nombre:**: Se pueden completar a partir de información del registro (Address, por ejemplo).

## *Tabla:* Sucursales
*Archivo:* Sucursales.csv

| Columnas | Descripción |
| --- | --- |
| **ID** | Identificador único de la sucursal |
| **Sucursal** | Nombre de la sucursal |
| **Direccion** | Dirección de la sucursal |
| **Localidad** | Localidad donde está ubicada la sucursal |
| **Provincia** | Provincia donde está ubicada la sucursal |
| **Latitud** | Latitud de la sucursal |
| **Longitud** | Longitud de la sucursal |

![Sucursales](/img/bar-Sucursales.jpg)

### Outliers

**Outliers en coordenadas**: Deben contrastarse con la localidad para verificar consistencia del dato. 
**Provincia**: Se debe normalizar y utilizar ID de provincia. 

![Sucursales_latitud](/img/box-Sucursales-Latitud.jpg)

![Sucursales_longitud](/img/box-Sucursales-Longitud.jpg)

## *Tabla:* Venta
*Archivo:* Venta.csv

| Columnas | Descripción |
| --- | --- |
| **IdVenta** | Identificador único de la venta |
| **Fecha** | Fecha de la venta |
| **Fecha_Entrega** | Fecha de entrega de los productos |
| **IdCanal** | Identificador del canal de venta |
| **IdCliente** | Identificador del cliente |
| **IdSucursal** | Identificador de la sucursal |
| **IdEmpleado** | Identificador del empleado |
| **IdProducto** | Identificador del producto |
| **Precio** | Precio de venta |
| **Cantidad** | Cantidad del producto vendida |

![Venta](/img/bar-Venta.jpg)

### Observaciones

Los valores nulos y outliers son bajos (2%) para cantidad y precio.

![Venta_Cantidad](/img/box-Venta-Cantidad.jpg)

![Venta_Precio](/img/box-Venta-Precio.jpg)


## *Tabla:* Compra
*Archivo:* Compra.csv

| Columnas | Descripción |
| --- | --- |
| **IdCompra** | Identificador único de la compra |
| **Fecha** | Fecha de la compra |
| **Fecha_Año** | Año de la compra |
| **Fecha_Mes** | Mes de la compra |
| **Fecha_Periodo** | Variable representativa del año y el mes |
| **IdProducto** | Identificador único del producto comprado |
| **Cantidad** | Cantidad comprada |
| **Precio** | Precio de compra |
| **IdProveedor** | Identificador único del proveedor |


![Compra](/img/bar-Compra.jpg)

### Observaciones

Existe un bajo porcentaje de valores nulos y un outlier en el campo Precio.
Se debe corregir dado que por su valor absoluto puede afectar los KPI que usen este campo.

![Compra_Precio](/img/box-Compra-Precio.jpg)


## *Tabla:* Clientes
*Archivo:* Clientes.csv

| Columnas | Descripción |
| --- | --- |
| **ID** |  Identificador único de cliente.|
| **Provincia** |  Provincia donde reside el cliente.|
| **Nombre_y_Apellido** | Nombre y apellido del cliente |
| **Domicilio** | Domicilio de residencia del cliente |
| **Telefono** | Teléfono de contacto (fijo o móvil). |
| **Edad** | Edad del cliente |
| **Localidad** | Localidad de residencia |
| **X** | Longitud (horizontal, positivo hacia el Este) |
| **Y** | Latitud (vertical, positivo hacia el Norte) |
| **col10** | Sin uso |


![Clientes](/img/bar-Clientes.jpg)

### Observaciones

**Edad**: Debería ser reemplazado por un campo que sea fecha de nacimiento
dado que es una característica que no cambia con el paso del tiempo.
**col10**: Solo tiene valores nulos. Se elimina del dataset.
**Localidad**: Se completan valores faltantes a partir de las coordenadas.
**X e Y**: Se utiliza algoritmo de Levenshtein para completar valores nulos a partir de la localidad.


![Clientes_X](/img/box-Clientes-X.jpg)

![Clientes_Y](/img/box-Clientes-Y.jpg)


## *Tabla:* Localidades
*Archivo:* Localidades.csv

| Columnas | Descripción |
| --- | --- |
| **categoria** | N/A |
| **centroide_lat** | Latitud de referencia para la localidad |
| **centroide_lon** | Longitud de referencia para la localidad |
| **departamento_id** | N/A |
| **departamento_nombre** | N/A |
| **fuente** | N/A |
| **id** | Identificador único de la localidad |
| **localidad_censal_id** | N/A |
| **localidad_censal_nombre** | N/A |
| **municipio_id** | N/A |
| **municipio_nombre** | N/A |
| **nombre** | Nombre de la localidad |
| **provincia_id** | Identificador único de la provincia |
| **provincia_nombre** | Nombre de la provincia donde está ubicada la localidad |

### Observaciones

Se descartan las columnas que no suman información, dejando como referencia a las 
localidades con su identificador, centroides, nombre y referencia a la provincia (provincia_id).
