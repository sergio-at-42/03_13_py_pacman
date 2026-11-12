from __future__ import annotations
import pygame

from .config import Config
from .sprite_image import SpPacman, SpBlinky, SpPinky, SpInky, SpClyde, SpBomb, SpItem

class Instruction():

    window:pygame.Surface
    background: pygame.Surface
    instruction_area:pygame.Surface

    title: str = "I N S T R U C T I O N S"
    description: str = "The player controls Pac-Man within a maze, aiming to eat all the pacgums,\n while contending with four ghosts, each with distinct behaviors."
    items: list[dict[str, str]] = [
        {"image": f"{Config.image_directory}{SpPacman.spe1}", "label": "Pac-Man", "description": "The great Pac-Man since 1980."},
        {"image": f"{Config.image_directory}{SpBlinky.spe0}", "label": "Blinky", "description": "The direct pursuer."},
        {"image": f"{Config.image_directory}{SpPinky.spe0}", "label": "Pinky", "description": "The ambusher that attempts to anticipate the player's path."},
        {"image": f"{Config.image_directory}{SpInky.spe0}", "label": "Inky", "description": "Characterized by more unpredictable or erratic behavior."},
        {"image": f"{Config.image_directory}{SpClyde.spe0}", "label": "Clyde", "description": "Alternates between pursuing the player\n and moving away randomly."},
        {"image": f"{Config.image_directory}{SpItem.spgum}", "label": "Pacgum", "description": "Eat all the pacgums to finish the level."},
        {"image": f"{Config.image_directory}{SpItem.spsuper}", "label": "SuperPacgum", "description": "These allow Pac-Man to temporarily become\n the predator, enabling him to eat the ghosts."},
        {"image": f"{Config.image_directory}{SpBomb.sp0}", "label": "Bomb", "description": "Destroys all ghosts within a certain radius."},
    ]
    cheat_title: str = "C H E A T   M O D E"
    cheats: list[dict[str, str]] = [
        {"key": "SPACE", "description": "Give a little speed boost to Pac-Man."},
        {"key": "X", "description": "Put a bomb to Pac-Man position."},
        {"key": "R", "description": "Ghosts moving away randomly."},
        {"key": "F", "description": "Ghosts enter a frightened state."},
        {"key": "D", "description": "Kill all Ghosts."},
        {"key": "S", "description": "Ghosts fall asleep."},
        {"key": "C", "description": "Ghosts enter in a chase mode."},
        {"key": "L", "description": "Move to the next level."},
    ]

    @classmethod
    def display(cls) -> None:
        from .session import Session
        from .game import Game
        Instruction.items: list[dict[str, str]] = [
                {"image": f"{Config.image_directory}{SpPacman.spe1}", "label": "Pac-Man", "description": "The great Pac-Man since 1980."},
                {"image": f"{Config.image_directory}{SpBlinky.spe0}", "label": "Blinky", "description": "The direct pursuer."},
                {"image": f"{Config.image_directory}{SpPinky.spe0}", "label": "Pinky", "description": "The ambusher that attempts to anticipate the player's path."},
                {"image": f"{Config.image_directory}{SpInky.spe0}", "label": "Inky", "description": "Characterized by more unpredictable or erratic behavior."},
                {"image": f"{Config.image_directory}{SpClyde.spe0}", "label": "Clyde", "description": "Alternates between pursuing the player\n and moving away randomly."},
                {"image": f"{Config.image_directory}{SpItem.spgum}", "label": "Pacgum", "description": "Eat all the pacgums to finish the level."},
                {"image": f"{Config.image_directory}{SpItem.spsuper}", "label": "SuperPacgum", "description": "These allow Pac-Man to temporarily become\n the predator, enabling him to eat the ghosts."},
                {"image": f"{Config.image_directory}{SpBomb.sp0}", "label": "Bomb", "description": "Destroys all ghosts within a certain radius."},
            ]

        Instruction.window = Session.session.window
        # set background area
        Instruction.background = pygame.Surface(Instruction.window.get_size(), pygame.SRCALPHA)
        bg: pygame.image = pygame.image.load(f"{Config.instruction_bg}")
        Instruction.background.blit(bg, ((Instruction.background.get_width() - bg.get_width()) // 2, 0))
        # set instruction area
        Instruction.instruction_area = pygame.Surface((864, 960), pygame.SRCALPHA)
        Instruction.instruction_area.fill((0, 0, 48, 208))
        font_64 = pygame.font.Font(None, 64) # 44 pixels
        font_32 = pygame.font.Font(None, 32)
        # display title
        y = 36
        text = font_64.render(Instruction.title, True, (255, 127, 0))
        Instruction.instruction_area.blit(text, ((Instruction.instruction_area.get_width() - text.get_width()) // 2, y))
        # display description
        y += 72
        for line in Instruction.description.split("\n"):
            text = font_32.render(line, True, (255, 127, 0))
            Instruction.instruction_area.blit(text, (Instruction.instruction_area.get_width() // 2 - 400, y))
            y += 36
        # display items
        y += 36
        for item in Instruction.items:
            image = pygame.image.load(item["image"]).convert_alpha()
            Instruction.instruction_area.blit(image, (Instruction.instruction_area.get_width() // 2 - 400, y))
            text = font_32.render(item["label"], True, (255, 255, 0))
            Instruction.instruction_area.blit(text, (Instruction.instruction_area.get_width() // 2 - 400 + 48, y))
            for line in item["description"].split("\n"):
                text = font_32.render(line, True, (255, 255, 0))
                Instruction.instruction_area.blit(text, (Instruction.instruction_area.get_width() // 2 + 400 - text.get_width(), y))
                y += 36
        # display cheats
        y += 36
        text = font_32.render(Instruction.cheat_title, True, (255, 127, 0))
        Instruction.instruction_area.blit(text, ((Instruction.instruction_area.get_width() - text.get_width()) // 2, y))
        y += 36
        for cheat in Instruction.cheats:
            text = font_32.render(f"< {cheat["key"]} >", True, (255, 255, 0))
            Instruction.instruction_area.blit(text, (Instruction.instruction_area.get_width() // 2 - 400, y))
            text = font_32.render(cheat["description"], True, (255, 255, 0))
            Instruction.instruction_area.blit(text, (Instruction.instruction_area.get_width() // 2 + 400 - text.get_width(), y))
            y += 36
        # display areas in window
        Instruction.window.blit(Instruction.background, (0, 0))
        Instruction.window.blit(Instruction.instruction_area, ((Instruction.window.get_width() - Instruction.instruction_area.get_width()) // 2, 64))
        pygame.display.flip()
        Game.waiting_loop()
