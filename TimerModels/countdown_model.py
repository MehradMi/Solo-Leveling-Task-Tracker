import time
from dataclasses import dataclass
from typing import List

@dataclass
class CountdownTimer:
    """Countdown Timer Model"""
    countdown_time_in_seconds = int

    def compute_countdown_time_in_seconds(self, given_countdown_time: List):
        """Convert the user provided time to seconds"""
        computed_countdown_time_in_seconds = int(given_countdown_time[0]) * 3600 + int(given_countdown_time[1]) * 60 + int(given_countdown_time[2])
        self.countdown_time_in_seconds = computed_countdown_time_in_seconds

    def set_countdown_time(self):
        """User enters the amount of time and we set the countdown timer"""
        for x in range(self.countdown_time_in_seconds, 0, -1):
            seconds = x % 60
            minuts = int(x / 60) % 60
            hours = int(x / 3600)

            print(f"{hours:02}:{minuts:02}:{seconds:02}")
            time.sleep(1)