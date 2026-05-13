from __future__ import annotations

import math
import time
from typing import Dict, Optional

from .converters import lm335_kelvin_direct


try:
    from pipyadc import ADS1256
    from pipyadc.ADS1256_definitions import (
        DRATE_10,
        NEG_AIN1,
        NEG_AIN3,
        NEG_AINCOM,
        POS_AIN0,
        POS_AIN2,
        POS_AIN4,
    )
    PIPYADC_AVAILABLE = True
except Exception as exc:  # pragma: no cover - hardware dependency
    ADS1256 = None
    DRATE_10 = None
    NEG_AIN1 = NEG_AIN3 = NEG_AINCOM = 0
    POS_AIN0 = POS_AIN2 = POS_AIN4 = 0
    PIPYADC_AVAILABLE = False
    PIPYADC_IMPORT_ERROR = exc
else:
    PIPYADC_IMPORT_ERROR = None


class TempFilter:
    """Simple exponential moving average filter."""

    def __init__(self, alpha: float = 0.2) -> None:
        self.alpha = alpha
        self.y: Optional[float] = None

    def update(self, x: float) -> float:
        if self.y is None:
            self.y = x
        else:
            self.y = self.alpha * x + (1.0 - self.alpha) * self.y
        return self.y


AIN0_AIN1 = POS_AIN0 | NEG_AIN1
AIN2_AIN3 = POS_AIN2 | NEG_AIN3
AIN4_AINCOM = POS_AIN4 | NEG_AINCOM

CH_SEQUENCE = [
    AIN0_AIN1,
    AIN2_AIN3,
    AIN4_AINCOM,
]


class AdsData:
    def __init__(self) -> None:
        if not PIPYADC_AVAILABLE or ADS1256 is None:
            raise RuntimeError(f'pipyadc is not available: {PIPYADC_IMPORT_ERROR}')

        # Import only after pipyadc is confirmed available.
        # waveshare_config itself imports pipyadc definitions.
        from . import waveshare_config

        self.temp_filter = TempFilter(alpha=0.15)
        self.data: Optional[Dict[str, float]] = None
        self.ads = ADS1256(waveshare_config)
        self.ads.pga = 1
        self.ads.drate = DRATE_10
        self.ads.cal_self()

    def poll_data(self) -> Dict[str, float]:
        raw_channels = self.ads.read_sequence(CH_SEQUENCE)

        data: Dict[str, float] = {}
        for i in range(8):
            raw_value = int(raw_channels[i]) if i < len(raw_channels) else 0
            volts = float(raw_value * self.ads.v_per_digit) if i < len(raw_channels) else 0.0
            data[f'AIN{i}'] = raw_value
            if i == 2:
                data[f'ch{i}'] = self.temp_filter.update(lm335_kelvin_direct(volts))
            else:
                data[f'ch{i}'] = volts

        self.data = data
        return data


class SimulatedAdsData:
    """Demo data source for integration testing without ADS1256 hardware."""

    def __init__(self) -> None:
        self.started = time.monotonic()

    def poll_data(self) -> Dict[str, float]:
        t = time.monotonic() - self.started
        data: Dict[str, float] = {}
        for i in range(8):
            raw = int(100000 + 1000 * i + 5000 * math.sin(t + i * 0.4))
            data[f'AIN{i}'] = raw
            data[f'ch{i}'] = raw / 1000000.0

        # Keep channel 2 shaped like a Kelvin temperature for HMI/testing.
        data['ch2'] = 295.0 + 2.0 * math.sin(t / 5.0)
        return data
