import csv
import os
import pymongo
import matplotlib.pyplot as plt

# Configuración de MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bd_escenarios_deportivos"]
collection = db["escenarios"]

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls')

def cargar_datos_csv():
    """Carga los datos del archivo CSV a MongoDB al inicio del programa."""
    try:
        # El archivo CSV debe estar en la misma carpeta que este script
        nombre_archivo = "escenarios_deportivos.csv"
        
        # Verificamos si el archivo existe
        if not os.path.exists(nombre_archivo):
            print(f"Error: El archivo {nombre_archivo} no se encuentra.")
            print("Asegúrate de que el archivo 'escenarios_deportivos.csv' esté en la misma carpeta que este script.")
            return False
        
        # Primero limpiamos la colección para evitar duplicados
        collection.delete_many({})
        
        # Abrimos el archivo y lo cargamos a MongoDB
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lector_csv = csv.DictReader(archivo)
            registros = list(lector_csv)
            
            if not registros:
                print("El archivo CSV está vacío o no tiene el formato correcto.")
                return False
            
            # Convertimos valores numéricos (latitud y longitud)
            for registro in registros:
                if 'Longitud' in registro:
                    try:
                        registro['Longitud'] = float(registro['Longitud'])
                    except:
                        registro['Longitud'] = 0
                
                if 'latitud' in registro:
                    try:
                        registro['latitud'] = float(registro['latitud'])
                    except:
                        registro['latitud'] = 0
            
            # Insertar los datos en MongoDB
            collection.insert_many(registros)
            print(f"Se cargaron {len(registros)} escenarios deportivos desde el archivo CSV.")
            return True
            
    except Exception as e:
        print(f"Error al cargar datos desde CSV: {e}")
        return False

def crear_registro():
    """Crea un nuevo registro de escenario deportivo en la base de datos."""
    limpiar_pantalla()
    try:
        print("CREAR NUEVO ESCENARIO DEPORTIVO")
        
        # Solicitar datos al usuario según la estructura del CSV
        tipo_escenario = input("Tipo de escenario: ")
        corregimiento_comuna = input("Corregimiento o comuna: ")
        vereda_barrio = input("Vereda o Barrio: ")
        nombre_barrio_vereda = input("Nombre barrio o vereda: ")
        nombre_escenario = input("Nombre escenario deportivo: ")
        direccion = input("Dirección: ")
        
        # Coordenadas (opcionales)
        try:
            longitud = float(input("Longitud (puede dejar en blanco): ") or "0")
            latitud = float(input("Latitud (puede dejar en blanco): ") or "0")
        except ValueError:
            longitud = 0
            latitud = 0
        
        # Crear documento con la estructura del CSV
        nuevo_escenario = {
            "Tipo de escenario": tipo_escenario,
            "Corregimiento o comuna": corregimiento_comuna,
            "Vereda o Barrio": vereda_barrio,
            "Nombre barrio o vereda": nombre_barrio_vereda,
            "Nombre escenario deportivo": nombre_escenario,
            "Dirección": direccion,
            "Longitud": longitud,
            "latitud": latitud,
            "georeferenciacion": f"POINT ({longitud} {latitud})"
        }
        
        # Insertar en MongoDB
        resultado = collection.insert_one(nuevo_escenario)
        print(f"¡Escenario deportivo creado correctamente!")
    except Exception as e:
        print(f"Error al crear escenario deportivo: {e}")
    
    input("\nPresiona Enter para volver al menú...")

def leer_registros():
    """Muestra todos los escenarios deportivos almacenados en la base de datos."""
    limpiar_pantalla()
    try:
        print("=== LISTA DE ESCENARIOS DEPORTIVOS ===")
        
        # Obtener todos los registros
        registros = list(collection.find())
        
        if not registros:
            print("No hay escenarios deportivos en la base de datos.")
        else:
            # Mostrar cada registro
            for i, registro in enumerate(registros, 1):
                print(f"\nEscenario #{i}:")
                print(f"Nombre: {registro.get('Nombre escenario deportivo', 'N/A')}")
                print(f"Ubicación: {registro.get('Corregimiento o comuna', 'N/A')}, {registro.get('Nombre barrio o vereda', 'N/A')}")
                print(f"Dirección: {registro.get('Dirección', 'N/A')}")
                print("-" * 40)
            
            print(f"\nTotal: {len(registros)} escenarios deportivos")
    except Exception as e:
        print(f"Error al leer escenarios deportivos: {e}")
    
    input("\nPresiona Enter para volver al menú...")

def actualizar_registro():
    """Actualiza un escenario deportivo existente."""
    limpiar_pantalla()
    try:
        print("=== ACTUALIZAR ESCENARIO DEPORTIVO ===")
        
        # Buscar por nombre para simplificar
        nombre_buscar = input("Ingresa el nombre del escenario deportivo a actualizar: ")
        registro = collection.find_one({"Nombre escenario deportivo": nombre_buscar})
        
        if not registro:
            print(f"No se encontró ningún escenario con el nombre '{nombre_buscar}'.")
        else:
            # Mostrar el registro encontrado
            print("\nEscenario encontrado:")
            print(f"Tipo: {registro.get('Tipo de escenario', 'N/A')}")
            print(f"Nombre: {registro.get('Nombre escenario deportivo', 'N/A')}")
            print(f"Ubicación: {registro.get('Corregimiento o comuna', 'N/A')}, {registro.get('Nombre barrio o vereda', 'N/A')}")
            print(f"Dirección: {registro.get('Dirección', 'N/A')}")
            
            # Preguntar qué campo actualizar
            print("\n¿Qué campo deseas actualizar?")
            print("1. Tipo de escenario")
            print("2. Dirección")
            print("3. Corregimiento o comuna")
            print("4. Nombre barrio o vereda")
            opcion = input("Selecciona una opción (1-4): ")
            
            # Actualizar el campo seleccionado
            if opcion == "1":
                nuevo_valor = input("Nuevo tipo de escenario: ")
                collection.update_one({"_id": registro["_id"]}, {"$set": {"Tipo de escenario": nuevo_valor}})
            elif opcion == "2":
                nuevo_valor = input("Nueva dirección: ")
                collection.update_one({"_id": registro["_id"]}, {"$set": {"Dirección": nuevo_valor}})
            elif opcion == "3":
                nuevo_valor = input("Nuevo corregimiento o comuna: ")
                collection.update_one({"_id": registro["_id"]}, {"$set": {"Corregimiento o comuna": nuevo_valor}})
            elif opcion == "4":
                nuevo_valor = input("Nuevo nombre de barrio o vereda: ")
                collection.update_one({"_id": registro["_id"]}, {"$set": {"Nombre barrio o vereda": nuevo_valor}})
            else:
                print("Opción no válida.")
                return
            
            print("\n¡Escenario deportivo actualizado correctamente!")
    except Exception as e:
        print(f"Error al actualizar escenario deportivo: {e}")
    
    input("\nPresiona Enter para volver al menú...")

def eliminar_registro():
    """Elimina un escenario deportivo de la base de datos."""
    limpiar_pantalla()
    try:
        print("=== ELIMINAR ESCENARIO DEPORTIVO ===")
        
        # Buscar por nombre para simplificar
        nombre_eliminar = input("Ingresa el nombre del escenario deportivo a eliminar: ")
        registro = collection.find_one({"Nombre escenario deportivo": nombre_eliminar})
        
        if not registro:
            print(f"No se encontró ningún escenario con el nombre '{nombre_eliminar}'.")
        else:
            # Mostrar el registro encontrado
            print("\nEscenario encontrado:")
            print(f"Tipo: {registro.get('Tipo de escenario', 'N/A')}")
            print(f"Nombre: {registro.get('Nombre escenario deportivo', 'N/A')}")
            print(f"Ubicación: {registro.get('Corregimiento o comuna', 'N/A')}, {registro.get('Nombre barrio o vereda', 'N/A')}")
            print(f"Dirección: {registro.get('Dirección', 'N/A')}")
            
            # Confirmar eliminación
            confirmacion = input("\n¿Estás seguro de que deseas eliminar este escenario? (s/n): ").lower()
            
            if confirmacion == "s":
                collection.delete_one({"_id": registro["_id"]})
                print("\n¡Escenario deportivo eliminado correctamente!")
            else:
                print("\nOperación cancelada.")
    except Exception as e:
        print(f"Error al eliminar escenario deportivo: {e}")
    
    input("\nPresiona Enter para volver al menú...")

def generar_grafico():
    """Genera un gráfico basado en los escenarios deportivos almacenados."""
    limpiar_pantalla()
    try:
        print("=== GENERAR GRÁFICO ===")
        
        # Verificar si hay datos
        if collection.count_documents({}) == 0:
            print("No hay datos para generar un gráfico.")
            input("\nPresiona Enter para volver al menú...")
            return
        
        print("¿Qué tipo de gráfico deseas generar?")
        print("1. Tipos de escenarios deportivos")
        print("2. Escenarios por comuna/corregimiento")
        opcion = input("Selecciona una opción (1-2): ")
        
        if opcion == "1":
            # Agrupar datos por tipo de escenario
            pipeline = [
                {"$group": {"_id": "$Tipo de escenario", "cantidad": {"$sum": 1}}}
            ]
            resultados = list(collection.aggregate(pipeline))
            
            # Preparar datos para el gráfico
            tipos = [r["_id"] for r in resultados]
            cantidades = [r["cantidad"] for r in resultados]
            
            # Crear gráfico de barras
            plt.figure(figsize=(12, 7))
            plt.bar(tipos, cantidades, color='skyblue')
            plt.title("Cantidad de Escenarios por Tipo", fontsize=16)
            plt.xlabel("Tipo de Escenario", fontsize=12)
            plt.ylabel("Cantidad", fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
        elif opcion == "2":
            # Agrupar datos por comuna/corregimiento
            pipeline = [
                {"$group": {"_id": "$Corregimiento o comuna", "cantidad": {"$sum": 1}}}
            ]
            resultados = list(collection.aggregate(pipeline))
            
            # Preparar datos para el gráfico
            ubicaciones = [r["_id"] for r in resultados]
            cantidades = [r["cantidad"] for r in resultados]
            
            # Crear gráfico de torta (pie)
            plt.figure(figsize=(10, 8))
            plt.pie(cantidades, labels=ubicaciones, autopct='%1.1f%%', startangle=90, shadow=True)
            plt.axis('equal')
            plt.title("Distribución de Escenarios por Ubicación", fontsize=16)
            plt.tight_layout()
            
        else:
            print("Opción no válida.")
            input("\nPresiona Enter para volver al menú...")
            return
        
        # Guardar gráfico
        nombre_archivo = "grafico_escenarios.png"
        plt.savefig(nombre_archivo)
        
        print(f"\nGráfico guardado como '{nombre_archivo}' en la carpeta actual.")
        print("Puedes abrirlo para ver los resultados.")
        
        # Cerrar el gráfico para liberar memoria
        plt.close()
        
    except Exception as e:
        print(f"Error al generar gráfico: {e}")
    
    input("\nPresiona Enter para volver al menú...")

def menu_principal():
    """Muestra el menú principal del sistema."""
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("     SISTEMA DE GESTIÓN DE ESCENARIOS DEPORTIVOS")
        print("=" * 60)
        print("1. Crear nuevo escenario deportivo")
        print("2. Ver todos los escenarios deportivos")
        print("3. Actualizar escenario deportivo")
        print("4. Eliminar escenario deportivo")
        print("5. Generar gráfico")
        print("0. Salir")
        print("=" * 60)
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            crear_registro()
        elif opcion == "2":
            leer_registros()
        elif opcion == "3":
            actualizar_registro()
        elif opcion == "4":
            eliminar_registro()
        elif opcion == "5":
            generar_grafico()
        elif opcion == "0":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    try:
        # Verificar conexión a MongoDB
        client.server_info()
        print("Conexión a MongoDB establecida correctamente.")
        
        # Cargar datos del CSV automáticamente al inicio
        datos_cargados = cargar_datos_csv()
        if datos_cargados:
            print("Datos de escenarios deportivos cargados correctamente desde el archivo CSV.")
        
        input("Presiona Enter para continuar al menú principal...")
        
        # Iniciar el menú principal
        menu_principal()
        
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Error: No se pudo conectar a MongoDB.")
        print("Asegúrate de que el servidor MongoDB esté en ejecución.")
        input("Presiona Enter para salir...")
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")