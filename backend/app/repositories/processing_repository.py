from app.models.processing_log import ProcessingLog


class ProcessingRepository:

    def __init__(self, db):
        self.db = db

    def create(self, user_id, time, accuracy):
        log = ProcessingLog(
            user_id=user_id,
            processing_time=time,
            accuracy=accuracy
        )
        self.db.add(log)
        self.db.commit()

    def get_user_stats(self, user_id):
        logs = self.db.query(ProcessingLog).filter_by(user_id=user_id).all()

        if not logs:
            return {
                "processed": 0,
                "avg_time": 0,
                "avg_accuracy": 0
            }

        processed = len(logs)
        avg_time = sum(l.processing_time for l in logs) / processed
        avg_accuracy = sum(l.accuracy for l in logs) / processed

        return {
            "processed": processed,
            "avg_time": avg_time,
            "avg_accuracy": avg_accuracy
        }
