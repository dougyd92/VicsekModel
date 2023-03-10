from configparser import ConfigParser
from datetime import datetime
from typing import Any

from matplotlib.animation import FFMpegWriter, FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

class Agent:
  def __init__(
    self,
    width: int,
    height: int,
    speed: float
  ) -> None:
    self.x = width * np.random.rand()
    self.y = height * np.random.rand()
    self.speed = speed
    self.heading = 2 * np.pi * np.random.rand()
    self.new_heading = 0
  

class Vicsek:
  def __init__(
    self,
    width: int,
    height: int,
    n_agents: int,
    speed: float,
    neighborhood_radius: float,
    noise_intensity: float
  ) -> None:
    self.width = width
    self.height = height
    self.n_agents = n_agents
    self.speed = speed
    self.neighborhood_radius = neighborhood_radius
    self.noise_intensity = noise_intensity

    self.agents = [Agent(width, height, speed) for i in range(n_agents)]
  
  def run(self, delta_t: float, duration: float):
    t = 0
    history = []
    for t in tqdm(np.arange(0, duration+delta_t, delta_t)):
      # Update headings to align with neighbors
      for a in self.agents:
        # Get average heading of neighbors (including self)
        neighbor_count = 0
        heading_sum_x = 0
        heading_sum_y = 0
        for b in self.agents:
          distance = self.toroidal_distance(a, b)
          if distance <= self.neighborhood_radius:
            neighbor_count += 1
            heading_sum_x += np.cos(b.heading)
            heading_sum_y += np.sin(b.heading)
        avg_heading = np.arctan2(heading_sum_y / neighbor_count, heading_sum_x / neighbor_count)
        noise = np.random.uniform(-np.pi, np.pi) * self.noise_intensity
        # Don't update a.heading yet, as the neighbor's updates still depend on it
        a.new_heading = avg_heading + noise

      # Update positions with new velocity
      for a in self.agents:
        a.heading = a.new_heading
        a.x = (a.x + a.speed * delta_t * np.cos(a.heading)) % self.width
        a.y = (a.y + a.speed * delta_t * np.sin(a.heading)) % self.height

      history.append({
         'x': [a.x for a in self.agents],
         'y': [a.y for a in self.agents],
         'heading': [a.heading for a in self.agents],
         't': t
      })
    return history

  def toroidal_distance(self, agent1: Agent, agent2: Agent):
    """
    Compute the distance between two agents, while taking the toroidal geometry
    into account. (i.e. agents on the far left and right edges will count as
    neighbors)
    """
    dx = abs(agent1.x - agent2.x)
    if dx > self.width:
      dx = self.width - dx
    dy = abs(agent1.y - agent2.y)
    if dy > self.height:
      dy = self.height - dy
    return np.sqrt(dx**2 + dy**2)


def animation_step(i: int, ax: Any, text: Any, history: list[np.ndarray]) -> Any:
    for quiver in ax.collections:
      quiver.remove()
    ax.quiver(history[i]['x'], history[i]['y'], np.cos(history[i]['heading']),np.sin(history[i]['heading']), pivot='mid')
    text.set_text(f"t={history[i]['t']:.2f}")
    return [ax]


def animate(
    width: int,
    height: int,
    history: list[np.ndarray],
    delta_t: float,
    annotation: str,
    save_to_file: bool
) -> None:
    fig, ax = plt.subplots(figsize = (width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    text = ax.annotate("t=", (width-1, -0.5), fontsize="x-large", annotation_clip=False, va='top')
    ax.annotate(annotation, (0, -0.5), fontsize="x-large", annotation_clip=False, va='top')
    ax.quiver(history[0]['x'],history[0]['y'],np.cos(history[0]['heading']),np.sin(history[0]['heading']))
    anim = FuncAnimation(
      fig,
      animation_step,
      fargs=(ax, text, history),
      frames=len(history),
      interval=delta_t*1000,
      repeat=False,
    )

    if save_to_file:
      writer = FFMpegWriter(fps=1/delta_t, bitrate=1800)
      anim.save('vicsek_' + datetime.now().strftime("%Y%m%d%H%m%S") + '.mp4', writer=writer) 
    plt.show()

def main() -> None:
  config = ConfigParser()
  config.read("simulation_params.ini")
  width = config["Environment"].getint("width")
  height = config["Environment"].getint("height")
  n_agents = config["Simulation"].getint("n_agents")
  duration = config["Simulation"].getfloat("duration")
  delta_t = config["Simulation"].getfloat("delta_t")
  speed = config["Agent"].getfloat("speed")
  neighborhood_radius = config["Agent"].getfloat("neighborhood_radius")
  noise_intensity = config["Agent"].getfloat("noise_intensity")
  save_to_file = config["Animation"].getboolean("save_to_file")

  sim = Vicsek(    
    width,
    height,
    n_agents,
    speed,
    neighborhood_radius,
    noise_intensity)

  print(f"Running simulation with {n_agents} agents for {duration / delta_t} time steps...")
  history = sim.run(delta_t, duration)

  print(f"Simulation complete. Generating animation...")
  annotation = f"# agents: {n_agents}\nEnvironment size: {width}x{height}\nEta: {noise_intensity}"
  animate(width, height, history, delta_t, annotation, save_to_file)

if __name__ == "__main__":
    main()
