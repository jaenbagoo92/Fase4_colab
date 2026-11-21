"""Módulo encargado de gestionar la bitácora (logs) del sistema en un archivo de texto,
garantizando el registro continuo de eventos y excepciones sin detener la aplicación.
Documentado línea por línea para la Fase 4 de POO."""

from datetime import datetime


class GestorLogs:
    """Clase utilitaria para escribir eventos e incidencias en un archivo plano (logs.txt)."""

    # Nombre del archivo donde se almacenará el historial persistente de eventos y errores
  ARCHIVO_LOG = "logs.txt"

    @classmethod
    def registrar_evento(cls, tipo: str, mensaje: str, detalle_error: Exception = None) -> None:
        """ Registra una línea con marca de tiempo exacta en logs.txt.
        Utiliza try/except/finally para proteger la operación de entrada/salida (I/O) en disco. """
      
        # Obtiene la fecha y hora actual formateada para la trazabilidad
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Construye la estructura base del mensaje de registro
        linea = f"[{marca_tiempo}] [{tipo.upper()}] {mensaje}"
        
        # Si se pasa una excepción como parámetro, se adjuntan los detalles de la causa raíz
        if detalle_error: linea += f" | Causa: {type(detalle_error).__name__}: {detalle_error}"
            if detalle_error.__cause__: linea += f" (Encadenado desde: {type(detalle_error.__cause__).__name__}: {detalle_error.__cause__})"

        archivo = None
        try:
            # Intenta abrir el archivo en modo adición ('a') con codificación UTF-8 para no sobrescribir registros previos
            archivo = open(cls.ARCHIVO_LOG, mode="a", encoding="utf-8")
            # Escribe la línea generada seguida de un salto de línea archivo.write(linea + "\n")
        except OSError as error_io:
            # Captura cualquier falla del sistema operativo al escribir en disco para evitar que colapse la app
            print(f"CRÍTICO: No se pudo escribir en el archivo de logs: {error_io}")
        finally:
            # Bloque obligatorio que garantiza el cierre seguro del recurso de archivo si fue abierto con éxito
            if archivo is not None and not archivo.closed:
                archivo.close()
