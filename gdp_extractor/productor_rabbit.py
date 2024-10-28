import pika 

def enviar_mensajes():
    # Configurar la conexión
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Crear la cola
    channel.queue_declare(queue="notificaciones")
    
    # Enviar el mensaje
    message = "Nueva información disponible en la base de datos"
    channel.basic_publish(exchange='', routing_key='notificaciones', body=message)
    print("Mensaje enviado:", message)  # Mensaje de confirmación
    connection.close()

#enviar_mensajes()
