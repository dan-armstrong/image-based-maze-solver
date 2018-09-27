import math

space_permittivity = 8.85418782 * 10**(-12)
magnetic_permeability = 4 * math.pi * 10**(-7)

def light_speed(fsp, mp, T):
    rp = 3*(1+(T-300)/100)
    return math.sqrt(1 / (fsp*mp*rp))

speed = light_speed(space_permittivity, magnetic_permeability, 400)
print(speed)
