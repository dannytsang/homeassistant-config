import json
import logging

from homeassistant.helpers.typing import HomeAssistantType

_LOGGER = logging.getLogger(__name__)


class GameState:
    EVENT_ROUND_FREEZE = "csgo_round_freeze"
    EVENT_ROUND_STARTED = "csgo_round_started"
    EVENT_ROUND_ENDED = "csgo_round_ended"

    EVENT_BOMB_PLANTED = "csgo_bomb_planted"
    EVENT_BOMB_DEFUSED = "csgo_bomb_defused"
    EVENT_BOMB_EXPLODED = "csgo_bomb_exploded"

    EVENT_HEALTH_LOW = "csgo_health_low"
    EVENT_HEALTH_CRITICAL = "csgo_health_critical"

    EVENT_GAME_STOPPED = "csgo_game_stopped"

    def __init__(self, hass: HomeAssistantType):
        self._hass = hass

        self._round_state = None
        self._bomb_state = None
        self._health_state = None

    def load(self, data: str):
        data = json.loads(data)
        self._round_state = data["round_state"]
        self._bomb_state = data["bomb_state"]
        self._bomb_state = data["health_state"]

    def dump(self) -> str:
        return json.dumps(
            dict(round_state=self._round_state, bomb_state=self._bomb_state, health_state=self._health_state)
        )

    def update(self, data: dict):
        # handle active game state
        if "round" in data:
            if "phase" in data["round"]:
                self._check_round_state(value=data["round"]["phase"])
            if "bomb" in data["round"]:
                self._check_bomb_state(value=data["round"]["bomb"])
        if "player" in data:
            self._check_health_state(value=data["player"]["state"]["health"])
        # no game state submitted, must have ended
        else:
            self._reset()

    def _reset(self):
        if self._round_state or self._bomb_state:
            self._round_state = None
            self._bomb_state = None
            self._health_state = None
            self._fire_event(event=self.EVENT_GAME_STOPPED)

    def _check_round_state(self, value: str):
        # state hasn't changed
        if self._round_state == value:
            return

        # round status has changed so the bomb should reset
        self._bomb_state = None

        # report new state
        if value == "live":
            self._fire_event(event=self.EVENT_ROUND_STARTED)
        elif value == "freezetime":
            self._fire_event(event=self.EVENT_ROUND_FREEZE)
        elif value == "over":
            self._fire_event(event=self.EVENT_ROUND_ENDED)

        # remember current state
        self._round_state = value
    
    def _check_health_state(self, value: int):
        # state hasn't changed
        if self._health_state == value:
            return

        # report new state
        if value <= 30 and value > 10:
            self._fire_event(event=self.EVENT_HEALTH_LOW)
        elif value <= 10:
            self._fire_event(event=self.EVENT_HEALTH_CRITICAL)

        # remember current state
        self._health_state = value

    def _check_bomb_state(self, value: str):
        # state hasn't changed
        if self._bomb_state == value:
            return

        # report new state
        if value == "planted":
            self._fire_event(event=self.EVENT_BOMB_PLANTED)
        elif value == "defused":
            self._fire_event(event=self.EVENT_BOMB_DEFUSED)
        elif value == "exploded":
            self._fire_event(event=self.EVENT_BOMB_EXPLODED)

        # remember current state
        self._bomb_state = value

    def _fire_event(self, event: str):
        _LOGGER.debug(f"csgo fired event: {event}")
        self._hass.bus.async_fire(event)
