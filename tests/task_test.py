import sys
sys.path.append("..")
from app.utils import task

taskid = task.generate_task_id()
task.add(taskid, "task")

print(task.get(taskid))
try:
    task.get("task-1111")
except Exception as e:
    print(f"can not find {e}")

task.delete(taskid)
print(task.get(taskid))
try:
    task.get("task-1111")
except Exception as e:
    print(f"can not find {e}")