import importlib.util
import importlib
import os
import sys
from typing import Callable

def load_agent(agent_path: str) -> Callable:
    """
    Loads the agent from either a file path or module name.
    If a .py file is passed, it will be loaded as a module with a unique name.
    If a module name is passed, it will be imported normally (recommended for multiprocessing).
    """

    # If it's a .py file path, load it using a unique module name
    if agent_path.endswith(".py"):
        module_name = os.path.splitext(os.path.basename(agent_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, agent_path)
        agent_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = agent_module  # ensure consistent identity
        spec.loader.exec_module(agent_module)
    else:
        # Treat it as a normal importable module
        agent_module = importlib.import_module(agent_path)

    if not hasattr(agent_module, 'agent_move'):
        raise ValueError(f"Agent module '{agent_path}' does not define 'agent_move' function.")

    return getattr(agent_module, 'agent_move')
