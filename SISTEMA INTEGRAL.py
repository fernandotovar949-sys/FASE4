import os
import logging
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================
LOG_FILENAME = "sistema_software_fj.log"
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ==========================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================
class SoftwareFJError(Exception):
    """Clase base para todas las excepciones del sistema."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando los datos del cliente no son válidos."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Excepción lanzada cuando un servicio presenta anomalías o no está disponible."""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Excepción lanzada al intentar procesar una reserva incorrecta o inconsistente."""
    pass


# ==========================================
# 3. CLASES ABSTRACTAS Y ENTIDADES GENERALES
# ==========================================
class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales del sistema."""
    
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Método abstracto para retornar los detalles de la entidad."""
        pass


class Cliente(EntidadBase):
    """Clase Cliente con validaciones robustas y encapsulación de datos personales."""
    
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"El nombre '{valor}' no es válido. Debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(f"El correo '{valor}' tiene un formato incorrecto.")
        self._correo = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ClienteInvalidoError(f"El teléfono '{valor}' no es válido (debe contener solo dígitos y mínimo 7 caracteres).")
        self._telefono = valor

    def obtener_detalles(self) -> str:
        return f"Cliente [ID: {self.identificador}] - Nombre: {self.nombre}, Correo: {self.correo}, Teléfono: {self.telefono}"

# ==========================================
# 4. JERARQUÍA DE SERVICIOS (POLIMORFISMO)
# ==========================================
class Servicio(EntidadBase, ABC):
    """Clase abstracta Servicio."""
    
    def __init__(self, identificador: str, nombre_servicio: str, costo_base: float):
        super().__init__(identificador)
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base

    @property
    def costo_base(self):
        return self._costo_base

    @costo_base.setter
    def costo_base(self, valor):
        if valor < 0:
            raise ServicioNoDisponibleError("El costo base no puede ser negativo.")
        self._costo_base = float(valor)

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método abstracto sobreescrito para calcular costos."""
        pass

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass


class ReservaSalas(Servicio):
    """Servicio especializado 1: Reserva de salas."""
    
    def __init__(self, identificador: str, costo_base: float, capacidad: int):
        super().__init__(identificador, "Reserva de Salas", costo_base)
        self.capacidad = capacidad

    def calcular_costo(self, horas: int, incluye_catering: bool = False) -> float:
        try:
            if horas <= 0:
                raise ValueError("El número de horas debe ser mayor a cero.")
            total = self.costo_base * horas
            if incluye_catering:
                total += 50.0  # Costo fijo por catering
            return total
        except Exception as e:
            raise ServicioNoDisponibleError(f"Error al calcular costo de sala: {e}") from e

    def obtener_detalles(self) -> str:
        return f"Servicio: Reserva de Salas | ID: {self.identificador} | Capacidad: {self.capacidad} personas | Tarifa Base: ${self.costo_base}"


class AlquilerEquipos(Servicio):
    """Servicio especializado 2: Alquiler de equipos tecnológicos."""
    
    def __init__(self, identificador: str, costo_base: float, tipo_equipo: str):
        super().__init__(identificador, "Alquiler de Equipos", costo_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias: int, seguro_activado: bool = True) -> float:
        try:
            if dias <= 0:
                raise ValueError("El número de días de alquiler debe ser mayor a cero.")
            total = self.costo_base * dias
            if seguro_activado:
                total += 20.0 * dias  # Costo de seguro diario
            return total
        except Exception as e:
            raise ServicioNoDisponibleError(f"Error al calcular costo de equipos: {e}") from e

    def obtener_detalles(self) -> str:
        return f"Servicio: Alquiler de Equipos | ID: {self.identificador} | Equipo: {self.tipo_equipo} | Tarifa Día: ${self.costo_base}"


class AsesoriasEspecializadas(Servicio):
    """Servicio especializado 3: Asesorías especializadas de software."""
    
    def __init__(self, identificador: str, costo_base: float, area_experticia: str):
        super().__init__(identificador, "Asesoría Especializada", costo_base)
        self.area_experticia = area_experticia

    def calcular_costo(self, sesiones: int, nivel_senior: bool = False) -> float:
        try:
            if sesiones <= 0:
                raise ValueError("El número de sesiones debe ser mayor a cero.")
            total = self.costo_base * sesiones
            if nivel_senior:
                total *= 1.35  Recargo del 35% por consultor senior
            return total
        except Exception as e:
            raise ServicioNoDisponibleError(f"Error al calcular costo de asesoría: {e}") from e

    def obtener_detalles(self) -> str:
        return f"Servicio: Asesoría | ID: {self.identificador} | Área: {self.area_experticia} | Tarifa Sesión: ${self.costo_base}"


# ==========================================
# 5. CLASE RESERVA
# ==========================================
class Reserva:
    """Clase Reserva que integra cliente, servicio, duración y estado."""
    
    contador_reservas = 1000

    def __init__(self, cliente: Cliente, servicio: Servicio, parametro_duracion: int):
        Reserva.contador_reservas += 1
        self.codigo_reserva = f"RES-{Reserva.contador_reservas}"
        self.cliente = cliente
        self.servicio = servicio
        self.parametro_duracion = parametro_duracion
        self.estado = "Creada"
        self.costo_total = 0.0

    def confirmar_reserva(self, *args, **kwargs):
        """Procesa y confirma la reserva aplicando manejo avanzado de excepciones."""
        try:
            logging.info(f"Iniciando procesamiento de reserva {self.codigo_reserva}")
            # Cálculo polimórfico del costo según el tipo de servicio
            self.costo_total = self.servicio.calcular_costo(self.parametro_duracion, *args, **kwargs)
            self.estado = "Confirmada"
            print(f"[EXITO] Reserva {self.codigo_reserva} confirmada con éxito. Costo Total: ${self.costo_total:.2f}")
            logging.info(f"Reserva {self.codigo_reserva} confirmada exitosamente. Total: ${self.costo_total:.2f}")
        
        except (ValueError, TypeError) as err:
            self.estado = "Fallida"
            error_msg = f"Parámetros inválidos en la reserva {self.codigo_reserva}: {err}"
            logging.error(error_msg)
            raise ReservaInvalidaError(error_msg) from err
        
        except SoftwareFJError as err:
            self.estado = "Fallida"
            error_msg = f"Error operativo en el servicio para la reserva {self.codigo_reserva}: {err}"
            logging.error(error_msg)
            raise
        
        else:
            # Se ejecuta únicamente si no hubo excepciones
            logging.info(f"Bloque ELSE ejecutado: La reserva {self.codigo_reserva} pasó las validaciones de costos correctamente.")
        
        finally:
            # Se ejecuta siempre, garantizando estabilidad
            print(f"[LOG SISTEMA] Operación de reserva {self.codigo_reserva} finalizada bajo estado: {self.estado}.\n")
            logging.info(f"Finalizó el ciclo de procesamiento para la reserva {self.codigo_reserva}. Estado final: {self.estado}")

    def cancelar_reserva(self):
        self.estado = "Cancelada"
        print(f"[INFO] La reserva {self.codigo_reserva} ha sido cancelada.")
        logging.warning(f"La reserva {self.codigo_reserva} fue cancelada por solicitud.")


# ==========================================
# 6. SIMULACIÓN DE 10 OPERACIONES COMPLETAS
# ==========================================
def ejecutar_simulacion():
    print("==================================================")
    print(" INICIO DE SIMULACIÓN DE OPERACIONES - SOFTWARE FJ")
    print("==================================================\n")
    
    # Listas internas para almacenamiento en memoria
    clientes = []
    servicios = []
    reservas = []

    # Operación 1: Registro válido de Cliente 1
    print("--- Operación 1: Registro Exitoso de Cliente ---")
    try:
        c1 = Cliente("C001", "Carlos Andrés Pérez", "carlos.perez@email.com", "3104567890")
        clientes.append(c1)
        print(c1.obtener_detalles())
    except Exception as e:
        print(f"Error capturado: {e}")

    # Operación 2: Registro inválido de Cliente (Provocando ClienteInvalidoError)
    print("\n--- Operación 2: Registro Fallido de Cliente (Datos Erróneos) ---")
    try:
        c_malo = Cliente("C002", "Ana", "correo_sin_arroba", "abc1234")
        clientes.append(c_malo)
    except ClienteInvalidoError as e:
        print(f"[EXCEPCIÓN CONTROLADA] {e}")

    # Operación 3: Creación correcta de Servicios especializados
    print("\n--- Operación 3: Creación Correcta de Servicios ---")
    try:
        s1 = ReservaSalas("S-101", 100.0, capacidad=15)
        s2 = AlquilerEquipos("S-102", 45.0, tipo_equipo="Servidor Rack")
        s3 = AsesoriasEspecializadas("S-103", 120.0, area_experticia="Arquitectura Cloud")
        servicios.extend([s1, s2, s3])
        for s in servicios:
            print(s.obtener_detalles())
    except Exception as e:
        print(f"Error: {e}")

    # Operación 4: Creación de servicio con error de costo negativo (ServicioNoDisponibleError)
    print("\n--- Operación 4: Creación de Servicio con Costo Inválido ---")
    try:
        s_malo = ReservaSalas("S-999", -50.0, capacidad=5)
    except ServicioNoDisponibleError as e:
        print(f"[EXCEPCIÓN CONTROLADA] {e}")

    # Operación 5: Reserva Exitosa 1 (Salas con catering)
    print("\n--- Operación 5: Procesamiento de Reserva Exitosa (Salas) ---")
    try:
        res1 = Reserva(clientes[0], servicios[0], parametro_duracion=4)
        res1.confirmar_reserva(incluye_catering=True)
        reservas.append(res1)
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Operación 6: Reserva Exitosa 2 (Alquiler de equipos con seguro)
    print("\n--- Operación 6: Procesamiento de Reserva Exitosa (Equipos) ---")
    try:
        # Registramos otro cliente válido primero
        c2 = Cliente("C002", "María Fernanda Gómez", "maria.gomez@email.com", "3209876543")
        clientes.append(c2)
        
        res2 = Reserva(c2, servicios[1], parametro_duracion=5)
        res2.confirmar_reserva(seguro_activado=True)
        reservas.append(res2)
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Operación 7: Reserva Exitosa 3 (Asesoría especializada Senior)
    print("\n--- Operación 7: Procesamiento de Reserva Exitosa (Asesoría) ---")
    try:
        res3 = Reserva(clientes[0], servicios[2], parametro_duracion=3)
        res3.confirmar_reserva(nivel_senior=True)
        reservas.append(res3)
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Operación 8: Intento de reserva fallida por duración negativa (Prueba try/except/else/finally)
    print("\n--- Operación 8: Reserva Fallida por Duración Negativa (Try-Except-Else-Finally) ---")
    try:
        res_fallida = Reserva(clientes[1], servicios[0], parametro_duracion=-2)
        res_fallida.confirmar_reserva(incluye_catering=False)
    except ReservaInvalidaError as e:
        print(f"[EXCEPCIÓN CAPTURADA EN FLUJO PRINCIPAL] {e}")

    # Operación 9: Cancelación controlada de una reserva existente
    print("\n--- Operación 9: Cancelación de una Reserva Registrada ---")
    try:
        reservas[1].cancelar_reserva()
    except Exception as e:
        print(f"Error al cancelar: {e}")

    # Operación 10: Intento de acceso a recurso nulo o parámetro faltante con encadenamiento
    print("\n--- Operación 10: Encadenamiento de Excepciones y Robustez de Datos ---")
    try:
        # Simulamos una operación forzando un error de tipo en cálculo
        servicio_prueba = servicios[1]
        # Pasamos un argumento de texto en lugar de entero para generar error controlado
        servicio_prueba.calcular_costo(dias="tres_dias")
    except ServicioNoDisponibleError as e:
        print(f"[EXCEPCIÓN ENCADENADA CAPTURADA] {e}")
        print(f"Causa raíz original: {e.__cause__}")

    print("\n==================================================")
    print(f" SIMULACIÓN FINALIZADA. Revise el archivo '{LOG_FILENAME}' para ver el registro de eventos.")
    print("==================================================")

if __name__ == "__main__":
    ejecutar_simulacion()

