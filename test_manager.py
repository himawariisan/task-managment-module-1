import pytest
from task_manager.manager import TaskManager
from task_manager.task import Task


@pytest.fixture
def temp_manager(tmp_path):
    """Створює TaskManager з тимчасовим файлом."""
    filepath = tmp_path / "tasks.txt"
    return TaskManager(str(filepath))

def test_task_creation():
    task = Task(1, "Купити молоко", 2)
    assert task.task_id == 1
    assert task.description == "Купити молоко"
    assert task.priority == 2
    assert task.completed is False
    assert isinstance(task.creation_date, str)

def test_task_mark_as_completed():
    task = Task(5, "Зробити домашку", 3)
    task.mark_as_completed()
    assert task.completed is True

def test_task_to_dict_and_from_dict():
    original = Task(10, "Тестове завдання", 1)
    data = original.to_dict()
    restored = Task.from_dict(data)

    assert restored.task_id == original.task_id
    assert restored.description == original.description
    assert restored.priority == original.priority
    assert restored.creation_date == original.creation_date
    assert restored.completed == original.completed

def test_add_task(temp_manager):
    task = temp_manager.add_task("Написати звіт", 3)
    assert task.task_id == 1
    assert len(temp_manager.tasks) == 1
    assert temp_manager.tasks[0].description == "Написати звіт"

def test_add_task_invalid_priority(temp_manager):
    with pytest.raises(ValueError):
        temp_manager.add_task("Неправильний пріоритет", 0)

    with pytest.raises(ValueError):
        temp_manager.add_task("Неправильний пріоритет", 6)

def test_delete_task(temp_manager):
    task = temp_manager.add_task("Видалити мене", 4)
    task_id = task.task_id
    
    temp_manager.delete_task(task_id)
    assert len(temp_manager.tasks) == 0

    with pytest.raises(KeyError):
        temp_manager.delete_task(999)

def test_list_tasks(temp_manager):
    temp_manager.add_task("Завдання A", 5)
    temp_manager.add_task("Завдання B", 1)
    temp_manager.add_task("Завдання C", 3)

    tasks = temp_manager.list_tasks(sort_by="priority")
    assert len(tasks) == 3
    assert tasks[0].priority == 1
    assert tasks[1].priority == 3
    assert tasks[2].priority == 5

def test_complete_and_remove_task(temp_manager):
    task = temp_manager.add_task("Виконати і видалити", 2)
    task_id = task.task_id

    completed_task = temp_manager.complete_and_remove_task(task_id)
    
    assert completed_task.completed is True
    assert len(temp_manager.tasks) == 0

    with pytest.raises(KeyError):
        temp_manager.complete_and_remove_task(999)


def test_persistence_between_managers(temp_manager):
    """Перевірка, що дані зберігаються у файл і завантажуються"""
    temp_manager.add_task("Постійне завдання", 4)
    
    new_manager = TaskManager(temp_manager.filepath)

    assert len(new_manager.tasks) == 1
    assert new_manager.tasks[0].description == "Постійне завдання"
    assert new_manager.tasks[0].priority == 4
