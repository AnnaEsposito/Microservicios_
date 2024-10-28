import pika

def recibir_mensaje():
    # Configurar la conexión
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notificaciones')
    
    def callback(ch, method, properties, body):
        print(f"Mensaje recibido: {body.decode()}")  # Decodificar si es necesario
    
    # Mensaje de confirmación de espera
    print('Esperando mensajes...')
    channel.basic_consume(queue='notificaciones', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

recibir_mensaje()
