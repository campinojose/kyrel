"""
KYREL - Funciones del Sistema
Todas las funciones de lógica de negocio
"""

import os
import json
from datetime import datetime

DATOS_FILE = "datos.json"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cargar_datos():
    """Carga los datos desde el archivo JSON"""
    if not os.path.exists(DATOS_FILE):
        return {
            "productos": [],
            "ventas": [],
            "empleados": [],
            "asistencias": [],
            "incapacidades": [],
            "movimientos": [],
            "configuracion": {
                "proximo_id_producto": 1,
                "proximo_id_venta": 1,
                "proximo_id_movimiento": 1
            }
        }
    
    try:
        with open(DATOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            "productos": [],
            "ventas": [],
            "empleados": [],
            "asistencias": [],
            "incapacidades": [],
            "movimientos": [],
            "configuracion": {
                "proximo_id_producto": 1,
                "proximo_id_venta": 1,
                "proximo_id_movimiento": 1
            }
        }

def guardar_datos(datos):
    """Guarda los datos en el archivo JSON"""
    try:
        # Escribir a un archivo temporal primero
        temp_file = DATOS_FILE + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        # Reemplazar el archivo original
        import shutil
        shutil.move(temp_file, DATOS_FILE)
        return True
    except Exception as e:
        print(f"{Colors.RED}Error al guardar datos: {e}{Colors.END}")
        return False

def obtener_producto_por_id(producto_id):
    """Obtiene un producto por su ID"""
    datos = cargar_datos()
    for producto in datos["productos"]:
        if producto["id"] == int(producto_id):
            return producto
    return None

def obtener_productos_por_sede_categoria(sede, categoria):
    """Obtiene productos filtrados por sede y categoría"""
    datos = cargar_datos()
    return [p for p in datos["productos"] if p["sede"] == sede and p["categoria"] == categoria]

def obtener_todos_productos():
    """Obtiene todos los productos"""
    datos = cargar_datos()
    return datos["productos"]

def obtener_empleado_por_carnet(carnet):
    """Obtiene un empleado por su carnet"""
    datos = cargar_datos()
    for empleado in datos.get("empleados", []):
        if empleado["carnet"].upper() == carnet.upper():
            return empleado
    return None

def agregar_movimiento(datos, producto_id, tipo, cantidad, sede):
    """Registra un movimiento de inventario"""
    movimiento = {
        "id": datos["configuracion"]["proximo_id_movimiento"],
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "producto_id": producto_id,
        "tipo": tipo,
        "cantidad": cantidad,
        "sede": sede
    }
    datos["movimientos"].append(movimiento)
    datos["configuracion"]["proximo_id_movimiento"] += 1

# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_header(titulo):
    """Muestra el encabezado de cada vista"""
    print("\n" + "="*60)
    print(f"{Colors.BOLD}{Colors.CYAN}{titulo.center(60)}{Colors.END}")
    print(f"{Colors.YELLOW}Fecha: {datetime.now().strftime('%d %b %Y - %I:%M %p')}{Colors.END}")
    print("="*60 + "\n")

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.END}")

def leer_opcion(prompt, opciones_validas):
    """Lee una opción del usuario y valida que sea correcta"""
    while True:
        opcion = input(f"{Colors.GREEN}{prompt}{Colors.END}").strip()
        if opcion in opciones_validas:
            return opcion
        print(f"{Colors.RED}Opción inválida. Intenta de nuevo.{Colors.END}")

# ============================================================
# DASHBOARD
# ============================================================

def dashboard():
    """Vista del Dashboard General"""
    mostrar_header("DASHBOARD GENERAL")
    
    datos = cargar_datos()
    total_productos = sum(p["cantidad"] for p in datos["productos"])
    total_ventas_hoy = sum(v["total"] for v in datos["ventas"] if v["fecha"] == datetime.now().strftime("%Y-%m-%d"))
    
    print(f"{Colors.BOLD}📊 MÉTRICAS DEL DÍA{Colors.END}")
    print("-" * 60)
    print(f"  {Colors.GREEN}► Total unidades en stock:{Colors.END}       {total_productos}")
    print(f"  {Colors.GREEN}► Ventas registradas hoy:{Colors.END}        ${total_ventas_hoy:.2f}")
    print(f"  {Colors.GREEN}► Facturas emitidas:{Colors.END}             {len(datos['ventas'])}")
    print(f"  {Colors.GREEN}► Modelos de productos:{Colors.END}          {len(datos['productos'])}")
    print()
    
    print(f"{Colors.BOLD}📈 PRODUCTOS POR SEDE{Colors.END}")
    print("-" * 60)
    sedes = {}
    for p in datos["productos"]:
        sedes[p["sede"]] = sedes.get(p["sede"], 0) + p["cantidad"]
    
    for sede, cantidad in sedes.items():
        barra = "█" * (cantidad // 5)
        print(f"  {sede:12} │ {barra} {cantidad}")
    print()
    
    print(f"{Colors.BOLD}📦 ÚLTIMOS MOVIMIENTOS DE INVENTARIO{Colors.END}")
    print("-" * 60)
    movimientos = datos["movimientos"][-4:]  # Últimos 4
    print(f"  {'Producto':<20} {'Sede':<10} {'Tipo':<10} {'Cant.':<8} {'Fecha':<12}")
    print("  " + "-" * 58)
    for mov in reversed(movimientos):
        producto = obtener_producto_por_id(mov["producto_id"])
        nombre = producto["nombre"][:19] if producto else f"ID {mov['producto_id']}"
        print(f"  {nombre:<20} {mov['sede']:<10} {mov['tipo']:<10} {mov['cantidad']:<8} {mov['fecha']:<12}")
    
    pausar()

# ============================================================
# INVENTARIO
# ============================================================

def inventario_principal():
    """Vista principal del inventario por sede"""
    mostrar_header("INVENTARIO POR SEDE")
    
    datos = cargar_datos()
    total_camisas = sum(p["cantidad"] for p in datos["productos"] if p["categoria"] == "Camisas")
    total_sacos = sum(p["cantidad"] for p in datos["productos"] if p["categoria"] == "Sacos")
    
    print(f"{Colors.BOLD}📊 RESUMEN TOTAL{Colors.END}")
    print("-" * 60)
    print(f"  {Colors.GREEN}► Camisas Totales:{Colors.END}  {total_camisas}")
    print(f"  {Colors.GREEN}► Sacos Totales:{Colors.END}    {total_sacos}")
    print()
    
    print(f"{Colors.BOLD}📈 INVENTARIO POR SEDE{Colors.END}")
    print("-" * 60)
    sedes_cantidad = {}
    for p in datos["productos"]:
        sedes_cantidad[p["sede"]] = sedes_cantidad.get(p["sede"], 0) + p["cantidad"]
    
    emojis = {"Norte": "🟡", "Centro": "🔴", "Sur": "🟢"}
    for sede, cantidad in sorted(sedes_cantidad.items()):
        barra = "█" * (cantidad // 5)
        emoji = emojis.get(sede, "⚪")
        print(f"  {emoji} {sede:12} │ {barra} {cantidad}")
    print()
    
    print(f"{Colors.BOLD}🔍 BÚSQUEDA DE INVENTARIO{Colors.END}")
    print("-" * 60)
    print("1. Norte")
    print("2. Centro")
    print("3. Sur")
    print("0. Volver al menú principal")
    print()
    
    opcion = leer_opcion("Selecciona una sede (0-3): ", ["0", "1", "2", "3"])
    
    if opcion == "0":
        return
    
    sedes = {"1": "Norte", "2": "Centro", "3": "Sur"}
    sede = sedes[opcion]
    
    print()
    print("1. Camisas")
    print("2. Sacos")
    opcion_item = leer_opcion("Selecciona el tipo de producto (1-2): ", ["1", "2"])
    
    items = {"1": "Camisas", "2": "Sacos"}
    item = items[opcion_item]
    
    mostrar_resultados_inventario(sede, item)

def mostrar_resultados_inventario(sede, item):
    """Muestra los resultados de la búsqueda de inventario"""
    items_data = obtener_productos_por_sede_categoria(sede, item)
    cantidad_total = sum(p["cantidad"] for p in items_data)
    
    mostrar_header(f"INVENTARIO: {item} en Sede {sede}")
    
    print(f"{Colors.BOLD}{Colors.GREEN}Cantidad Total: {cantidad_total}{Colors.END}\n")
    
    print(f"{Colors.BOLD}📦 MODELOS DISPONIBLES{Colors.END}")
    print("-" * 60)
    print(f"  {'ID':<6} {'Nombre':<30} {'Cantidad':<10} {'Precio':<10}")
    print("  " + "-" * 58)
    
    for producto in items_data:
        print(f"  #{producto['id']:<5} {producto['nombre']:<30} {producto['cantidad']:<10} ${producto['precio']:<9.2f}")
    
    print()
    print(f"{Colors.BOLD}OPCIONES:{Colors.END}")
    print("1. Agregar producto nuevo")
    print("2. Modificar cantidad de producto existente")
    print("0. Volver")
    print()
    
    opcion = leer_opcion("Selecciona una opción (0-2): ", ["0", "1", "2"])
    
    if opcion == "1":
        agregar_producto(sede, item)
        mostrar_resultados_inventario(sede, item)
    elif opcion == "2":
        modificar_producto(sede, item)
        mostrar_resultados_inventario(sede, item)

def agregar_producto(sede, item):
    """Formulario para agregar un nuevo producto"""
    mostrar_header(f"AGREGAR PRODUCTO - {item} en {sede}")
    
    print(f"{Colors.YELLOW}Ingresa los datos del nuevo producto:{Colors.END}\n")
    
    nombre = input("Nombre del producto: ").strip()
    if not nombre:
        print(f"{Colors.RED}✗ Nombre no puede estar vacío{Colors.END}")
        pausar()
        return
    
    try:
        cantidad = int(input("Cantidad inicial: "))
        precio = float(input("Precio unitario: $"))
        
        if cantidad < 0 or precio < 0:
            print(f"{Colors.RED}✗ Cantidad y precio deben ser positivos{Colors.END}")
            pausar()
            return
    except ValueError:
        print(f"{Colors.RED}✗ Cantidad y precio deben ser valores numéricos válidos{Colors.END}")
        pausar()
        return
    
    # Cargar datos actuales
    datos = cargar_datos()
    
    # Crear nuevo producto con ID auto-increment
    nuevo_producto = {
        "id": datos["configuracion"]["proximo_id_producto"],
        "nombre": nombre,
        "categoria": item,
        "sede": sede,
        "cantidad": cantidad,
        "precio": precio
    }
    
    # Agregar producto a la lista
    datos["productos"].append(nuevo_producto)
    
    # Incrementar el próximo ID
    datos["configuracion"]["proximo_id_producto"] += 1
    
    # Registrar movimiento de entrada
    agregar_movimiento(
        datos,
        nuevo_producto["id"],
        "Entrada",
        cantidad,
        sede
    )
    
    # Guardar datos (una sola vez al final)
    guardar_datos(datos)
    
    print(f"\n{Colors.GREEN}✓ Producto agregado exitosamente con ID #{nuevo_producto['id']}{Colors.END}")
    print(f"  Nombre: {nombre}")
    print(f"  Cantidad: {cantidad}")
    print(f"  Precio: ${precio:.2f}")
    print(f"  Sede: {sede}")
    print(f"  Categoría: {item}")
    
    pausar()

def modificar_producto(sede, item):
    """Formulario para modificar cantidad de producto"""
    mostrar_header(f"MODIFICAR INVENTARIO - {item} en {sede}")
    
    print("1. Agregar cantidad a producto existente")
    print("2. Borrar cantidad de producto existente")
    print("0. Cancelar")
    print()
    
    opcion = leer_opcion("Selecciona operación (0-2): ", ["0", "1", "2"])
    
    if opcion == "0":
        return
    
    print()
    try:
        producto_id = int(input("ID del producto: "))
        cantidad = int(input("Cantidad a " + ("agregar" if opcion == "1" else "borrar") + ": "))
        
        if cantidad <= 0:
            print(f"{Colors.RED}✗ Cantidad debe ser mayor a 0{Colors.END}")
            pausar()
            return
    except ValueError:
        print(f"{Colors.RED}✗ ID y cantidad deben ser valores numéricos válidos{Colors.END}")
        pausar()
        return
    
    # Cargar datos
    datos = cargar_datos()
    
    # Buscar producto en los datos cargados
    producto = None
    for p in datos["productos"]:
        if p["id"] == producto_id:
            producto = p
            break
    
    if not producto:
        print(f"{Colors.RED}✗ Producto con ID #{producto_id} no encontrado{Colors.END}")
        pausar()
        return
    
    # Validar que el producto pertenezca a la sede y categoría correctas
    if producto["sede"] != sede or producto["categoria"] != item:
        print(f"{Colors.RED}✗ El producto no pertenece a esta sede/categoría{Colors.END}")
        print(f"  Producto está en: Sede {producto['sede']}, {producto['categoria']}")
        pausar()
        return
    
    # Modificar cantidad
    if opcion == "1":
        producto["cantidad"] += cantidad
        tipo_movimiento = "Entrada"
        operacion = "agregada"
    else:
        if producto["cantidad"] < cantidad:
            print(f"{Colors.RED}✗ No hay suficiente stock. Disponible: {producto['cantidad']}{Colors.END}")
            pausar()
            return
        producto["cantidad"] -= cantidad
        tipo_movimiento = "Salida"
        operacion = "eliminada"
    
    # Registrar movimiento
    agregar_movimiento(
        datos,
        producto_id,
        tipo_movimiento,
        cantidad,
        sede
    )
    
    # Guardar cambios (una sola vez al final)
    guardar_datos(datos)
    
    print(f"\n{Colors.GREEN}✓ Operación completada exitosamente{Colors.END}")
    print(f"  Producto: {producto['nombre']}")
    print(f"  Cantidad {operacion}: {cantidad}")
    print(f"  Stock actual: {producto['cantidad']}")
    
    pausar()

# ============================================================
# VENTAS
# ============================================================

def ventas_dashboard():
    """Vista del módulo de ventas"""
    mostrar_header("REGISTRO DE VENTAS")
    
    print(f"{Colors.BOLD}💰 VENTAS EN EL DÍA{Colors.END}")
    print("-" * 60)
    print(f"  {Colors.GREEN}► Ventas totales:{Colors.END}         $5,000  (+10% vs ayer)")
    print(f"  {Colors.GREEN}► Total de facturas:{Colors.END}      500     (+3% vs ayer)")
    print(f"  {Colors.GREEN}► Productos vendidos:{Colors.END}     9       (+2% vs ayer)")
    print(f"  {Colors.GREEN}► Nuevos clientes:{Colors.END}        12      (+5% vs ayer)")
    print()
    
    print(f"{Colors.BOLD}💵 GANANCIAS TOTALES{Colors.END}")
    print("-" * 60)
    print(f"  {Colors.GREEN}Total: $6,078.76{Colors.END}")
    print(f"  Rentabilidad: 48% más que el mes pasado")
    print()
    
    print(f"{Colors.BOLD}🏆 TOP PRODUCTOS{Colors.END}")
    print("-" * 60)
    productos_top = [
        ("01", "Camiseta Básica H&M", "46%", 46),
        ("02", "Jean tipo Denim M", "17%", 17),
        ("03", "Camiseta Oversize", "19%", 19),
        ("04", "Gorra Los Cadillacs", "29%", 29),
    ]
    print(f"  {'#':<4} {'Nombre':<25} {'Ventas':<10} {'Popularidad':<15}")
    print("  " + "-" * 58)
    for pid, nombre, ventas, pop in productos_top:
        barra = "█" * (pop // 5)
        print(f"  {pid:<4} {nombre:<25} {ventas:<10} {barra}")
    print()
    
    print(f"{Colors.BOLD}📊 VISITANTES POR MES{Colors.END}")
    print("-" * 60)
    visitantes = [("Ene", 300), ("Feb", 280), ("Mar", 350), ("Abr", 420), ("May", 390), 
                  ("Jun", 450), ("Jul", 410), ("Ago", 480), ("Sep", 430), ("Oct", 460), 
                  ("Nov", 410), ("Dic", 440)]
    for mes, cant in visitantes:
        barra = "█" * (cant // 20)
        print(f"  {mes:4} │ {barra} {cant}")
    print()
    
    print(f"{Colors.BOLD}ACCIONES DISPONIBLES:{Colors.END}")
    print("1. Registrar una venta")
    print("2. Buscar factura")
    print("3. Procesar devolución")
    print("4. Consultar stock disponible")
    print("0. Volver al menú principal")
    print()
    
    opcion = leer_opcion("Selecciona una opción (0-4): ", ["0", "1", "2", "3", "4"])
    
    if opcion == "0":
        return
    elif opcion == "1":
        registrar_venta()
    elif opcion == "2":
        buscar_factura()
    elif opcion == "3":
        procesar_devolucion()
    elif opcion == "4":
        consultar_stock()
    
    ventas_dashboard()

def registrar_venta():
    """Formulario para registrar una nueva venta"""
    mostrar_header("REGISTRAR NUEVA VENTA")
    
    print(f"{Colors.YELLOW}Ingresa los datos de la venta:{Colors.END}\n")
    
    cliente = input("Nombre del cliente: ").strip()
    if not cliente:
        print(f"{Colors.RED}✗ Nombre del cliente no puede estar vacío{Colors.END}")
        pausar()
        return
    
    # Solicitar carnet del empleado
    empleado_carnet = input("Carnet del empleado que atendió: ").strip().upper()
    if not empleado_carnet:
        print(f"{Colors.RED}✗ Carnet del empleado no puede estar vacío{Colors.END}")
        pausar()
        return
    
    # Validar que el empleado existe
    empleado = obtener_empleado_por_carnet(empleado_carnet)
    if not empleado:
        print(f"{Colors.RED}✗ Empleado con carnet {empleado_carnet} no encontrado{Colors.END}")
        pausar()
        return
    
    try:
        producto_id = int(input("ID del producto: "))
        cantidad = int(input("Cantidad: "))
        
        if cantidad <= 0:
            print(f"{Colors.RED}✗ Cantidad debe ser mayor a 0{Colors.END}")
            pausar()
            return
    except ValueError:
        print(f"{Colors.RED}✗ ID y cantidad deben ser valores numéricos válidos{Colors.END}")
        pausar()
        return
    
    # Cargar datos
    datos = cargar_datos()
    
    # Buscar producto en los datos cargados
    producto = None
    for p in datos["productos"]:
        if p["id"] == producto_id:
            producto = p
            break
    
    if not producto:
        print(f"{Colors.RED}✗ Producto con ID #{producto_id} no encontrado{Colors.END}")
        pausar()
        return
    
    # Verificar stock
    if producto["cantidad"] < cantidad:
        print(f"{Colors.RED}✗ Stock insuficiente. Disponible: {producto['cantidad']}{Colors.END}")
        pausar()
        return
    
    # Buscar empleado en los datos cargados para actualizar ventas
    empleado_data = None
    for e in datos.get("empleados", []):
        if e["carnet"].upper() == empleado_carnet.upper():
            empleado_data = e
            break
    
    # Calcular total
    total = cantidad * producto["precio"]
    
    # Crear nueva venta
    nueva_venta = {
        "id": datos["configuracion"]["proximo_id_venta"],
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "cliente": cliente,
        "producto_id": producto_id,
        "cantidad": cantidad,
        "total": total,
        "empleado_carnet": empleado_carnet
    }
    
    # Agregar venta
    datos["ventas"].append(nueva_venta)
    
    # Actualizar stock del producto
    producto["cantidad"] -= cantidad
    
    # Actualizar ventas realizadas del empleado
    if empleado_data:
        empleado_data["ventas_realizadas"] += 1
    
    # Incrementar próximo ID
    datos["configuracion"]["proximo_id_venta"] += 1
    
    # Registrar movimiento
    agregar_movimiento(
        datos,
        producto_id,
        "Venta",
        cantidad,
        producto["sede"]
    )
    
    # Guardar datos (una sola vez al final)
    guardar_datos(datos)
    
    print(f"\n{Colors.GREEN}✓ Venta registrada exitosamente #{nueva_venta['id']}{Colors.END}")
    print(f"  Cliente: {cliente}")
    print(f"  Producto: {producto['nombre']}")
    print(f"  Cantidad: {cantidad}")
    print(f"  Precio unitario: ${producto['precio']:.2f}")
    print(f"  {Colors.BOLD}Total: ${total:.2f}{Colors.END}")
    print(f"  Stock restante: {producto['cantidad']}")
    print(f"  Atendido por: {empleado['nombre']} ({empleado_carnet})")
    
    pausar()

def buscar_factura():
    """Buscar una factura por número"""
    mostrar_header("BUSCAR FACTURA")
    
    try:
        numero = int(input(f"{Colors.YELLOW}Número de factura: {Colors.END}"))
    except ValueError:
        print(f"{Colors.RED}✗ Número de factura inválido{Colors.END}")
        pausar()
        return
    
    # Cargar datos
    datos = cargar_datos()
    
    # Buscar venta
    venta = None
    for v in datos["ventas"]:
        if v["id"] == numero:
            venta = v
            break
    
    if not venta:
        print(f"\n{Colors.RED}✗ Factura #{numero} no encontrada{Colors.END}")
        pausar()
        return
    
    # Obtener información del producto
    producto = obtener_producto_por_id(venta["producto_id"])
    
    # Obtener información del empleado
    empleado = obtener_empleado_por_carnet(venta.get("empleado_carnet", ""))
    
    print(f"\n{Colors.GREEN}✓ Factura encontrada:{Colors.END}\n")
    print(f"  {Colors.BOLD}Factura: #{venta['id']}{Colors.END}")
    print(f"  Fecha: {venta['fecha']}")
    print(f"  Cliente: {venta['cliente']}")
    print(f"  Producto: {producto['nombre'] if producto else 'Desconocido'}")
    print(f"  Cantidad: {venta['cantidad']}")
    print(f"  {Colors.BOLD}Total: ${venta['total']:.2f}{Colors.END}")
    if empleado:
        print(f"  Atendido por: {empleado['nombre']} ({venta.get('empleado_carnet', 'N/A')})")
    
    pausar()

def procesar_devolucion():
    """Procesar una devolución"""
    mostrar_header("PROCESAR DEVOLUCIÓN")
    
    print(f"{Colors.YELLOW}Ingresa los datos de la devolución:{Colors.END}\n")
    
    try:
        factura_id = int(input("Número de factura: "))
        cantidad_devolver = int(input("Cantidad a devolver: "))
        
        if cantidad_devolver <= 0:
            print(f"{Colors.RED}✗ Cantidad debe ser mayor a 0{Colors.END}")
            pausar()
            return
    except ValueError:
        print(f"{Colors.RED}✗ Valores numéricos inválidos{Colors.END}")
        pausar()
        return
    
    motivo = input("Motivo: ").strip()
    
    # Cargar datos
    datos = cargar_datos()
    
    # Buscar venta
    venta = None
    for v in datos["ventas"]:
        if v["id"] == factura_id:
            venta = v
            break
    
    if not venta:
        print(f"\n{Colors.RED}✗ Factura #{factura_id} no encontrada{Colors.END}")
        pausar()
        return
    
    # Validar cantidad
    if cantidad_devolver > venta["cantidad"]:
        print(f"{Colors.RED}✗ Cantidad a devolver excede cantidad vendida ({venta['cantidad']}){Colors.END}")
        pausar()
        return
    
    # Buscar producto en los datos cargados
    producto = None
    for p in datos["productos"]:
        if p["id"] == venta["producto_id"]:
            producto = p
            break
    
    if not producto:
        print(f"{Colors.RED}✗ Producto no encontrado{Colors.END}")
        pausar()
        return
    
    # Restaurar stock
    producto["cantidad"] += cantidad_devolver
    
    # Registrar movimiento
    agregar_movimiento(
        datos,
        venta["producto_id"],
        "Devolución",
        cantidad_devolver,
        producto["sede"]
    )
    
    # Guardar cambios (una sola vez al final)
    guardar_datos(datos)
    
    print(f"\n{Colors.GREEN}✓ Devolución procesada correctamente{Colors.END}")
    print(f"  Factura: #{factura_id}")
    print(f"  Producto: {producto['nombre']}")
    print(f"  Cantidad devuelta: {cantidad_devolver}")
    print(f"  Motivo: {motivo}")
    print(f"  Stock actualizado: {producto['cantidad']}")
    
    pausar()

def consultar_stock():
    """Consultar stock disponible"""
    mostrar_header("CONSULTAR STOCK DISPONIBLE")
    
    producto_nombre = input(f"{Colors.YELLOW}Nombre del producto (parcial): {Colors.END}").strip().lower()
    
    if not producto_nombre:
        print(f"{Colors.RED}✗ Debes ingresar un nombre{Colors.END}")
        pausar()
        return
    
    # Cargar todos los productos
    productos = obtener_todos_productos()
    
    # Filtrar por nombre (búsqueda parcial)
    productos_filtrados = [p for p in productos if producto_nombre in p["nombre"].lower()]
    
    if not productos_filtrados:
        print(f"\n{Colors.RED}✗ No se encontraron productos con '{producto_nombre}'{Colors.END}")
        pausar()
        return
    
    # Agrupar por nombre de producto y sede
    stock_por_producto = {}
    for p in productos_filtrados:
        if p["nombre"] not in stock_por_producto:
            stock_por_producto[p["nombre"]] = {}
        stock_por_producto[p["nombre"]][p["sede"]] = p["cantidad"]
    
    # Mostrar resultados
    print(f"\n{Colors.GREEN}Stock disponible:{Colors.END}\n")
    
    for nombre_prod, sedes in stock_por_producto.items():
        print(f"{Colors.BOLD}{nombre_prod}:{Colors.END}")
        total = 0
        for sede, cantidad in sedes.items():
            print(f"  📍 Sede {sede}: {cantidad} unidades")
            total += cantidad
        print(f"  {Colors.BOLD}Total: {total} unidades{Colors.END}\n")
    
    pausar()

# ============================================================
# EMPLEADOS
# ============================================================

def gestion_empleados():
    """Vista principal de gestión de empleados"""
    mostrar_header("GESTIÓN DE EMPLEADOS")
    
    datos = cargar_datos()
    empleados = datos.get("empleados", [])
    incapacidades = datos.get("incapacidades", [])
    asistencias = datos.get("asistencias", [])
    
    total_empleados = len(empleados)
    total_incapacidades = len(incapacidades)
    
    # Calcular ausencias (asistencias con presente=false)
    total_ausencias = sum(1 for a in asistencias if not a["presente"])
    
    print(f"{Colors.BOLD}👥 RESUMEN GENERAL{Colors.END}")
    print("-" * 60)
    print(f"  {Colors.GREEN}► Total empleados:{Colors.END}           {total_empleados}")
    print(f"  {Colors.GREEN}► Incapacidades activas:{Colors.END}     {total_incapacidades}")
    print(f"  {Colors.GREEN}► Ausencias registradas:{Colors.END}     {total_ausencias}")
    print()
    
    # Calcular promedio de asistencia por sede
    print(f"{Colors.BOLD}📊 PROMEDIO DE ASISTENCIA POR SEDE{Colors.END}")
    print("-" * 60)
    
    asistencias_por_sede = {}
    for emp in empleados:
        sede = emp["sede"]
        if sede not in asistencias_por_sede:
            asistencias_por_sede[sede] = {"total": 0, "presentes": 0}
        
        # Contar asistencias del empleado
        for asist in asistencias:
            if asist["empleado_carnet"] == emp["carnet"]:
                asistencias_por_sede[sede]["total"] += 1
                if asist["presente"]:
                    asistencias_por_sede[sede]["presentes"] += 1
    
    for sede, stats in sorted(asistencias_por_sede.items()):
        if stats["total"] > 0:
            promedio = (stats["presentes"] / stats["total"]) * 100
            barra = "█" * int(promedio // 5)
            print(f"  {sede:12} │ {barra} {promedio:.1f}%")
    print()
    
    print(f"{Colors.BOLD}OPCIONES:{Colors.END}")
    print("1. Buscar empleado por carnet")
    print("2. Listar todos los empleados")
    print("0. Volver al menú principal")
    print()
    
    opcion = leer_opcion("Selecciona una opción (0-2): ", ["0", "1", "2"])
    
    if opcion == "0":
        return
    elif opcion == "1":
        buscar_empleado()
    elif opcion == "2":
        listar_empleados()
    
    gestion_empleados()

def buscar_empleado():
    """Buscar y mostrar información de un empleado por carnet"""
    mostrar_header("BUSCAR EMPLEADO")
    
    carnet = input(f"{Colors.YELLOW}Carnet del empleado: {Colors.END}").strip().upper()
    
    if not carnet:
        print(f"{Colors.RED}✗ Debes ingresar un carnet{Colors.END}")
        pausar()
        return
    
    empleado = obtener_empleado_por_carnet(carnet)
    
    if not empleado:
        print(f"\n{Colors.RED}✗ Empleado con carnet {carnet} no encontrado{Colors.END}")
        pausar()
        return
    
    # Obtener ventas del empleado
    datos = cargar_datos()
    ventas_empleado = [v for v in datos.get("ventas", []) if v.get("empleado_carnet") == carnet]
    total_ventas = sum(v["total"] for v in ventas_empleado)
    
    print(f"\n{Colors.GREEN}✓ Empleado encontrado:{Colors.END}\n")
    print(f"  {Colors.BOLD}Carnet: {empleado['carnet']}{Colors.END}")
    print(f"  Nombre: {empleado['nombre']}")
    print(f"  Sede: {empleado['sede']}")
    print(f"  Horas trabajadas: {empleado['horas_trabajadas']} hrs")
    print(f"  Ventas realizadas: {empleado['ventas_realizadas']}")
    print(f"  {Colors.BOLD}Total vendido: ${total_ventas:.2f}{Colors.END}")
    
    pausar()

def listar_empleados():
    """Lista todos los empleados"""
    mostrar_header("LISTA DE EMPLEADOS")
    
    datos = cargar_datos()
    empleados = datos.get("empleados", [])
    
    if not empleados:
        print(f"{Colors.RED}No hay empleados registrados{Colors.END}")
        pausar()
        return
    
    print(f"{Colors.BOLD}{'Carnet':<10} {'Nombre':<25} {'Sede':<12} {'Horas':<8} {'Ventas':<8}{Colors.END}")
    print("-" * 70)
    
    for emp in empleados:
        print(f"{emp['carnet']:<10} {emp['nombre']:<25} {emp['sede']:<12} {emp['horas_trabajadas']:<8} {emp['ventas_realizadas']:<8}")
    
    pausar()
