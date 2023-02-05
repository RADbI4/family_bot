import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='work_d_in')


def publish_to_work_days(date):
    """
    Отправляет сообщение в очередь work_d_in.
    :param date: [29, 1, '2023]
    :return:
    """
    channel.basic_publish(exchange='', routing_key='work_d_in', body=date)
