"""AudioDeviceService — thin wrapper over sounddevice for output checks."""

from __future__ import annotations

import sounddevice as sd


class AudioDeviceService:
    def has_output_device(self) -> bool:
        try:
            return any(d["max_output_channels"] > 0 for d in sd.query_devices())
        except Exception:
            return False

    def default_sample_rate(self) -> int:
        try:
            return int(sd.query_devices(kind="output")["default_samplerate"])
        except Exception:
            return 48000