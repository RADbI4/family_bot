from pika_API.src.pika_handlers import RabbitMQHandler
import pika_API.src.const as c


def calendar_in_publish(msg, **kwargs):
    """
    Отправляет задание в очередь
    на создание и загрузку календарика.
    work_d_in
    :return:
    """
    queue = c.WorkDIn
    conn = c.RabbitMQ_conn.local_host
    with RabbitMQHandler.rabbit_connector(queue=queue, conn=conn) as agent:
        agent.publish_message(msg=msg, queue_cls=queue)


def google_drive_in_publish(msg, **kwargs):
    """
    Отправляет сообщение в очередь
    на загрузку zip архива на гугл диск.
    :param msg:
    :param kwargs:
    :return:
    """
    queue = c.GoogeCloudIn
    conn = c.RabbitMQ_conn.local_host
    with RabbitMQHandler.rabbit_connector(queue=queue, conn=conn) as agent:
        agent.publish_message(msg=msg, queue_cls=queue)


def yandex_drive_publish(msg, **kwargs):
    """
    Отправляет сообщение в очередь
    на загрузку документов на яндекс диск.
    :param msg:
    :param kwargs:
    :return:
    """
    queue = c.YaDiskIn
    conn = c.RabbitMQ_conn.local_host
    with RabbitMQHandler.rabbit_connector(queue=queue, conn=conn) as agent:
        agent.publish_message(msg=msg, queue_cls=queue)


if __name__ == '__main__':
    pass