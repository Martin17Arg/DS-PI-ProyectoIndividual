import os

# Evaluacion de calidad de dato
os.system('python batch.py')

# Carga inicial
os.system('python normalizar_canaldeventa.py')
os.system('python normalizar_tipodegasto.py')
os.system('python normalizar_cliente.py')
os.system('python normalizar_gasto.py')
os.system('python normalizar_proveedor.py')
os.system('python normalizar_sucursal.py')
os.system('python normalizar_venta.py')
os.system('python normalizar_compra.py')

# Carga incremental
os.system('python normalizar_cliente_delta.py')
os.system('python normalizar_venta_delta.py')
