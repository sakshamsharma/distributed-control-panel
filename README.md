# distributed-control-panel
distributed-control-panel (henceforth DCP) is a python-based control panel to launch, control, and view distributed applications across machines.

# Usecase
Building, testing, and showing demos of distributed p2p applications is a painful job. DCP attemps to change this.
The idea is to provide an abstraction over all the instances of the your distributed application, and all the servers it is being run on.

DCP does this by launching an HTTP process on each of your servers (it uses SSH to authenticate on each of the servers the first time). This process now knows how to launch instances of your binary on each of the server, as well as how to stop them.

Furthermore, you get easy access to logs of each instance, full control over their CLI arguments, as well as other utility features.

All this is done inside an interactive Python shell, which means you can interact with the outputs in whatever way you like, within the comfort of Python.

A (potentially outdated) list of useful variables is shown here:
- nodes
- servers
- logs
- shutdown_all_servers()
- setup_all_servers()
- run_binaries_on_all_nodes()
- stop_binaries_on_all_nodes()
- Tmux.ls(?server)

All processes are run inside tmux sessions, and the scripts are written for python 3.

Each node is an instance of the Node class, and each server is an instance of the Server class. These provide many more utility functions, which you can look into. Documentation for the same will be available in the future.

# Running
```
./dcp.sh --help
./dcp.sh --cfg=config.json --nodes=3 --edges=5
```
