# Sistema Integral de Gestión - Software FJ

**Curso:** Programación Orientada a Objetos - Fase 4 (Prácticas simuladas)  
**Modalidad:** Entrega individual  

## Descripción del Proyecto
Aplicación desarrollada en Python bajo una arquitectura orientada a objetos (sin bases de datos). Implementa:
- Abstracción y clases abstractas (`ABC`)
- Herencia y polimorfismo en servicios (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`)
- Encapsulación estricta con propiedades y validaciones
- Sobrecarga simulada mediante parámetros opcionales en cálculos de costos
- Manejo avanzado de excepciones (`try/except/else/finally`, excepciones personalizadas y encadenamiento con `raise ... from e`)
- Bitácora persistente de eventos y errores en `logs.txt`

## Estructura de Archivos
- `excepciones.py`: Excepciones personalizadas del dominio.
- `logger.py`: Gestor de logs en archivo plano.
- `modelos.py`: Clases de dominio y lógica de negocio.
- `main.py`: Controlador de ejecución secuencial con 10 operaciones simuladas.

## Instrucciones de Ejecución
Ejecute el script principal desde su terminal:
```bash
python main.py
