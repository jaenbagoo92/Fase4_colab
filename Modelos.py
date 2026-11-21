"""Módulo principal del modelo de dominio de Software FJ.
Implementa abstracción, herencia, polimorfismo, encapsulación y simulación de sobrecarga.
Documentado línea por línea para la Fase 4 de POO."""

from abc import ABC, abstractmethod
from excepciones import (DatosInvalidosError,ServicioNoDisponibleError,ReservaInvalidaError,CalculoInconsistenteError,)
from logger import GestorLogs

class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad identificable del sistema."""

    def __init__(self, codigo_id: str): # Valida que el código identificador no esté vacío o sea inválido
        if not codigo_id or not isinstance(codigo_id, str) or not codigo_id.strip():
            raise DatosInvalidosError("El código identificador de la entidad no puede estar vacío.")
        self._codigo_id = codigo_id.strip()

    @property
    def codigo_id(self) -> str: # Propiedad de lectura encapsulada para el identificador
        return self._codigo_id

    @abstractmethod
    def obtener_resumen(self) -> str:  """Método abstracto obligatorio para describir la entidad en texto."""
        pass

class Cliente(EntidadSistema): """Clase que representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(self, codigo_id: str, nombre: str, correo: str, telefono: str):
        super().__init__(codigo_id) # Asignación a través de setters para activar validaciones inmediatas
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:  # Valida que el nombre tenga al menos 3 caracteres reales
        if not valor or len(valor.strip()) < 3:
            raise DatosInvalidosError(f"Nombre inválido '{valor}': debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None: # Valida la estructura básica del correo electrónico
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None: # Valida que el teléfono contenga únicamente dígitos y una longitud mínima
        if not valor or not valor.strip().isdigit() or len(valor.strip()) < 7:
            raise DatosInvalidosError(f"Teléfono inválido '{valor}': debe contener al menos 7 dígitos numéricos.")
        self._telefono = valor.strip()

    def obtener_resumen(self) -> str: # Retorna una cadena formateada con los datos encapsulados del cliente
        return f"Cliente [{self.codigo_id}]: {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"


class Servicio(EntidadSistema, ABC):"""Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo_id: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):super().__init__(codigo_id)
        if not nombre_servicio or not nombre_servicio.strip():raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        if tarifa_base <= 0:raise CalculoInconsistenteError(f"La tarifa base ({tarifa_base}) debe ser mayor que cero.")

        self._nombre_servicio = nombre_servicio.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre_servicio(self) -> str:
        return self._nombre_servicio

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros_operacion(self, duracion_horas: int) -> None: """Valida reglas específicas de cada tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: int) -> float:  """Calcula el costo polimórfico según el tipo de servicio y su duración."""
        pass

    def calcular_costo_total(self, duracion_horas: int, impuesto_pct: float = 0.0, descuento_pct: float = 0.0, ) -> float: """  Método con comportamiento sobrecargado mediante parámetros opcionales:
        1. calcular_costo_total(horas) -> Solo costo base.
        2. calcular_costo_total(horas, impuesto_pct) -> Costo base + impuestos.
        3. calcular_costo_total(horas, impuesto_pct, descuento_pct) -> Costo base + impuestos - descuento.
        """
        if impuesto_pct < 0 or descuento_pct < 0 or descuento_pct >= 100:
            raise CalculoInconsistenteError(f"Porcentajes inválidos: impuesto={impuesto_pct}%, descuento={descuento_pct}%.")

        subtotal = self.calcular_costo_base(duracion_horas)
        monto_descuento = subtotal * (descuento_pct / 100.0)
        base_gravable = subtotal - monto_descuento
        monto_impuesto = base_gravable * (impuesto_pct / 100.0)
        return round(base_gravable + monto_impuesto, 2)


class ReservaSala(Servicio):"""Servicio especializado para reserva de salas de reuniones o capacitación."""

    def __init__(self, codigo_id: str, nombre_servicio: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(codigo_id, nombre_servicio, tarifa_base, disponible)
        if capacidad <= 0: raise DatosInvalidosError("La capacidad de la sala debe ser mayor a 0 personas.")
        self._capacidad = capacidad

    def validar_parametros_operacion(self, duracion_horas: int) -> None:
        if duracion_horas < 1 or duracion_horas > 12:
            raise ReservaInvalidaError("Las salas solo se reservan entre 1 y 12 horas por jornada.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        self.validar_parametros_operacion(duracion_horas)
        # Aplica un recargo del 10% por limpieza si la sala supera las 4 horas de uso
        recargo = 1.10 if duracion_horas > 4 else 1.0
        return round(self.tarifa_base * duracion_horas * recargo, 2)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Sala [{self.codigo_id}]: {self.nombre_servicio} (Capacidad: {self._capacidad} pers.) - ${self.tarifa_base}/h [{estado}]"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de hardware y equipos tecnológicos."""

    def __init__(self, codigo_id: str, nombre_servicio: str, tarifa_base: float, cantidad_unidades: int, disponible: bool = True):
        super().__init__(codigo_id, nombre_servicio, tarifa_base, disponible)
        if cantidad_unidades < 1:
            raise DatosInvalidosError("Debe alquilarse al menos 1 unidad del equipo.")
        self._cantidad_unidades = cantidad_unidades

    def validar_parametros_operacion(self, duracion_horas: int) -> None:
        if duracion_horas < 2:
            raise ReservaInvalidaError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        self.validar_parametros_operacion(duracion_horas)
        return round(self.tarifa_base * duracion_horas * self._cantidad_unidades, 2)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Equipo [{self.codigo_id}]: {self.nombre_servicio} ({self._cantidad_unidades} unds.) - ${self.tarifa_base}/h [{estado}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría técnica e ingeniería de software."""

    def __init__(self, codigo_id: str, nombre_servicio: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(codigo_id, nombre_servicio, tarifa_base, disponible)
        if not especialidad or not especialidad.strip():
            raise DatosInvalidosError("Debe especificar el área de especialidad de la asesoría.")
        self._especialidad = especialidad.strip()

    def validar_parametros_operacion(self, duracion_horas: int) -> None:
        if duracion_horas <= 0 or duracion_horas > 8:
            raise ReservaInvalidaError("Las asesorías especializadas deben durar entre 1 y 8 horas.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        self.validar_parametros_operacion(duracion_horas)
        return round(self.tarifa_base * duracion_horas, 2)

    def obtener_resumen(self) -> str:
      estado = "Disponible" if self.disponible else "No disponible"
        return f"Asesoría [{self.codigo_id}]: {self.nombre_servicio} ({self._especialidad}) - ${self.tarifa_base}/h [{estado}]"


class Reserva(EntidadSistema):"""Integra Cliente, Servicio, duración y estado, gestionando el ciclo de vida de la reserva."""

    def __init__(self, codigo_id: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        super().__init__(codigo_id)
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere una instancia válida de Servicio.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ReservaInvalidaError(f"La duración en horas ({duracion_horas}) debe ser un entero positivo.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = "PENDIENTE"
        self._costo_final = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_final(self) -> float:
        return self._costo_final

    def procesar_y_confirmar(self, impuesto_pct: float = 19.0, descuento_pct: float = 0.0) -> None: """ Valida disponibilidad, calcula el costo total y confirma la reserva. Demuestra encadenamiento de excepciones (raise ... from e) exigido en la rúbrica. """
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError(f"No se puede confirmar la reserva {self.codigo_id} porque está CANCELADA.")

        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre_servicio}' no se encuentra disponible." )

        try:
            # Intenta calcular el costo mediante las reglas del servicio polimórfico
            self._costo_final = self._servicio.calcular_costo_total(self._duracion_horas, impuesto_pct, descuento_pct)
        except (ReservaInvalidaError, CalculoInconsistenteError) as error_calculo: # Encadenamiento formal de excepciones para preservar la traza del error original
            raise ReservaInvalidaError(f"Fallo al procesar la reserva {self.codigo_id} para '{self._servicio.nombre_servicio}'.") from error_calculo

        self._estado = "CONFIRMADA"
        GestorLogs.registrar_evento( "INFO",f"Reserva {self.codigo_id} CONFIRMADA | Cliente: {self._cliente.nombre} | Total: ${self._costo_final}",)

    def cancelar(self, motivo: str) -> None: """Cancela una reserva activa registrando formalmente el motivo."""
        if self._estado == "CANCELADA":  raise ReservaInvalidaError(f"La reserva {self.codigo_id} ya se encontraba cancelada.")
        self._estado = "CANCELADA"
        GestorLogs.registrar_evento("WARN", f"Reserva {self.codigo_id} CANCELADA. Motivo: {motivo}")

    def obtener_resumen(self) -> str:
        return ( f"Reserva [{self.codigo_id}] | Estado: {self._estado} | "f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre_servicio} | "f"Duración: {self._duracion_horas}h | Total: ${self._costo_final}")
