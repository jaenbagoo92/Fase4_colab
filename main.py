"""Punto de entrada principal de la aplicación Software FJ.
Simula 10 operaciones completas (válidas e inválidas) demostrando estabilidad,
manejo de listas en memoria y uso de bloques try/except/else/finally.
Documentado línea por línea para la Fase 4 de POO."""

from excepciones import SoftwareFJError
from logger import GestorLogs
from modelos import (Cliente,ReservaSala,AlquilerEquipo,AsesoriaEspecializada,Reserva,)


class SistemaGestionSoftwareFJ:"""Contenedor en memoria que almacena colecciones de clientes, servicios y reservas."""

    def __init__(self): # Listas internas para almacenar las entidades gestionadas sin bases de datos
        self.clientes: list[Cliente] = []
        self.servicios: list = []
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, codigo_id: str, nombre: str, correo: str, telefono: str) -> Cliente | None: """Registra un cliente utilizando la estructura estructurada try/except/else."""
        try:   # Intenta instanciar el cliente aplicando validaciones estrictas
            nuevo_cliente = Cliente(codigo_id, nombre, correo, telefono)
        except SoftwareFJError as e: # Captura errores de validación de datos sin detener la ejecución de la app
            print(f"  [X] Error registrando cliente: {e}")
            GestorLogs.registrar_evento("ERROR", f"Fallo al registrar cliente ({codigo_id})", e)
            return None
        else: # Se ejecuta únicamente si no ocurrieron excepciones durante la creación
            self.clientes.append(nuevo_cliente)
            print(f"  [OK] {nuevo_cliente.obtener_resumen()}")
            GestorLogs.registrar_evento("INFO", f"Cliente registrado exitosamente: {codigo_id}")
            return nuevo_cliente

    def registrar_servicio(self, servicio) -> bool: """Almacena un servicio validado dentro del catálogo interno."""
        self.servicios.append(servicio)
        print(f"  [OK] {servicio.obtener_resumen()}")
        GestorLogs.registrar_evento("INFO", f"Servicio agregado al catálogo: {servicio.codigo_id}")
        return True

    def crear_y_procesar_reserva(self, codigo_id: str, cliente: Cliente, servicio, duracion: int, impuesto: float = 19.0, descuento: float = 0.0) -> Reserva | None:
        """Procesa una reserva completa empleando try/except/else/finally."""
        reserva = None
        try:  # Intenta crear la reserva y procesar su confirmación y costos
            reserva = Reserva(codigo_id, cliente, servicio, duracion)
            reserva.procesar_y_confirmar(impuesto_pct=impuesto, descuento_pct=descuento)
        except SoftwareFJError as e: # Captura incidencias de negocio y registra el error controlado
            print(f"  [X] Error en reserva {codigo_id}: {e}")
            if e.__cause__:
                print(f"      -> Causa raíz encadenada: {e.__cause__}")
            GestorLogs.registrar_evento("ERROR", f"Error procesando reserva {codigo_id}", e)
            return None
        else:  # Se ejecuta si la reserva se procesó de forma exitosa
            self.reservas.append(reserva)
            print(f"  [OK] {reserva.obtener_resumen()}")
            return reserva
        finally: # Bloque de auditoría que se ejecuta siempre al finalizar la transacción
            print(f"      (Auditoría finalizada para intento de transacción '{codigo_id}')")


def ejecutar_simulacion():
    print("=" * 75)
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ (SIN BASE DE DATOS)")
    print("=" * 75)
    GestorLogs.registrar_evento("INFO", "=== INICIO DE EJECUCIÓN DEL SISTEMA SOFTWARE FJ ===")

    sistema = SistemaGestionSoftwareFJ()

    # --- OPERACIÓN 1: Registro válido de Cliente 1 ---
    print("\n1. Registrando cliente válido (CLI-01)...")
    cli1 = sistema.registrar_cliente("CLI-01", "Carlos Mendoza", "carlos.mendoza@empresa.com", "3001234567")

    # --- OPERACIÓN 2: Registro válido de Cliente 2 ---
    print("\n2. Registrando cliente válido (CLI-02)...")
    cli2 = sistema.registrar_cliente("CLI-02", "Laura Gómez", "laura.gomez@tech.co", "3109876543")

    # --- OPERACIÓN 3: Registro INVÁLIDO de Cliente (correo y teléfono erróneos) ---
    print("\n3. Intentando registrar cliente con datos inválidos (CLI-03)...")
    sistema.registrar_cliente("CLI-03", "Pedro", "correo_sin_arroba", "123")

    # --- OPERACIÓN 4: Creación válida de Servicios del catálogo ---
    print("\n4. Creando catálogo de servicios válidos e inactivos...")
    sala1 = ReservaSala("SRV-01", "Sala Ejecutiva Norte", 80000, capacidad=15, disponible=True)
    equipo1 = AlquilerEquipo("SRV-02", "Workstation Dell Precision", 45000, cantidad_unidades=3, disponible=True)
    asesoria1 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud", 150000, especialidad="AWS & DevOps", disponible=True)
    sala_inactiva = ReservaSala("SRV-04", "Sala Mantenimiento", 60000, capacidad=8, disponible=False)

    sistema.registrar_servicio(sala1)
    sistema.registrar_servicio(equipo1)
    sistema.registrar_servicio(asesoria1)
    sistema.registrar_servicio(sala_inactiva)

    # --- OPERACIÓN 5: Creación INVÁLIDA de Servicio (Tarifa negativa) ---
    print("\n5. Intentando crear servicio con tarifa inconsistente...")
    try:
        AsesoriaEspecializada("SRV-ERR", "Consultoría Fallida", -50000, "Seguridad")
    except SoftwareFJError as e:
        print(f"  [X] Error controlado al instanciar servicio: {e}")
        GestorLogs.registrar_evento("ERROR", "Intento de creación de servicio con tarifa negativa", e)

    # --- OPERACIÓN 6: Reserva EXITOSA de Sala (método con sobrecarga de parámetros) ---
    print("\n6. Procesando reserva exitosa de Sala (5 horas, IVA 19%, Descuento 10%)...")
    res1 = sistema.crear_y_procesar_reserva("RES-01", cli1, sala1, duracion=5, impuesto=19.0, descuento=10.0)

    # --- OPERACIÓN 7: Reserva EXITOSA de Equipos (solo impuestos) ---
    print("\n7. Procesando reserva exitosa de Alquiler de Equipos (4 horas, IVA 19%)...")
    sistema.crear_y_procesar_reserva("RES-02", cli2, equipo1, duracion=4, impuesto=19.0)

    # --- OPERACIÓN 8: Reserva FALLIDA por servicio no disponible ---
    print("\n8. Intentando reservar servicio no disponible (SRV-04)...")
    sistema.crear_y_procesar_reserva("RES-03", cli1, sala_inactiva, duracion=3)

    # --- OPERACIÓN 9: Reserva FALLIDA por regla de negocio (Excepción encadenada) ---
    print("\n9. Intentando reservar Asesoría por 15 horas (supera máximo permitido de 8h)...")
    sistema.crear_y_procesar_reserva("RES-04", cli2, asesoria1, duracion=15)

    # --- OPERACIÓN 10: Cancelación de reserva y protección contra doble cancelación ---
    print("\n10. Cancelando reserva RES-01 y probando protección contra doble cancelación...")
    if res1:
        try:
            res1.cancelar("Cambio de agenda del cliente")
            print(f"  [OK] Estado actualizado: {res1.obtener_resumen()}")
            # Intento explícito de volver a cancelar la misma reserva ya cancelada
            res1.cancelar("Segundo intento inválido")
        except SoftwareFJError as e:
            print(f"  [X] Excepción capturada en operación repetida: {e}")
            GestorLogs.registrar_evento("ERROR", "Intento de doble cancelación en RES-01", e)

    # Resumen final del sistema en memoria
    print("\n" + "=" * 75)
    print(f"RESUMEN FINAL EN MEMORIA: {len(sistema.clientes)} Clientes | {len(sistema.servicios)} Servicios | {len(sistema.reservas)} Reservas registradas")
    print("Todos los eventos y errores fueron guardados correctamente en 'logs.txt'.")
    print("=" * 75)
    GestorLogs.registrar_evento("INFO", "=== FIN DE EJECUCIÓN SIN INTERRUPCIONES ===")


if __name__ == "__main__":
    ejecutar_simulacion()
