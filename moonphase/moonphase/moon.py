from skyfield.api import load
import calendar

def get_moon_phase(year, month, day):
    eph = load('de421.bsp')
    ts = load.timescale()

    t_today = ts.utc(year, month, day)
    t_next = ts.utc(year, month, day + 1)

    earth = eph['earth']
    moon = eph['moon']
    sun = eph['sun']

    # Get elongation (angular separation) today
    angle = earth.at(t_today).observe(moon).apparent().separation_from(
        earth.at(t_today).observe(sun).apparent()
    ).degrees

    # Get vector from Earth to Moon and Earth to Sun
    r_moon = earth.at(t_today).observe(moon).apparent().position.km
    r_sun = earth.at(t_today).observe(sun).apparent().position.km

    # Dot product method to determine waxing or waning
    dot = sum(m * s for m, s in zip(r_moon, r_sun))
    waxing = dot < 0  # Negative dot = waxing, Positive = waning

    # Determine moon phase
    if angle < 22.5:
        phase = 'New Moon'
        emoji = '🌑'
    elif angle < 67.5:
        phase = 'Waxing Crescent' if waxing else 'Waning Crescent'
        emoji = '🌒' if waxing else '🌘'
    elif angle < 112.5:
        phase = 'First Quarter' if waxing else 'Last Quarter'
        emoji = '🌓' if waxing else '🌗'
    elif angle < 157.5:
        phase = 'Waxing Gibbous' if waxing else 'Waning Gibbous'
        emoji = '🌔' if waxing else '🌖'
    else:
        phase = 'Full Moon'
        emoji = '🌕'

    return {
        'phase': phase,
        'angle': round(angle, 2),
        'emoji': emoji,
        'Dtoday': f' {day} {calendar.month_name[month]}, {year}'
    }