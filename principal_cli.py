"""
KYREL - Sistema de Gestión
Versión Consola (CLI)
Archivo Principal
"""

import sys
from funciones import *

def menu_principal():
    """Menú principal del sistema"""
    while True:
        limpiar_pantalla()
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
        print(f"{'KYREL - SISTEMA DE GESTIÓN'.center(60)}")
        print(f"{'='*60}{Colors.END}\n")
        
        print(f"{Colors.BOLD}MENÚ PRINCIPAL{Colors.END}")
        print("-" * 60)
        print(f"  {Colors.GREEN}1.{Colors.END} 📊 Dashboard General")
        print(f"  {Colors.GREEN}2.{Colors.END} 📦 Inventario por Sede")
        print(f"  {Colors.GREEN}3.{Colors.END} 💰 Registro de Ventas")
        print(f"  {Colors.GREEN}4.{Colors.END} 👥 Gestión de Empleados")
        print(f"  {Colors.RED}0.{Colors.END} ❌ Salir")
        print("-" * 60)
        print()
        
        opcion = leer_opcion("Selecciona una opción (0-4): ", ["0", "1", "2", "3", "4"])
        
        if opcion == "0":
            limpiar_pantalla()
            print(f"\n{Colors.CYAN}Gracias por usar KYREL. ¡Hasta pronto!{Colors.END}\n")
            sys.exit(0)
        elif opcion == "1":
            dashboard()
        elif opcion == "2":
            inventario_principal()
        elif opcion == "3":
            ventas_dashboard()
        elif opcion == "4":
            gestion_empleados()

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        limpiar_pantalla()
        print(f"\n{Colors.CYAN}Programa interrumpido. ¡Hasta pronto!{Colors.END}\n")
        sys.exit(0)
