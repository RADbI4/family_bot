import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='g_cloud_in')


def publish_g_cloud_in(data):
    """
    Отправляет сообщение в очередь g_cloud_in.
    :param f_data: файл
    :return:
    """
    channel.basic_publish(exchange='', routing_key='g_cloud_in', body=data)
