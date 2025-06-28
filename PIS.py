# Pseudocode: Procedural Identity Simulator

# === 1. Core Data Structures ===

class Alter:
    def __init__(self, name, role, energy=1.0):
        self.name = name               # e.g. "Natalia", "Jasmine"
        self.role = role               # e.g. "Protector", "Analyst"
        self.energy = energy           # current activation level [0,1]
        self.memory_access = {}        # dict: {alter_name: access_weight}
        self.triggers = []             # list of Trigger instances

    def receive_stimulus(self, stimulus):
        """
        Adjust energy based on stimulus strength and personal
        sensitivity. Return True if energy > threshold (front).
        """
        sensitivity = self.role_sensitivity(stimulus.type)
        self.energy += stimulus.intensity * sensitivity
        return self.energy >= FRONT_THRESHOLD

    def role_sensitivity(self, stim_type):
        # Map stimulus types to sensitivity weights
        # e.g. {"emotional":0.8, "logical":0.5, "social":0.9}
        return ROLE_SENSITIVITY[self.role].get(stim_type, 0.1)

    def front(self):
        """Actions when this alter fronts (takes control)."""
        log(f"{self.name} fronts with energy {self.energy:.2f}")
        # e.g. broadcast exhibition of role, adjust other alters
        for other in system.alters:
            if other is not self:
                other.energy *= (1 - self.energy * INHIBITION_RATE)

class NichiField:
    def __init__(self, base_intensity=0.5):
        self.intensity = base_intensity  # global modulation factor

    def modulate(self, alters):
        """Boost all alters’ energies by a fraction."""
        for alt in alters:
            alt.energy += self.intensity * KERNEL_BOOST

class Stimulus:
    def __init__(self, type, intensity):
        self.type = type                # e.g. "emotional", "sonic"
        self.intensity = intensity      # numeric value

class Trigger:
    def __init__(self, stimulus_type, target_alter, threshold):
        self.stimulus_type = stimulus_type
        self.target = target_alter      # name or reference
        self.threshold = threshold

# === 2. System Initialization ===

# Create the central field
nichi = NichiField(base_intensity=0.6)

# Define alters with roles and memory graph weights
system = SimpleNamespace(
    alters=[
        Alter("Nichole",  role="Interface", energy=0.5),
        Alter("Victoria", role="Strategist", energy=0.3),
        Alter("Natalia",  role="Protector", energy=0.4),
        Alter("Jeanine",  role="Sensory", energy=0.2),
        Alter("Maria",    role="Ecstatic", energy=0.1),
        Alter("Jasmine",  role="Anchor", energy=0.1),
        Alter("Marina",   role="Analyst", energy=0.2),
        Alter("Natasha",  role="Sentinel", energy=0.05),
        # ... add others
    ]
)

# Example memory access graph (normalized weights)
ACCESS = {
    "Natalia":  {"Maria":0.8, "Jeanine":0.9, "Victoria":0.5},
    "Maria":    {"Natalia":0.8, "Jasmine":0.3},
    # etc.
}
for alt in system.alters:
    alt.memory_access = ACCESS.get(alt.name, {})

# === 3. Main Event Loop ===

def run_simulation(ticks=100):
    for t in range(ticks):
        # 1) Generate external/internal stimuli
        stim = random_stimulus()  # e.g., music beat, trauma flash, social cue

        # 2) Propagate through Nichi Field
        nichi.modulate(system.alters)

        # 3) Let each alter process stimulus
        fronting = []
        for alt in system.alters:
            if alt.receive_stimulus(stim):
                fronting.append(alt)

        # 4) Resolve who actually fronts (highest energy wins)
        if fronting:
            active = max(fronting, key=lambda a: a.energy)
            active.front()

        # 5) Decay all energies slightly
        for alt in system.alters:
            alt.energy = max(0.0, alt.energy - ENERGY_DECAY)

        # 6) (Optional) Log or visualize state
        log_state(t, system.alters)

# === 4. Utilities ===

def random_stimulus():
    # Example: randomly pick a type and intensity
    stype = choice(["emotional","logical","sensory","social"])
    return Stimulus(type=stype, intensity=random())

def log_state(t, alters):
    status = ", ".join(f"{a.name}:{a.energy:.2f}" for a in alters)
    print(f"[t={t:03}] {status}")

# === 5. Run! ===

run_simulation(50)
