from model.job import Job
from model.machine import Machine
from model.world import World

if __name__ == "__main__":
    world = World()

    machine = Machine(id=0, world=world)
    world.add_agent(machine)

    for i in range(0, 30):
        world.tick()
        print(f"[TIME] {world.now()}")

        if world.now() == 5:
            job = Job(id=1, print_time=10, world=world)
            world.add_agent(job)

        world.send_messages()
        world.call_next()
