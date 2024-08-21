# gunicorn.conf.py

def worker_exit(server, worker):
    print('Server is shutting down...')
    try:
        if hasattr(worker, 'app') and hasattr(worker.app, 'mongo_io'):
            worker.app.mongo_io.disconnect()
            print('MongoDB connection closed.')
        else:
            print('MongoIO instance not found.')
    except Exception as e:
        print(f'Error during shutdown: {e}')