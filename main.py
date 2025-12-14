#!/usr/bin/env python3
"""
Главный файл игры "Neon Snake"
"""

from game import Game

if __name__ == "__main__":
    print("=" * 50)
    print("   N E O N   S N A K E ")
    print("=" * 50)
    print("\nУправление:")
    print("  Стрелки или WASD - движение")
    print("  ESC - пауза/меню")
    print("\nУровни сложности:")
    print("  1 - Легкий (медленно)")
    print("  2 - Средний (нормально)")
    print("  3 - Сложный (быстро)")
    print("\n" + "=" * 50)
    
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\nИгра прервана пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")
    finally:
        print("\nСпасибо за игру!")