class OuboxRelyWorker:

    def __init__(self):
        pass


    async def start(self):
        interval = 5 # or get from .ENV
        pass
    

    async def process_pending_events(self):
        # 1. Fetch PENDING events where scheduled_for <= now
        # 2. Try to publish to RabbitMQ/Broker
        # 3. If Success -> call command_service.mark_published()
        # 4. If Fail -> call command_service.handle_retry()
        pass


