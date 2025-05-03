import pytest
from cleanup_helper_app.models.optimizer import solve_cleanup_plan


def test_solve_cleanup_plan_light_mode():
    detected_objects = [
        {"label": "Adhesive tape", "bbox": [0, 0, 10, 10], "center": (5, 5)},
        {"label": "Accordion", "bbox": [20, 20, 40, 40], "center": (30, 30)},
        {"label": "Unknown", "bbox": [50, 50, 60, 60], "center": (55, 55)},
    ]

    cost_table = {
        "Adhesive tape": 1,
        "Accordion": 3,
        # "Unknown"は cost_table に存在しない → デフォルト2
    }

    result = solve_cleanup_plan(detected_objects, cost_table, mode="light")

    # lightモードは最大5コストなので、全部入るかチェック
    total_cost = sum(obj["cost"] for obj in result)
    assert total_cost <= 5
    assert all("order" in obj for obj in result)
    assert result == sorted(result, key=lambda x: x["order"])


def test_solve_cleanup_plan_full_mode():
    detected_objects = [
        {"label": "Adhesive tape", "bbox": [0, 0, 10, 10], "center": (5, 5)},
        {"label": "Accordion", "bbox": [20, 20, 40, 40], "center": (30, 30)},
        {"label": "Unknown", "bbox": [50, 50, 60, 60], "center": (55, 55)},
    ]

    cost_table = {
        "Adhesive tape": 1,
        "Accordion": 3,
    }

    result = solve_cleanup_plan(detected_objects, cost_table, mode="full")

    total_cost = sum(obj["cost"] for obj in result)
    assert total_cost <= 15
    assert len(result) == 3  # fullなら全部入るはず
    assert all("order" in obj for obj in result)
    assert result == sorted(result, key=lambda x: x["order"])