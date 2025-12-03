"""样式管理模块"""


class DialogStyles:
    """对话框样式"""
    DIFFICULTY_WINDOW = """
        DifficultySelectionWindow {
            background: qlineargradient(
                x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #4CAF50,
                stop: 0.5 #8BC34A,
                stop: 1 #CDDC39
            );
        }
    """

    TITLE_LABEL = """
        QLabel {
            color: white;
            background-color: rgba(0, 0, 0, 120);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
        }
    """

    DESCRIPTION_LABEL = """
        QLabel {
            color: white;
            background-color: rgba(0, 0, 0, 80);
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    """

    DIFFICULTY_BUTTON = """
        QPushButton {{
            background-color: {color};
            border: 3px solid white;
            border-radius: 15px;
            padding: 15px;
            min-height: 100px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {color};
            border: 4px solid yellow;
            font-weight: bold;
        }}
        QPushButton:pressed {{
            background-color: {color};
            border: 2px solid white;
        }}
    """

    CANCEL_BUTTON = """
        QPushButton {
            background-color: rgba(255, 255, 255, 200);
            border: 2px solid #333;
            color: #333;
            padding: 12px 30px;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 255);
            border-color: #000;
        }
    """


class GameWindowStyles:
    """游戏窗口样式"""

    MAIN_BUTTON = """
        QPushButton {{
            background-color: {color};
            border: none;
            color: white;
            padding: 15px 25px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            margin: 4px 2px;
            border-radius: 10px;
            background-color: rgba({r}, {g}, {b}, 220);
            min-width: 180px;
        }}
        QPushButton:hover {{
            background-color: rgba({r}, {g}, {b}, 240);
        }}
    """

    GAME_BUTTON = """
        QPushButton {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            font-size: 12px;
            font-weight: bold;
            margin: 4px 2px;
            border-radius: 8px;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:disabled {
            background-color: #cccccc;
        }
    """

    BACK_BUTTON = """
        QPushButton {
            background-color: #2196F3;
            border: none;
            color: white;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            font-size: 12px;
            font-weight: bold;
            margin: 4px 2px;
            border-radius: 8px;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
    """

    INFO_LABEL = "color: white; padding: 8px 15px; background-color: rgba(0, 0, 0, 150); border-radius: 8px;"


class LeaderboardStyles:
    """排行榜样式"""
    TABLE_STYLE = """
    QTableWidget {
            background-color: rgba(255, 255, 255, 200);
                border: 2px solid #4CAF50;
                border-radius: 8px;
                gridline-color: #ddd;
                color: #333333;
            }
            QTableWidget::item {
                background-color: rgba(255, 255, 255, 200);
                color: #333333;
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }
            QTableWidget::item:selected {
                background-color: rgba(76, 175, 80, 150);
                color: white;
            }
            QHeaderView::section {
            background-color: #4CAF50;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #45a049;
            }
    """

    TITLE_STYLE = "color: white; background-color: rgba(0, 0, 0, 120); padding: 10px; border-radius: 10px;"

    CLOSE_BUTTON = """
        QPushButton {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            margin: 4px 2px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """