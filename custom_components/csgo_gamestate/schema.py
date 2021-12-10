import voluptuous as vol


WEBHOOK_SCHEMA = vol.Schema(
    {
        vol.Optional("round"): vol.Schema(
            {
                vol.Optional("phase"): vol.Any("live", "freezetime", "over"),
                vol.Optional("bomb"): vol.Any("planted", "defused", "exploded"),
                vol.Optional("win_team"): vol.Any("CT", "T"),
            },
            extra=vol.ALLOW_EXTRA,
        ),
        vol.Optional("player"): vol.Schema(
            {
                vol.Optional("state"): vol.Schema(
                    {
                        vol.Optional("health"): vol.Any(int),
                        vol.Optional("flashed"): vol.Any(int),
                    },
                    extra=vol.ALLOW_EXTRA,
                ),
            },
            extra=vol.ALLOW_EXTRA,
        ),
    },
    extra=vol.ALLOW_EXTRA,
)
