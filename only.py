class StarCalculator:
    def __init__(self, mass=None, temperature=None, lifespan=None, spectral_type=None, metallicity=None):
        self.mass = mass
        self.temperature = temperature
        self.lifespan = lifespan
        self.spectral_type = spectral_type
        self.metallicity = metallicity if metallicity is not None else 1.0  # Defaulting to solar metallicity if not provided

    def calculate_properties(self):
        if self.mass:
            self.calculate_from_mass()
        elif self.temperature:
            self.calculate_from_temperature()
        elif self.spectral_type:
            self.calculate_from_spectral_type()
        else:
            raise ValueError("At least one property (mass, temperature, or spectral type) must be provided.")

    def calculate_from_mass(self):
        if not self.mass:
            raise ValueError("Mass must be provided to calculate other properties.")

        # More precise relations for main sequence stars:
        # Mass-luminosity relation: L/Lsun ~ (M/Msun)^3.5
        # Lifespan relation: T ~ (M/Msun)^-2.5 * 10 billion years for high mass stars,
        # but longer, more nuanced calculations for low mass stars
        
        self.temperature = 5800 * (self.mass ** 0.505)

        # Adjust lifespan for low-mass stars:
        if self.mass >= 0.43:
            self.lifespan = 10 * (self.mass ** -2.5)  # in billions of years
        else:
            # Low-mass stars (M dwarfs and below) can live trillions of years
            self.lifespan = 15 * (self.mass ** -1.8)  # Adjusted for L/T dwarfs and red dwarfs
        
        # Enhanced temperature-based spectral type classification
        self.spectral_type = self.determine_spectral_type_with_subclass(self.temperature)
        
        # Prompt user for metallicity if not provided
        if self.metallicity is None:
            self.metallicity = float(input("Enter metallicity (relative to solar units, e.g., 1.0 for solar metallicity): ") or 1.0)

    def calculate_from_temperature(self):
        if not self.temperature:
            raise ValueError("Temperature must be provided to calculate other properties.")
        
        # Estimate mass from temperature: M/Msun ~ (T/5800)^(1/0.505)
        self.mass = (self.temperature / 5800) ** (1 / 0.505)
        self.calculate_from_mass()

    def calculate_from_spectral_type(self):
        if not self.spectral_type:
            raise ValueError("Spectral type must be provided to calculate other properties.")

        spectral_type_dict = {
            'O': (20, 50000),  # More accurate data for O-type stars
            'B': (2.5, 25000),
            'A': (2.0, 10000),
            'F': (1.4, 7500),
            'G': (1.1, 5800),
            'K': (0.8, 4500),
            'M': (0.5, 3500),
            'L': (0.08, 2200),
            'T': (0.05, 1200)  # Adding brown dwarf classification
        }

        if self.spectral_type[0] in spectral_type_dict:
            base_mass, base_temp = spectral_type_dict[self.spectral_type[0]]
            subclass = int(self.spectral_type[1:]) if len(self.spectral_type) > 1 and self.spectral_type[1:].isdigit() else 0
            adjustment_factor = 1 + 0.01 * (5 - subclass)  # More detailed subclass scaling
            self.mass = base_mass * adjustment_factor  # Adjust mass based on subclass
            self.temperature = base_temp * adjustment_factor  # Adjust temperature based on subclass
            
            # Adjust lifespan specifically for low-mass stars
            if self.mass < 0.43:
                self.lifespan = 15 * (self.mass ** -1.8)  # For stars like L4V
            else:
                self.calculate_from_mass()
        else:
            raise ValueError("Unknown spectral type.")

    def determine_spectral_type_with_subclass(self, temperature):
        spectral_type = ""
        subclass = 0
        if temperature >= 60000:
            spectral_type = 'Wolf Rayet Star'
            subclass = 0
        elif 30000 <= temperature < 60000:
            spectral_type = 'O'
            subclass = min(9, int((60000 - temperature) // 3000))
        elif 10000 <= temperature < 30000:
            spectral_type = 'B'
            subclass = min(9, int((30000 - temperature) // 2000))
        elif 7500 <= temperature < 10000:
            spectral_type = 'A'
            subclass = min(9, int((10000 - temperature) // 250))
        elif 6000 <= temperature < 7500:
            spectral_type = 'F'
            subclass = min(9, int((7500 - temperature) // 150))
        elif 5200 <= temperature < 6000:
            spectral_type = 'G'
            subclass = min(9, int((6000 - temperature) // 80))
        elif 3700 <= temperature < 5200:
            spectral_type = 'K'
            subclass = min(9, int((5200 - temperature) // 150))
        elif 2400 <= temperature < 3700:
            spectral_type = 'M'
            subclass = min(9, int((3700 - temperature) // 130))
        elif 1300 <= temperature < 2400:
            spectral_type = 'L'
            subclass = min(9, int((2400 - temperature) // 100))
        elif 600 <= temperature < 1300:
            spectral_type = 'T'
            subclass = min(9, int((1300 - temperature) // 70))
        else:
            spectral_type = 'Below T type (Y dwarf or planet)'
            subclass = ''
        
        return f"{spectral_type}{subclass}"

    def display_properties(self):
        return {
            'Mass (in Solar masses)': round(self.mass, 3),
            'Temperature (K)': round(self.temperature, 2),
            'Lifespan (billion years)': round(self.lifespan, 3),
            'Spectral Type': self.spectral_type,
            'Metallicity (Solar units)': round(self.metallicity, 2)
        }

# Example usage
mass_input = float(input("Enter mass in solar masses (or leave blank): ") or 0)
temperature_input = float(input("Enter temperature in Kelvin (or leave blank): ") or 0)
spectral_type_input = input("Enter spectral type (or leave blank): ").strip().upper() or None
metallicity_input = input("Enter metallicity (relative to solar units, or leave blank for default 1.0): ").strip()
metallicity_input = float(metallicity_input) if metallicity_input else None

calc = StarCalculator(
    mass=mass_input if mass_input > 0 else None,
    temperature=temperature_input if temperature_input > 0 else None,
    spectral_type=spectral_type_input,
    metallicity=metallicity_input
)

calc.calculate_properties()
print(calc.display_properties())
