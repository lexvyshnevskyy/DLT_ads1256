import logging
from typing import Dict, Optional

from pipyadc import ADS1256
from pipyadc.ADS1256_definitions import DRATE_10, NEG_AIN1, NEG_AIN3, NEG_AINCOM, POS_AIN0, POS_AIN2, POS_AIN4

from . import waveshare_config
from .converters import lm335_kelvin_direct

logging.basicConfig(level=logging.INFO)


class TempFilter:
    """Simple exponential moving average filter."""

    def __init__(self, alpha: float = 0.2) -> None:
        self.alpha = alpha
        self.y = None

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
        self.temp_filter = TempFilter(alpha=0.15)
        self.data: Optional[Dict[str, float]] = None
        self.ads = ADS1256(waveshare_config)
        self.ads.pga = 1
        self.ads.drate = DRATE_10
        self.ads.cal_self()

    def poll_data(self) -> Dict[str, float]:
        raw_channels = self.ads.read_sequence(CH_SEQUENCE)

        data = {f'AIN{i}': int(value) for i, value in enumerate(raw_channels)}
        data.update({
            f'ch{i}': self.temp_filter.update(lm335_kelvin_direct(value * self.ads.v_per_digit)) if i == 2 else float(value * self.ads.v_per_digit)
            for i, value in enumerate(raw_channels)
        })
        self.data = data
        return data
