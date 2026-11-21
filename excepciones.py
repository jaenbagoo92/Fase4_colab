"""Módulo de excepciones personalizadas para el sistema de gestión de Software FJ.
Permite identificar y controlar errores específicos del dominio del negocio.
Desarrollado para la Fase 4 de Programación Orientada a Objetos."""

# Clase base principal de la que heredan todas las excepciones personalizadas del negocio
class SoftwareFJError(Exception):
    """Clase base para todas las excepciones del sistema Software FJ."""
    pass


# Excepción disparada cuando los datos de entrada no cumplen con las validaciones
class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los datos ingresados (correo, documento, nombre, etc.) son inválidos o faltantes."""
    pass


# Excepción disparada ante intentos de usar o reservar recursos inactivos
class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar o usar un servicio inactivo o sin capacidad."""
    pass


# Excepción disparada cuando la lógica de la reserva presenta inconsistencias o fallas
class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva tiene duración inválida, estado inconsistente o falla en procesamiento."""
    pass


# Excepción disparada ante cálculos matemáticos o financieros incorrectos
class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando los parámetros de cálculo (descuentos, impuestos, tarifas) generan valores incoherentes."""
    pass
