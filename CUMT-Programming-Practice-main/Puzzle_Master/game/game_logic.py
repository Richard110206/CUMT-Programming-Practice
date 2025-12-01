import json
import os
from PyQt5.QtCore import QDate


class GameLogic:
    """游戏逻辑管理"""

    @staticmethod
    def save_to_leaderboard(time, steps):
        """保存到排行榜"""
        record = {
            "time": time,
            "steps": steps,
            "date": QDate.currentDate().toString("yyyy-MM-dd")
        }

        leaderboard_data = []
        if os.path.exists("leaderboard.json"):
            try:
                with open("leaderboard.json", "r", encoding="utf-8") as f:
                    leaderboard_data = json.load(f)
            except:
                pass

        leaderboard_data.append(record)

        try:
            with open("leaderboard.json", "w", encoding="utf-8") as f:
                json.dump(leaderboard_data, f, ensure_ascii=False, indent=2)
        except:
            pass

    @staticmethod
    def load_leaderboard():
        """加载排行榜数据"""
        leaderboard_data = []
        if os.path.exists("leaderboard.json"):
            try:
                with open("leaderboard.json", "r", encoding="utf-8") as f:
                    leaderboard_data = json.load(f)
                leaderboard_data.sort(key=lambda x: x["time"])
            except:
                leaderboard_data = []
        return leaderboard_data

    @staticmethod
    def is_puzzle_complete(current_indices, original_indices):
        """检查拼图是否完成"""
        return current_indices == original_indices

    @staticmethod
    def exchange_pieces(pieces, current_indices, source_index, target_index):
        """交换两个拼图块"""
        source_pos = current_indices.index(source_index)
        target_pos = current_indices.index(target_index)

        current_indices[source_pos], current_indices[target_pos] = \
            current_indices[target_pos], current_indices[source_pos]

        pieces[source_pos].index = current_indices[source_pos]
        pieces[target_pos].index = current_indices[target_pos]

        return source_pos, target_pos